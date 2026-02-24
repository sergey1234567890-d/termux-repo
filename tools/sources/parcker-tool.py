import sys

import zstandard as zstd

import shutil
import tarfile
import json
import hashlib
import pathlib
import argparse
import os
class Parcker:
    """Класс для сжатия и сбора пакета и запись информации о пакеты в формат .apt2"""
    def __init__(self, name: str) -> None:
        """Функция инит нужна для подготовки данных.
        Name это имя пакета для создания пакета .apt2"""
        self.ins = name+'.tar'
        self.ins1 = self.ins+'.zst'
        self.ins2 = name+'.apt2'
        self.path = pathlib.Path(name)
        self.conf = 'control.json'
        con = 'control'
        bns = 'bin'
        self.update_path0 = self.path / con
        self.update_path0.mkdir(parents=True, exist_ok=True)
        self.update_path = self.path / bns
        self.update_path.mkdir(parents=True, exist_ok=True)
        self.control = {
            'author': '',
            'name': '',
            'version': '',
            'architecture': 'amd64',
            'depends': [],
            'sha256': ' ',
        }
    def nuw_control(self, *, input_f: str) -> None:
        """ Функция для создания control.json c информации о пакете
        input_f параметр путь до exe
"""

        try:
            file_path = pathlib.Path(input_f)
            file_path.rename(self.update_path / file_path.name)
            f = self.update_path / file_path.name

            for sf in self.control:
                if 'architecture' in s:
                    continue
                elif 'sha256' in s:
                    break
                i = input(sf +': ')
                self.control[sf] = i

            with open(f, 'rb') as f:
                returns = hashlib.file_digest(f, 'sha256')
            self.control['sha256'] = returns.hexdigest()
        except FileNotFoundError:
            print('No such file or directory')
            sys.exit()
    def json_control_save(self) -> None:
        """Функция для сохранения файл control.json по пути control\control.json"""
        try:
            with open(self.update_path0/self.conf, 'w') as f:
                json.dump(self.control, f, indent=4)
        except FileNotFoundError:
            print('No such file or directory')
            sys.exit()
    def tar(self, out = None,):
        try:

            with tarfile.open(self.ins, 'w') as tar:
                tar.add(self.path, arcname=out)
        except FileNotFoundError:
            print('No such file or directory')
            sys.exit()
    def zst(self, level1: int =19) -> None:
        cxx = zstd.ZstdCompressor(level=level1)
        try:
            with open(self.ins, 'rb') as f1:
                with open(self.ins1, 'wb') as f2:
                    cxx.copy_stream(f1, f2)
            print(f'done {self.ins1}')
            os.remove(self.ins)
            if os.path.exists(self.path):
                try:
                    shutil.rmtree(self.path)
                    print(f'Done remove dir {self.path}')
                except OSError as err:
                    print(f'Error remove dir {err.strerror}')
            else:
                print(f'No such file or directory {self.path}')
            os.rename(self.ins1, self.ins2)
        except FileNotFoundError:
            print('No such file or directory')
            sys.exit()

class CLI:
    """class CLI нужен для обработки аргументов с командной строки """
    def __init__(self) -> None:
        """Функция __init__ для обработки аргументов из модуля argparse  """
        self.par = argparse.ArgumentParser(
            description=''' Version 0.1.0 The standard apt2 packaging tool uses the zstandard compression algorithm. Help at 
            https://sergey1234567890-d.github.io/MysiteAPTFW/'''
        )
        self._args()
        self.args = None
    def _args(self,) -> None:
        """Функция создание параметров и позиционных аргументов"""
        self.par.add_argument(
            'name',
            type=str,
            help='''
        The name parameter
        is a mandatory argument and takes the name of the package to create.''',
        )
        self.par.add_argument(
            'exe',
            type=str,
            help='The exe flag accepts the path to the executable .EXE file. Required argument',
        )
    def run(self):
        self.args = self.par.parse_args()
        self.main(self.args.name, self.args.exe)
    @staticmethod
    def main(name, exe):
        a = Parcker(name)
        a.nuw_control(input_f=exe)
        a.json_control_save()
        a.tar()
        a.zst()
if __name__ == '__main__':
    s = CLI()
    s.run()