
from os import path
from ness.report import NessusReport


def from_file(path_str):

    full_path = path.abspath(path_str)
    if not path.exists(full_path):
        raise FileNotFoundError(full_path)

    with open(full_path) as f_conn:
        content = f_conn.read()
        return NessusReport.from_string(content)
