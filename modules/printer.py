import subprocess
import tempfile
import logging

tfunilx = './tfunilx'


def write_string_to_printer(string):
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(string.encode('latin1'))
    fp.close()
    subprocess.call(["cat", fp.name])
    # comment to disable printing
    subprocess.call([tfunilx, "SendFileCmd", fp.name])
