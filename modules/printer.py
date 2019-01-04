import subprocess
import tempfile

tfunilx = './tfunilx'

def write_string_to_printer(string):
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(string.encode('latin1'))
    fp.close()
    subprocess.call(["cat", fp.name])
    # subprocess.call([tfunilx, "SendFileCmd", fp.name]) # comment to disable printing
