import subprocess
import tempfile

def create_input_file(string):
    file = open(('test.txt'),'w')
    file.write(string)
    file.close()

def write_string_to_printer(string):
    print(str(string))
    return create_input_file(str(string)), print_to_fiscal()

def print_to_fiscal():
    entrada = './iobatch -p 192.168.3.79 -s 1000 -i test.txt -o salida.txt'
    #subprocess.call(entrada)
    subprocess.check_call(entrada, stdin=None, stdout=None, stderr=None, shell=True)

def print_X():
    cierrex = './iobatch -p 192.168.3.79 -s 1000 -i ./files/cierrex.txt -o salida.txt -n 3 -t 5 -v'
    subprocess.check_call(cierrex, stdin=None, stdout=None, stderr=None, shell=True)

def print_Z():
    cierrez = './iobatch -p 192.168.3.79 -s 1000 -i ./files/cierrez.txt -o salida.txt -n 3 -t 5 -v'
    subprocess.check_call(cierrez, stdin=None, stdout=None, stderr=None, shell=True)



    # fp = tempfile.NamedTemporaryFile(delete=False)
    # fp.write(string.encode('latin1'))
    # fp.close()
    # subprocess.call(["cat", fp.name])
    #subprocess.call([tfunilx, "SendFileCmd", fp.name]) # comment to disable printing
#with open('./files/CierreX.txt', 'w') as entrada:
#    print(entrada)
#subprocess.call([iobatch], shell=True)

    #subprocess.check_call(iobatch + entrada, shell=True)
    # subprocess.check_call(iobatch + args, stdin=entrada, stdout=False, stderr=None, shell=True)
    # def write_string_to_printer(string):
    #     fp = tempfile.NamedTemporaryFile(delete=False)
    #     fp.write(string.encode('latin1'))
    #     fp.close()
    #     #subprocess.call([iobatch,"-p host 192.168.3.69 -i CierreX.txt -o salida.txt" ], shell=True)
    #     #subprocess.call([iobatch, "SendFileCmd", fp.name]) # comment to disable printing
#subprocess.check_call(iobatch + args, shell=True)
#subprocess.check_call(iobatch + args, stdin=None, stdout=None, stderr=None, shell=True)
