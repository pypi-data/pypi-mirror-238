import glob
import hashlib
from os.path import dirname, isfile, basename

all_mods_path = []


def __list_all_modules(loc):
    global all_mods_path
    work_dir = dirname(loc)
    work_dir = work_dir[:work_dir.rfind("/")]
    work_dir = work_dir + "/dk"
    mod_paths = glob.glob(work_dir + "/*/*.py")
    mod_paths.extend(glob.glob(work_dir + "/*.py"))
    all_mods_path = [
        f
        for f in mod_paths
        if isfile(f)
           and f.endswith(".py")
           and not f.endswith("plugins/__init__.py")
    ]

    return all_mods_path


def gen_hash(module_paths):
    for mpath in module_paths:
        with open(mpath, "r+", encoding="utf-8") as file:
            content = file.read()
            core_position = content.find('__dk_core__')
            __md5_hash__ = hashlib.md5(content.encode()).hexdigest()
            if core_position != -1:
                new_content = content[:core_position] + f"__dk_core__ = 0x0{__md5_hash__}16DC\n"
                new_content += content[core_position:]
                file.seek(0)
                file.write(new_content)
                file.truncate()
            else:
                print("Not found")


__all__ = sorted(__list_all_modules(__file__))
gen_hash(__all__)