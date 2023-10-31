import numpy as np

from typing import Callable
from ctypes import c_float

from bondzai.davinsy_py.enums import EventOperationID, DBMTable, DBMAttributesVM, KPITypes
from bondzai.davinsy_py.davinsy import DAT_ATTRIBUTE
from bondzai.davinsy_py.davinsy import Table, set_agent_id, get_agent_id
from bondzai.davinsy_py.model import VirtualModel, PreprocPhase, compute_dbm_row_size_class, compute_dbm_row_size_reg, compute_ctx_row_size
from bondzai.davinsy_py.preproc import Preproc
from bondzai.davinsy_py.model import CATTROWID, CMETALABEL, CROWID, CMeta_factory, VirtualModel
from bondzai.davinsy_py.operations import OperationRegistry,CUST_OP,CPUSH_INFERINFO,CPUSH_PARAM,CMODE_PARAM,CEVENT_ID
from .logger import logger

try:
    import davinsy_run
    import davinsy_mal
    import davinsy_dbm
    import davinsy_log
except ModuleNotFoundError:
    raise Exception("Cannot import C libs")


class DvsCom():

    """
    Define the abstract link object between sensor and DavinSy
    """
    def __init__(self):
        """
        Load agent for its config
        Args:
            config: Config object
        """
        self.connect()

        # inherited for WSPProxySDK - Agent
        self.device_name = "local_device"
        self.gateway = None

        self._active_label = None

        self._wait_response = {}

        self._on_log_handlers: dict[str, Callable[[DvsCom, str], None]] = {}
        self._on_event_handlers: dict[str, Callable[[DvsCom, EventOperationID, dict], None]] = {}

        self._on_train_done_handlers: dict[str, Callable[[DvsCom, dict], None]] = {}
        self._on_final_process_done: dict[str, Callable[[DvsCom, dict], None]] = {}
        self._on_infer_done_handlers: dict[str, Callable[[DvsCom, dict], None]] = {}

        self.last_infer_data = {}

    ###############################
    ## BOOTSTRAP 
    ###############################
    def connect(self):
        """
        nothing in local
        """
        self.davinsy_connect = OperationRegistry()
        self.davinsy_connect.add_event_listener(self._handle_message)

    def set_agent_id_in_bld(self,agent_id):
        return set_agent_id(agent_id)

    def get_agent_id_from_bld(self):
        id_as_bytearray = get_agent_id()
        return id_as_bytearray.decode()

    def get_kpis(self):
        """
        Extract KPIs (only working for static mod)
        Returns:
            kpis: list of KPI dicts
        """


        allkpis = davinsy_log.get_kpis()

        kpis = []
        filtersKPI = {'TRAINING_TIME_START', 'INFER_TIME_START', 'PREPROC_TIME_START', 'PREPROC_I_TIME_START',
                      'POSTPROC_TIME_START', 'OTHER_TIME_START'}
        for kpi in allkpis:
            try:
                typname = KPITypes(kpi['type']).name
                unit = str(KPITypes(kpi['type']))
                if typname not in filtersKPI:
                    kpis.append({
                        "type": typname,
                        "label": kpi['desc'],
                        "unit": unit,
                        "value": kpi["value"]
                    })

            except Exception as e:
                logger.error(f"{kpi['type']} is not a valid KPI ID : {e}")
        return kpis

    def get_uids(self):
        """
        Get the correspondance table between UUIDs and Local IDs
        Returns:
            uuids: list of operation UUIDs
        """
        return davinsy_run.get(0x300)


    def new_table(self,type, nb_rows: int, row_size :int):
        """
        Create a new table in Davinsy
        """

        table = Table(type,davinsy_dbm.new_table(type, nb_rows, row_size),nb_rows, row_size)
        return table

    def create_vm_table(self,rowsize: int,nb_max_vm: int ):
        """
        Create a new VM table in Davinsy
        """
        return self.new_table(DBMTable.DBM_VM.value, nb_max_vm, rowsize)

    def import_virtual_model(self,vm: VirtualModel,vm_table) : #-> Row, Dict
        """
        Create a new row in Virtual Model table and fill it with data
        """
        """
        Load th Virtual Model to DavinSy
        """
        # Load VM in Davinsy
        vmName = vm.get_name()
        
        preproc = {}
        preproc[vmName]={}
        rowsize = vm.get_vm_row_size()
        # Get the C version of it
        desc = bytearray(vm.get_C_description())
        deeplomath = bytearray(vm.get_C_deeplomath())
        postproc = bytearray(vm.get_C_postproc())

        # access to preproc from python
        recompute_size = False
        if recompute_size :
            preprocSize = 0
            for preprocPhase in PreprocPhase:
                preproc_c = vm.get_C_preproc(preprocPhase.value)
                if preproc_c is None:
                    # logger.warn("Preproc of type %s not present in the VM" % preprocPhase.name)
                    continue
                _preproc = bytearray(preproc_c)
                preprocSize += len(_preproc)
                preproc[vmName][preprocPhase] = Preproc(_preproc)  # infer used as preprocess BEFORE storage in raw mode

            rowsize = len(desc) + preprocSize + len(deeplomath) + len(postproc)
        else: # convert
            preprocSize = 0
            for preprocPhase in PreprocPhase:
                preproc_c = vm.get_C_preproc(preprocPhase.value)
                if preproc_c is None:
                    # logger.warn("Preproc of type %s not present in the VM" % preprocPhase.name)
                    continue
                _preproc = bytearray(preproc_c)
                preproc[vmName][preprocPhase] = Preproc(_preproc)  # infer used as preprocess BEFORE storage in raw mode

        # Creating the Virtual Model table at the good size
        logger.debug("total vm size = %d")

        # Storing in the VM table
        vmName = vm.get_name()
        if len(vmName) > 16:
            logger.warn("vm name might be too long = %s" % (vmName))

        row = vm_table.new_row(vmName)
        row.set_attribute(DBMAttributesVM.DBM_ATT_VM_DESC, desc)
        
        is_cond = False
        if PreprocPhase.DATA_TRANSFORM in preproc[vmName]:
            logger.info("Push DATA_TRANSFORM as INFER")
            row.set_attribute(DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_INFER, preproc[vmName][PreprocPhase.DATA_TRANSFORM].graph)
            is_cond = True
        elif PreprocPhase.FEATURE_EXTRACTION in preproc[vmName]:
            logger.info("Push FEATURE_EXTRACTION for TRAIN & INFER")

            row.set_attribute(DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_INFER, preproc[vmName][PreprocPhase.FEATURE_EXTRACTION].graph)
            row.set_attribute(DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_TRAIN, preproc[vmName][PreprocPhase.FEATURE_EXTRACTION].graph)
        else:
            raise Exception(f"Invalid Virtual Model {vmName}, Data Transform or Feature Extraction is requested")           

        if not is_cond:
            if PreprocPhase.DATA_AUGMENTATION in preproc[vmName]:
                logger.info(f"Push DATA_AUGMENTATION for TRAIN")
                row.set_attribute(DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_DATA_AUGMENTATION, preproc[vmName][PreprocPhase.DATA_AUGMENTATION].graph)
            else:
                raise Exception(f"Invalid Virtual Model {vmName}, Data Augmentation is requested")           

            if PreprocPhase.BACKGROUND_ADAPTATION in preproc[vmName]:
                logger.info("Push BACKGROUND_ADAPTATION for TRAIN")
                row.set_attribute(DBMAttributesVM.DBM_ATT_VM_PREPROC_GRAPH_BACKGROUND_AUGMENTATION, preproc[vmName][PreprocPhase.BACKGROUND_ADAPTATION].graph)
            else:
                raise Exception(f"Invalid Virtual Model {vmName}, Background Augmentation is requested")           

        row.set_attribute(DBMAttributesVM.DBM_ATT_VM_DEEPLOMATH, deeplomath)
        row.set_attribute(DBMAttributesVM.DBM_ATT_VM_POSTPROC, postproc)

        return row, preproc

    def create_dbm_table(self,rawDataMaxLen,maxLabels,maxRegLen,maxNbRawData):
        """
        Create database table in memory
        """

        max_size_row_class = compute_dbm_row_size_class(rawDataMaxLen,maxLabels)
        max_size_row_reg = compute_dbm_row_size_reg(rawDataMaxLen,maxRegLen)
   
        maxsize_row = max(max_size_row_class,max_size_row_reg)
        # ---- DAT ----
        datTable = self.new_table(DBMTable.DBM_DAT.value, maxNbRawData, maxsize_row)
        if datTable is None:
            logger.error(f"Issue during DAT table creation row size {maxsize_row}, number of rows {maxNbRawData}")

        return datTable

    def create_ctx_table(self,nb_vm):
        """
        Create database table in memory
        """

        sizeof_DLM_ENV = compute_ctx_row_size()
   
        # ---- CTX ----
        ctxTable = self.new_table(DBMTable.DBM_CTX.value, nb_vm, sizeof_DLM_ENV)
        if ctxTable is None:
            logger.error(f"Issue during CTX table creation row size {sizeof_DLM_ENV}, number of rows {nb_vm}")

        return ctxTable
    
#    def register_external_ops(self,opId: str,operation: callable,registry):
#        registry.add_custom_operation(opId,operation)
#        return

    def import_one_raw_data_classification(self,table: Table, inputVect: np.ndarray, expectedOutput: np.ndarray) -> bool:
        """
        Create a new row in Data table and fill it with data
        """
        """
        Create a new row in Data table and fill it with data
        """
        isLoaded = False
        isMetaLoaded = False
        dbm_row = table.new_row(None)

        #labelList = [CMETALABEL(id=CATTROWID(length=0, id=CROWID(index=idx + 1)), label = out) # 0 because it's a list of list
        #                for idx, out in enumerate(expectedOutput)]
        labelList = []
        nb_labels = 0
        for k in range(0,len(expectedOutput),2):
            metalabel = CMETALABEL(id=CATTROWID(length=0, id=CROWID(index=expectedOutput[k])), label = expectedOutput[k+1])
            labelList.append(metalabel)
            nb_labels+=1
        meta = bytearray(
            CMeta_factory(0, nb_labels)(
                type=0,
                qi=1,
                labels=(nb_labels * CMETALABEL)(*labelList),
                )
            )
        dbm_row.set_attribute(DAT_ATTRIBUTE.DBM_ATT_DAT_META, meta)
        isMetaLoaded = True
        if isMetaLoaded:
            dbm_row.set_attribute(DAT_ATTRIBUTE.DBM_ATT_DAT_DATA, bytearray(inputVect))
            isLoaded = True
        return isLoaded

    def import_one_raw_data_regression(self,table: Table, inputVect: np.ndarray, expectedOutput: np.ndarray) -> bool:
        isLoaded = False
        isMetaLoaded = False
        dbm_row = table.new_row(None)

        expectedOutput_linear = expectedOutput[0]
        len_gt = int(len(expectedOutput_linear))
        vect = CMeta_factory(1, len_gt)(
            type=1,
            qi=1,
            values=(len_gt * c_float)(*expectedOutput_linear)  # (len_gt*c_float)a
        )
        meta = bytearray(vect)
        dbm_row.set_attribute(DAT_ATTRIBUTE.DBM_ATT_DAT_META, meta)
        isMetaLoaded = True


        if isMetaLoaded:
            dbm_row.set_attribute(DAT_ATTRIBUTE.DBM_ATT_DAT_DATA, bytearray(inputVect))
            isLoaded = True

        return isLoaded
    
    def export_one_record(self,handle: int, index: int):
        """
        Get one record from dataset
        """
        pass

    def get_all_tables(self):
        """
        Get all tables in Davinsy
        """
        pass

    def go_enroll_mode(self, labels: list):
        """
        Set DavinSy in enroll mode
        """
        pass

    def go_infer_mode(self):
        """
        Set DavinSy in infer mode
        """
        pass

    def end_init(self):
        """
        End initialization (needed on some platforms)
        """
        pass

    def get_life_cycle(self):
        """
        Get life cycle of the agent
        Returns:
            life_cycle: life cycle of the agent
        """
        return davinsy_mal.get(0x0300)  # MAL LIFE CYCLE
    
    ###############################
    ## RUN 
    ###############################
    

    def _handle_message(self, op_id, event, param, inp) -> None:
        data = {}
        if op_id == CUST_OP.OP_TRAIN_INFO.value:
            print("DVS LOCAL COM TRAIN DONE")
            logger.info("== DVS LOCAL COM TRAIN DONE")
            for callback in self._on_train_done_handlers.values():
                print(f"DVS LOCAL COM TRAIN DONE CALLBACK {callback}")
                callback(self, data)

        elif op_id == CUST_OP.OP_INFER_INFO.value:
            logger.info("== OP_INFER_INFO")
            param = CPUSH_PARAM.from_address(param)
            info =  CPUSH_INFERINFO.from_address(inp)
            allinfo = info.todict()
            self.last_infer_data = {}
            self.last_infer_data["param"] = param
            self.last_infer_data["info"] = allinfo
            logger.info("PST " + str(self.last_infer_data))

        elif op_id == CUST_OP.OP_SEND_EVT_ID.value:
            logger.info("== OP_SEND_EVT_ID")
            param = CMODE_PARAM.from_address(param)
            info = CEVENT_ID.from_address(inp)
            res_tmp = dict()
            res_tmp["param"] = param.mode
            res_tmp["evtid"] = info.evtid

            if info.evtid == EventOperationID.EVT_INT_INFER_DONE.value:
                self.last_infer_data["evtid"] = info.evtid
                #self.last_infer_data["param"] = info.param # Is it usefull ?
                for callback in self._on_infer_done_handlers.values():
                    callback(self, self.last_infer_data)
                # clear
                self.last_infer_data = {}
            if info.evtid == EventOperationID.EVT_INT_FINAL.value:
                print("DVS LOCAL COM EVT_INT_FINAL")
                for callback in self._on_final_process_done.values():
                    print(f"DVS LOCAL COM EVT_INT_FINAL CALLBACK {callback}")
                    callback(self, res_tmp)

    def remove_observer(self, dict_obj_name, idx):
        if not hasattr(self, dict_obj_name):
            return 
        dict_obj = getattr(self, dict_obj_name)
        if hasattr(dict_obj, idx):
            delattr(getattr(self, dict_obj_name), idx)

    def set_active_label(self, label_id: int) -> None:
       pass

    # NEW 
    def force_train(self,mode:int):
        data = [mode]
        evt_id = int(EventOperationID.EVT_INT_FORCE_TRAIN.value)
        davinsy_run.push_evt(evt_id, bytearray(data))

    def on_log(self, callback: Callable[["DvsCom", str], None]) -> None:
        cb_id = f"onlog-{len(self._on_log_handlers.keys())}"
        self._on_log_handlers[cb_id] = callback
        return lambda: self.remove_observer("_on_log_handlers", cb_id)

    def on_event(self, callback: Callable[["DvsCom", EventOperationID, dict], None]) -> None:
        cb_id = f"onevent-{len(self._on_log_handlers.keys())}"
        self._on_event_handlers[cb_id] = callback
        return lambda: self.remove_observer("_on_event_handlers", cb_id)

    def on_training_done(self, callback: Callable[["DvsCom", dict], None]) -> None:
        cb_id = f"ontraindone-{len(self._on_log_handlers.keys())}"
        self._on_train_done_handlers[cb_id] = callback
        return lambda: self.remove_observer("_on_train_handlers", cb_id)

    def on_inference_done(self, callback: Callable[["DvsCom", dict], None]) -> None:
        cb_id = f"oninferdone-{len(self._on_log_handlers.keys())}"
        self._on_infer_done_handlers[cb_id] = callback
        return lambda: self.remove_observer("_on_infer_done_handlers", cb_id)

    def on_final_process_done(self, callback: Callable[["DvsCom", dict], None]) -> None:
        cb_id = f"onfinaldone-{len(self._on_log_handlers.keys())}"
        self._on_final_process_done[cb_id] = callback
        return lambda: self.remove_observer("_on_final_process_done", cb_id)
