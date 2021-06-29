import subprocess
import tempfile

tfunilx = './tfunilx'


def write_string_to_printer(string):
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(string.encode('latin1'))
    fp.close()
    print('cat ----------------------------')
    subprocess.run(["cat", fp.name])
    # comment to disable printing
    check = subprocess.run([tfunilx, "ReadFpStatus"], capture_output=True)
    last = subprocess.run([tfunilx, "S1"], capture_output=True)
    print(check.stdout)
    print(last.stdout)

    process = subprocess.run(
        [tfunilx, "SendFileCmd", fp.name], capture_output=True)
    print(process.stdout)
