import subprocess
from subprocess import Popen, PIPE, STDOUT

def test(file):
    proc = Popen(file.name.split(' '), stdout=PIPE, stderr=PIPE)
    (output, error) = proc.communicate()
    if error != file.espected_error:
        print(f"Error not conform in {file.name}, espected {file.espected_error}, got {error}")
    if output != file.espected_output:
        print(f"Output not conform in {file.name}, espected {file.espected_output}, got {output}")
    return (output, error)

class File:
    def __init__(self, name, espected_output=b'', espected_error=b''):
        self.name             = "python main.py tests/"+name
        self.espected_output  = espected_output
        self.espected_error   = espected_error
    

files_to_test = [
    File("hello_world.porth", b'Hello, world !\r\n', b''),
]
for file in files_to_test:
    test(file)