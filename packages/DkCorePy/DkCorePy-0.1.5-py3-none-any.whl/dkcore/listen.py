import hashlib
import binascii
import time


def import_module(module_names):
    if isinstance(module_names, str):
        _check(module_names)
    elif isinstance(module_names, list):
        for module_name in module_names:
            _check(module_name)


def _check(file):
    try:
        file_name = file.split("/")[-1]
        with open(file, "r", encoding="utf-8") as file:
            content = file.read()
        __dk_core_secret__ = content.split("= 0x0")
        __dk_core_secret__ = __dk_core_secret__[1].split("16DC")[0]
        __dk_rm_secret__ = f"__dk_core__ = 0x0{__dk_core_secret__}16DC"
        __dk_core_code__ = content.split("= 0x1")
        __dk_core_code__ = __dk_core_code__[1].split("7079")[0]
        __dk_md5__ = hashlib.md5(content.encode()).hexdigest()
        __dk_lines__ = content.split('\n')
        __dk_lines__ = [__line__ for __line__ in __dk_lines__ if __line__ != __dk_rm_secret__]
        new_content = '\n'.join(__dk_lines__)
        __real_dk_core_secret__ = hashlib.md5(new_content.encode()).hexdigest()
        __not_dk__ = binascii.unhexlify(__dk_core_code__).decode('utf-8') not in file_name
        if __dk_core_secret__ != __real_dk_core_secret__ or __not_dk__:
            while True:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    exit()
                except:
                    pass
    except Exception as t:
        exit()
