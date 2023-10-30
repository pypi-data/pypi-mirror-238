from multiprocessing import Lock, Pool
import os
from events import Event
from unpacker import run_unpacker
from unpacker.hi_module import HiModule


class HiContext:
    def __init__(self) -> None:
        self.modules:{int, HiModule} = {}
        self.isready:bool = False
        self.onFileEntryReadAndCheck = Event()
        pass

    def AddSubscribersForOnFileEntryReadAndCheck(self, objMethod):
        self.onFileEntryReadAndCheck += objMethod

    
    def RemoveSubscribersFileEntryReadAndCheck(self, objMethod):
        self.onFileEntryReadAndCheck -= objMethod

    @classmethod
    def get_instance(cls):
        """Obtiene la instancia del singleton"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance
    
    def read_module_and_all_tag(self, module, deploy_path):
        hi_module = HiModule(f"{deploy_path}/{module}.module")
        hi_module.readIn()
        hi_module.readAllTagFilesIn(self.onFileEntryReadAndCheck)
        return hi_module

    
    def findRef(self, int_ref:int):
        for k in self.modules:
            if self.modules[k].hiFileTagGlobalIdMap.keys().__contains__(int_ref):
                return self.modules[k].hiFileTagGlobalIdMap[int_ref]
        return None



    def read_all_modules_on_path(self, ex_path_filter = '\\ds\\', deploy_path = ''):
        # Ignoring module hd files

        p = [os.path.join(dp, f)[len(deploy_path):].replace("\\", "/") for dp, dn, fn in
            os.walk(os.path.expanduser(deploy_path)) for f in fn if ".module" in f and ".module_" not in f and not dp.__contains__(ex_path_filter)]

        with Pool(processes=os.cpu_count()) as pool:
            multiple_results = [pool.apply_async(self.read_module_and_all_tag, (file.replace(".module", ""), deploy_path)) for file in p]
            for res in multiple_results:
                try:
                    hi_module = res.get(timeout=90)
                    if len(hi_module.hiFileTagGlobalIdMap) >0:
                        self.modules[hi_module.moduleHeader.ModuleIntId]  = hi_module
                        print(hi_module.moduleHeader.ModuleIntId)
                except TimeoutError:
                    pass
                
        
        pass

    def read_all_modules_on_path_no_paralell(self, ex_path_filter = '\\ds\\', deploy_path = ''):
        # Ignoring module hd files

        p = [os.path.join(dp, f)[len(deploy_path):].replace("\\", "/") for dp, dn, fn in
            os.walk(os.path.expanduser(deploy_path)) for f in fn if ".module" in f and ".module_" not in f and not dp.__contains__(ex_path_filter)]

        for file in p:
            hi_module = self.read_module_and_all_tag(file.replace(".module", ""), deploy_path)
            if len(hi_module.hiFileTagGlobalIdMap) >0:
                self.modules[hi_module.moduleHeader.ModuleIntId]  = hi_module
                print(hi_module.moduleHeader.ModuleIntId)
            
        
        pass   