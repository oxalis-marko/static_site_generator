import os
import shutil
import re

def dir_cp(src, dst):
    if os.path.exists(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)
        dir_list = os.listdir(src)
        pattern = re.compile(r'(Zone.Identifier$|^\.|\.tmp$|^Thumbs\.db$)')
        for entry in dir_list:
            if pattern.search(entry):
                continue
            e_path = os.path.join(src, entry)
            if os.path.isfile(e_path):
                shutil.copy(e_path, dst)
            else:
                dst_path = os.path.join(dst, entry)
                dir_cp(e_path, dst_path)
        shutil.rmtree(src)
    else:
        raise Exception(f"{src} does not exist")