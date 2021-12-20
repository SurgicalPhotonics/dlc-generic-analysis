from typing import List
from qtpy import QtWidgets


def open_files(
    obj: QtWidgets.QWidget, text: str, types_name: str = "Videos", file_types: List[str] = None
):
    if file_types is None:
        file_types = ["mp4", "avi", "m4v"]
    file_types_str = types_name + " ("
    for f_type in file_types:
        file_types_str += "*." + f_type + " "
    file_types_str += ");; @All Files (*)"
    files, _ = QtWidgets.QFileDialog.getOpenFileNames(
        obj,
        text,
        "",
        file_types_str,
        options=QtWidgets.QFileDialog.Options(),
    )
    return files


def open_dir(obj: QtWidgets.QWidget, text):
    files_dir, _ = QtWidgets.QFileDialog.getExistingDirectory(
        obj,
        text,
    )
    return files_dir
