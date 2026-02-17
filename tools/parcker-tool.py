import zstandard as zstd
import tarfile
import json

control = {
    'author' : 'sergey',
    'name': 'helo',
    'version' : '1.0.0',
    'architecture' : 'amd64',
    'depends' : [],
}
class Parckers():
    def json_control(self, file, data):
        try:
            with open(file, 'w') as f:
                json.dump(data, f, indent=4)
        except FileNotFoundError:
            print('No such file or directory')
    def parcker(self, path, out = None, *, out1):
        try:
            with tarfile.open(out1, 'w') as tar:
                tar.add(path, arcname=out)
        except FileNotFoundError:
            print('No such file or directory')
    def zsts(selff):
        pass
a = Parckers()
