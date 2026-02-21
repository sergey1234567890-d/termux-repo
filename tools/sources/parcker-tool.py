import sys

import zstandard as zstd

import shutil
import tarfile
import json
import hashlib
import pathlib
import argparse
import os
class Parckers:
    def __init__(self, name,):
        self.ins = name+'.tar'
        self.ins1 = self.ins+'.zst'
        self.ins2 = name+'.apt2'
        self.path = pathlib.Path(name)
        self.conl = 'control.json'
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
    def nuw_control(self, *, input_f,):
        """ Фунция для создание control.json
        input_f параметор  путь для exe
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
    def json_control_seve(self,):
        """File параметор пути для control.json"""
        try:
            with open(self.update_path0/self.conl, 'w') as f:
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
    def zsts(self, lavel1=19):
        cxx = zstd.ZstdCompressor(level=lavel1)
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
    def __init__(self):
        self.par = argparse.ArgumentParser(
            description='''The standard apt2 packaging tool uses the zstandard compression algorithm. Help at 
            https://sergey1234567890-d.github.io/MysiteAPTFW/'''
        )
        self._args()
    def _args(self,):
        self.par.add_argument(
            'name',
            type=str,
            help='''
        The namа parameter
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
        a = Parckers(name)
        a.nuw_control(input_f=exe)
        a.json_control_seve()
        a.tar()
        a.zsts()
if __name__ == '__main__':
    s = CLI()
    s.run()