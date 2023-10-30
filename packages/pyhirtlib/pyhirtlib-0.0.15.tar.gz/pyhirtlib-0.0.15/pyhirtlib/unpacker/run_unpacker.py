import os
from unpacker.hi_module import HiModule

def extract_module(module, save_to_files = False, unpack_path = '', deploy_path = ''):
    hi_module = HiModule(f"{deploy_path}/{module}.module")
    hi_module.readIn()
    return hi_module    

def extract_all_modules(save_to_files = True, unpack_path = '', deploy_path = '')->[]:
    # Ignoring module hd files
    result = []
    p = [os.path.join(dp, f)[len(deploy_path):].replace("\\", "/") for dp, dn, fn in
         os.walk(os.path.expanduser(deploy_path)) for f in fn if ".module" in f and ".module_" not in f]
    for file in p:
        # print(file)
        result.append(extract_module(file.replace(".module", ""), save_to_files, unpack_path, deploy_path))
    return result


