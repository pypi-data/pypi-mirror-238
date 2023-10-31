import traceback
import numpy as np

from bondzai.davinsy_py.davinsy import  alloc_mms_ring

from .dvs_config import DvsConfig
from .logger import logger
from .dvs_com import DvsCom


class DvsAgent:
    """
    Agent object, represent the direct interface to DavinSy
    """
    def __init__(self, config: DvsConfig = None,link: DvsCom = None, data_path = None):
        """
        Load agent for its config
        Args:
            config: Config object
            dataset: Dataset object
        """

        logger.debug("Agent init")

        # Load from config
        if config is None:
            self.config = DvsConfig(data_path)
        else:
            self.config = config

        # Manage communication protocol
        self.link = link

        # Define default values
        self.consistentDataChecker = None
        self.vm = []
        self.mode = None
        self.preproc = {}
        self.signalConditionning = {}  # TODO : load graph
        
        self.rawDataMaxSize = 0
        self.vmTable = None
        self.datTable = None
        self.ctxTable = None
        self.uids = None

#        self.waitEvent = WaitEvent()
        self.source_mem = {}
        self.lifecycle = -1

    def set_data_path(self,data_path):
        self.config.set_data_path(data_path)

    def get_data_path(self):
        return self.config.get_data_path()

    def set_max_nb_raw_data (self,max_nb_raw_data:int):
        if self.lifecycle != -1:
            raise Exception(" Max Number of raw data in DavinSy Database must be changed earlier in the boot steps ")
        self.config.set_max_nb_raw_data(max_nb_raw_data)

    def set_agent_id(self,agent_id):
        self.config.set_agent_id(agent_id)

    def init_and_load(self):
        """
        Init memory and prepare data structure for agent
        """
        self.lifecycle = self.link.get_life_cycle()

        logger.info(f"Device lifecycle: {self.lifecycle}")

        vms = self.config.preload_vms()

        bootstrap_info_list = self.config.get_bootstrap_info_list()

        # FOR STATIC INPUT SOURCE
        for vmName in bootstrap_info_list:
            info = bootstrap_info_list[vmName]
            if "source" in info:
                input_len = info["source"]["frame_len"] * info["source"]["max_frames_number"]
                # GO THROUGH LINK WITH A GET SOURCE RING BUFFER 
                self.source_mem[info["source"]["id"]] = alloc_mms_ring(input_len*4)

        isConsistent = all([self.check_vm_consistency(vm) for vm in self.vm])
        if not isConsistent:
            return
        if self.lifecycle == 1:
            logger.info("Device not initialized, initializing...")

            rowsize = 0
            for vm in vms:
                rowsize = max(rowsize, vm.get_vm_row_size())

            # create the VM table here 
            logger.debug(f"create_vm_table {rowsize}, {len(vms)} vms")
            self.vmTable = self.link.create_vm_table(rowsize,len(vms))
            
            uids = self.link.get_uids()
            
            #logger.debug(f"VM UID {uids}")
            # add to config ?
            logger.debug("import_virtual_model")
            for vm in vms:
                vm.set_uid2id(uids)
                row,preproc = self.link.import_virtual_model(vm,self.vmTable)
                # add to config
                self.preproc.update(preproc)

            for vm in vms:
                if vm.model["deeplomath"]["nbInstances"] == 0:
                    vm_name = vm.get_name() 
                    if vm_name in bootstrap_info_list :
                        info = bootstrap_info_list[vm_name]
                        if "source" in info:
                            # keep this preprocess for the initial dataset (data-conditionning)
                            self.signalConditionning[info["source"]["id"]] = self.config.get_bootstrap_dataconditionning(self.preproc[vm_name])

            max_raw_data = self.config.get_max_raw_data()
            if (max_raw_data<1):
                raise Exception("Max Raw Data Length (for DavinSy internal storage) not defined")
            max_label = self.config.get_max_labels()
            max_reg_len = self.config.get_max_reg_len()
            if (max_label<1 and max_reg_len < 1):
                raise Exception("Labels and regression size not defined")
            max_nb_raw_data = self.config.get_max_nb_raw_data()
            if (max_nb_raw_data < 1):
                raise Exception("Max Raw Data Length (for DavinSy internal storage) not defined")

            if (max_nb_raw_data*max_raw_data >  self.config.get_max_dbm_raw_data()):
                max_nb_raw_data = int(self.config.get_max_dbm_raw_data()/max_raw_data)
                self.config.set_max_nb_raw_data(max_nb_raw_data)
                logger.warning(f"create_dbm_table limiting : {max_nb_raw_data} elements in DavinSy internal storage")

            logger.debug(f"create_dbm_table max rawdata len: {max_raw_data}, {max_nb_raw_data} elements, with {max_label} label(s) or {max_reg_len} regression vector length")
            self.datTable = self.link.create_dbm_table(max_raw_data,
                                                       max_label,
                                                       max_reg_len,
                                                       max_nb_raw_data
                                                       )
            logger.debug("create_ctx_table")

            self.ctxTable = self.link.create_ctx_table(self.config.get_max_models())

            # create special row for correction
            # Row(self.datTable, -1, "lastin")

    def register_custom_ops_in_agent(self,custom_ops):
        for op in custom_ops:
            self.config.register_external_ops(op,custom_ops[op])

    def load_initial_data(self):
        """
        Load all data from a given dataset
        Args:
        """
        dataset_definition = None
        sourcekey = ""
        sourceid = 0
        ack = 0
        dataset_list = self.config.get_targz_file_list()
        for dataset_tar_path in dataset_list:
            my_tar = self.config.preload_targz(dataset_tar_path)
            if my_tar.tar:
                dataset_definition = self.config.load_initial_dataset_definition_targz(my_tar)

                if dataset_definition:
                    outputs_definition = dataset_definition["outputs"]
                    dataset = dataset_definition["dataset"]

                    for my_data in dataset:
                        filename = my_data["data"]
                        output = my_data["output"]

                        is_classification = True
                        if "source_id" in my_data:
                            sourcekey = my_data["source_id"]
                            sourceid = self.config.get_item_id("sources", my_data["source_id"])
                            if not sourceid:
                                sourceid = my_data["source_id"]
                        else: 
                            # sourceid = 1
                            raise Exception(f"issue during loading file {filename}, no source")

                        bootstrap_info = self.config.get_bootstrap_info_from_sourceid(sourceid)
                        if bootstrap_info == {}: # empty dict
                            raise Exception(f"Unable to find bootstrap info for source id {sourceid}")

                        groundthruth_for_davinsy = []
                        for labeltype in output:
                            # TODO- check if we need to manage the two cases
                            label_type_id = self.config.get_item_id("labels", labeltype)
                            if not label_type_id:
                                label_type_id = outputs_definition[labeltype].get("id", None)
                            if label_type_id is None:
                                raise Exception(f"Unable to find label type id for label type {labeltype}")

                            label_value = output[labeltype]

                            # manage regression here
                            if label_value in outputs_definition[labeltype]:
                                label_value_id = outputs_definition[labeltype].get(label_value, None)

                                if label_value_id is None:
                                    raise Exception(f"Unable to find label value id for {label_value}")
                                
                                groundthruth_for_davinsy.append(label_type_id)
                                groundthruth_for_davinsy.append(label_value_id)
                            else:
                                # only one vector supported for regression
                                groundthruth_for_davinsy = label_value
                                is_classification = False
                        
                        raw_input = self.config.load_data_from_dataset_targz(my_tar,filename)

                        if raw_input is None:
                            raise Exception(f"issue during loading file {filename}")


                        # MANAGE frame & hop len
                        if not "source" in bootstrap_info:
                            logger.error(f"Issue with Bootstrap {bootstrap_info}, missing source information")
                            raise Exception(f"Issue with Bootstrap")


                        frame_len = bootstrap_info["source"].get("frame_len",0)
                        file_hop_len = bootstrap_info["source"].get("file_hop_len",0)

                        if frame_len == 0 or frame_len >= len(raw_input):
                            sigVect = self.compute_raw_data(sourceid,data=raw_input)
                            if len(sigVect) < 1:
                                raise Exception(f"Unable to process data len  {str(len(raw_input))}")

                            isLoaded = self.load_one_raw_data(is_classification,inputVect=sigVect, expectedOutput=groundthruth_for_davinsy)

                            ack += int(isLoaded)

                            if ack >= (self.config.get_max_nb_raw_data()-1):
                                logger.warn("DavinSy Internal Storage for raw data might be full")
                                break
                        elif file_hop_len == 0 :
                            raw_input = raw_input[-frame_len:] # remove first sample
                            sigVect = self.compute_raw_data(sourceid,data=raw_input)
                            if len(sigVect) < 1:
                                raise Exception(f"Unable to process data len  {str(len(raw_input))}")

                            isLoaded = self.load_one_raw_data(is_classification,inputVect=sigVect, expectedOutput=groundthruth_for_davinsy)

                            ack += int(isLoaded)

                            if ack >= (self.config.get_max_nb_raw_data()-1):
                                logger.warn("DavinSy Internal Storage for raw data might be full")
                                break
                        else: # frames with over-lap
                            raw_input_rest = raw_input
                            while len(raw_input_rest) >= frame_len:
                                current_raw_input = raw_input_rest[:frame_len]
                                sigVect = self.compute_raw_data(sourceid,data=current_raw_input)
                                if len(sigVect) < 1:
                                    raise Exception(f"Unable to process data len  {str(len(current_raw_input))}")

                                isLoaded = self.load_one_raw_data(is_classification,inputVect=sigVect, expectedOutput=groundthruth_for_davinsy)

                                ack += int(isLoaded)

                                if ack >= (self.config.get_max_nb_raw_data()-1):
                                    logger.warn("DavinSy Internal Storage for raw data might be full")
                                    break

                                raw_input_rest = raw_input_rest[file_hop_len:]
                    logger.info(f"Loading {ack} data for source {sourcekey} id {sourceid}")

                else:
                    logger.debug("INITIAL DATASET HAVE NO DEFINITION")

                self.config.close_targz(my_tar)
        return ack
    

    def compute_raw_data(self, sourceid,data: np.ndarray) -> list:
        """
        Compute signature for a given vector
        Args:
            data: input raw data as list
        Returns:
            processedData: signature vector
        """
        if not sourceid in self.signalConditionning:
            return data
        return self.signalConditionning[sourceid].compute_signature(data)
    

    def load_one_raw_data(self, is_classification,inputVect: list, expectedOutput: list) -> bool:
        """
        Load one data in DavinSy database
        Args:
            inputVect: pre-processed input vector
            expectedOutput: expected output list
        Returns:
            isLoaded: True if data is correctly loaded, else False

        """

        isLoaded = False    
        inputVect = np.array(inputVect, dtype='float32')
        if (len(inputVect) > self.config.get_max_raw_data()):
            raise Exception(f" raw data length {len(inputVect)} higher that expected max raw data {self.config.get_max_raw_data()}")
            # return isLoaded
        try:
            #isLoaded = self.link.import_one_record(self.mode, self.datTable, inputVect, expectedOutput)
            if is_classification:
                expectedOutputVect = np.array(expectedOutput, dtype='int32')
                isLoaded = self.link.import_one_raw_data_classification(self.datTable, inputVect, expectedOutputVect)
            else:
                expectedOutputVect = np.array(expectedOutput, dtype='float32')
                isLoaded = self.link.import_one_raw_data_regression(self.datTable, inputVect, expectedOutputVect)

        except Exception as e:
            traceback.print_exc()
            logger.error("INVALID GT:" + str(expectedOutput) +" DATA LEN "+str(len(inputVect)) + " err: " + str(e))
        return isLoaded
    
    def configure_agent_id(self):
        agent_id = self.config.get_agent_id()
        status = self.link.set_agent_id_in_bld(agent_id)
        
        agent_id_checked = self.link.get_agent_id_from_bld()
        if agent_id_checked != agent_id:
            raise Exception(f" Agent Id not correcly setted {agent_id_checked} instead of {agent_id}")
        logger.info(f" agent identifier {agent_id_checked}")
    def update_tables(self):
        #self.link.get_all_tables()
        return
    
    # FOR DBG
    def get_source_mem(self):
        return self.source_mem