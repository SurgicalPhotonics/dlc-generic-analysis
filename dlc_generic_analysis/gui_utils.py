from typing import List
from qtpy import QtWidgets


def open_files(
    obj: QtWidgets.QWidget, text: str, types_name: str = "Videos", file_types: List[str] = None
):
    if file_types is None:
        file_types = ["mp4", "avi", "m4v"]
    # Opens a directory using File Dialog
    file_types_str = types_name + " ("
    for ftype in file_types:
        file_types_str += "*." + ftype
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
