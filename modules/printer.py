import subprocess
import tempfile
import re

tfunilx = './tfunilx'


def remove_zero_width_space_chars(string):
    """Removes Zero Width Characters (\\u200b, \\u200c, \\u200d, \\uFEFF) from a string and return a new one."""
    str = []
    for char in string:
        ch = char.encode('ascii', 'backslashreplace')
        if ch not in [b'\\u200b', b'\\u200c', b'\\u200d', b'\\uFEFF']:
            str.append(ch.decode('unicode-escape'))

    return ''.join(str).encode('utf-8')


def write_string_to_printer(string):
    str = remove_zero_width_space_chars(string)
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(str)
    fp.close()
    subprocess.call(["cat", fp.name])
    # comment to disable printing
    subprocess.call([tfunilx, "SendFileCmd", fp.name])
