import os
import shutil
from typing import List

from elftools.elf.elffile import ELFFile

from .arch import ARCH
from .utils import arch_to_abi


class Injector:
    @staticmethod
    def inject_library(source: str, unpack_path: str, smali_path: str = None, extra_files: List[str] = None, skip_copy=False) -> None:
        """
        Injects a library into an unpacked apk.

        :param source: The path to the shared library to inject.
        :type source: str
        :param unpack_path: The path to the apktool unpacked apk.
        :type unpack_path: str
        :param smali_path: The path to the smali file to inject into. Leave empty to skip this step. Defaults to None.
        :type smali_path: str, optional
        :param extra_files: Extra files to copy over the to the apk lib/ folder. Defaults to None.
        :type extra_files: list of str, optional
        :param skip_copy: Whatever to copy the library into target, or skip and just edit the smali. Defaults to False.
        :type skip_copy: bool, optional

        :return: If the injection was successful or not.
        :rtype: bool
        """
        lib, _ = os.path.splitext(os.path.basename(source))
        lib = lib.split('lib', 1)[-1]
        lines = []
        injected = False
        if smali_path and not os.path.isfile(smali_path):
            return injected

        arch = Injector.guess_arch_from_lib(source)
        abi = arch_to_abi(arch.lower())

        if not skip_copy:
            path = os.path.join(unpack_path, 'lib', abi)
            if not os.path.isdir(path):
                os.makedirs(path)
            paths = []
            paths.append(source)
            if extra_files:
                paths.extend(extra_files)
            for file in paths:
                name = os.path.basename(file)
                dest = os.path.join(path, name)
                if os.path.isfile(dest):
                    os.remove(dest)
                shutil.copyfile(file, dest)

        injected = not bool(smali_path)
        if smali_path:
            with open(smali_path, 'r') as smali:
                lines = smali.readlines()
            matches = []
            for line in lines:
                if 'const-string v0, "{}"\n'.format(lib) in line:
                    matches.append(line)
                if matches and 'invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V\n' in line:
                    matches.append(line)
            if len(matches) >= 2:
                return True
            for line in lines:
                if line.startswith('.method public constructor <init>()V') or line.startswith('.method static constructor <clinit>()V'):
                    index = lines.index(line)
                    if lines[index + 1].startswith('    .locals'):
                        lines.insert(
                            index + 2, '    const-string v0, "{}"\n'.format(lib))
                        lines.insert(
                            index + 3, '    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V\n')
                        injected = True
                        break
                    else:
                        lines.insert(
                            index + 1, '    const-string v0, "{}"\n'.format(lib))
                        lines.insert(
                            index + 2, '    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V\n')
                        injected = True
                        break
            with open(smali_path, 'w') as smali:
                smali.writelines(lines)
        return injected
    
    @staticmethod
    def guess_arch_from_lib(lib_path: str) -> ARCH:
        with open(lib_path, 'rb') as libfile:
            elffile = ELFFile(libfile)
            arch = elffile.get_machine_arch()
            if arch.lower() in ['aarch64', 'arm64']:
                arch = ARCH.ARM64
            if arch.lower() in ['x64']:
                arch = ARCH.X64
        return arch
            