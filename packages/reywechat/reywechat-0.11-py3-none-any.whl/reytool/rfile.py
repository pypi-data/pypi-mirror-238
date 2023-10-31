# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-05-09 15:30:10
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : File methods.
"""


from typing import Any, List, Union, Literal, Optional, overload
from json import dumps as json_dumps, JSONDecodeError
from os import (
    walk as os_walk,
    listdir as os_listdir
)
from os.path import (
    abspath as os_abspath,
    join as os_join,
    isfile as os_isfile,
    isdir as os_isdir,
    basename as os_basename
)
from hashlib import md5 as hashlib_md5

from .rregular import search


__all__ = (
    "get_paths",
    "search_file",
    "read_file",
    "write_file"
)


def get_paths(folder: Optional[str] = None, target: Literal["all", "file", "folder"] = "all", recursion: bool = False) -> List:
    """
    Get the path of files and folders in the folder path.

    Parameters
    ----------
    folder : Folder path.
        - `None` : Work folder path.
        - `str` : Use this folder path.

    target : Target data.
        - `Literal['all']` : Return file and folder path.
        - `Literal['file']` : Return file path.
        - `Literal['folder']` : Return folder path.

    recursion : Is recursion directory.

    Returns
    -------
    String is path.
    """

    # Handle parameter.
    if folder is None:
        folder = ""
    folder_path = os_abspath(folder)

    # Get paths.
    paths = []

    ## Recursive.
    if recursion:
        obj_walk = os_walk(folder_path)
        if target == "all":
            targets_path = [
                os_join(path, file_name)
                for path, folders_name, files_name in obj_walk
                for file_name in files_name + folders_name
            ]
            paths.extend(targets_path)
        elif target == "file":
            targets_path = [
                os_join(path, file_name)
                for path, _, files_name in obj_walk
                for file_name in files_name
            ]
            paths.extend(targets_path)
        elif target in ("all", "folder"):
            targets_path = [
                os_join(path, folder_name)
                for path, folders_name, _ in obj_walk
                for folder_name in folders_name
            ]
            paths.extend(targets_path)

    ## Non recursive.
    else:
        names = os_listdir(folder_path)
        if target == "all":
            for name in names:
                target_path = os_join(folder_path, name)
                paths.append(target_path)
        elif target == "file":
            for name in names:
                target_path = os_join(folder_path, name)
                is_file = os_isfile(target_path)
                if is_file:
                    paths.append(target_path)
        elif target == "folder":
            for name in names:
                target_path = os_join(folder_path, name)
                is_dir = os_isdir(target_path)
                if is_dir:
                    paths.append(target_path)

    return paths


@overload
def search_file(
    pattern: str,
    folder: Optional[str] = None,
    recursion: bool = False,
    all_ : Literal[False] = False
) -> Optional[str]: ...

@overload
def search_file(
    pattern: str,
    folder: Optional[str] = None,
    recursion: bool = False,
    all_ : Literal[True] = False
) -> List[str]: ...

def search_file(
    pattern: str,
    folder: Optional[str] = None,
    recursion: bool = False,
    all_ : bool = False
) -> Optional[str]:
    """
    Search file by name.

    Parameters
    ----------
    pattern : Match file name pattern.
    folder : Folder path.
        - `None` : Work folder path.
        - `str` : Use this folder path.

    recursion : Is recursion directory.
    all_ : Whether return all match file path, otherwise return first match file path.

    Returns
    -------
    Match file path or null.
    """

    # Get paths.
    paths = get_paths(folder, "file", recursion)

    # All.
    if all_:
        match_paths = []
        for path in paths:
            file_name = os_basename(path)
            result = search(pattern, file_name)
            if result is not None:
                match_paths.append(path)
        return match_paths

    # First.
    else:
        for path in paths:
            file_name = os_basename(path)
            result = search(pattern, file_name)
            if result is not None:
                return path


@overload
def read_file(path: str, type_: Literal["bytes"] = "bytes") -> bytes: ...

@overload
def read_file(path: str, type_: Literal["str"] = "bytes") -> str: ...

def read_file(path: str, type_: Literal["str", "bytes"] = "bytes") -> Union[bytes, str]:
    """
    Read file data.

    Parameters
    ----------
    path : Read file path.
    type_ : File data type.
        - `Literal['bytes']` : Return file bytes data.
        - `Literal['str']` : Return file string data.

    Returns
    -------
    File bytes data or string data.
    """

    # Handle parameter.
    if type_ == "bytes":
        mode = "rb"
    elif type_ == "str":
        mode = "r"

    # Read.
    with open(path, mode) as file:
        content = file.read()

    return content


def write_file(path: str, data: Optional[Any] = "", append: bool = False) -> None:
    """
    Write file data.

    Parameters
    ----------
    path : Write File path. When path not exist, then cerate file.
    data : Write data.
        - `bytes` : File bytes data.
        - `str` : File text.
        - `Any` : Try.

    append : Whether append data, otherwise overwrite data.
    """

    # Handle parameter.

    ## Write mode.
    if append:
        mode = "a"
    else:
        mode = "w"
    if data.__class__ == bytes:
        mode += "b"

    ## Convert data to string.
    if data.__class__ not in (str, bytes):
        try:
            data = json_dumps(data, ensure_ascii=False)
        except (JSONDecodeError, TypeError):
            data = str(data)

    # Write.
    with open(path, mode) as file:
        file.write(data)


def get_md5(file: Union[str, bytes]) -> str:
    """
    Get file MD5.

    Parameters
    ----------
    file : File path or file bytes.

    Returns
    -------
    File MD5.
    """

    # Get bytes.

    ## Path.
    if file.__class__ == str:
        file_bytes = read_file(file)
    
    ## Bytes.
    elif file.__class__ == bytes:
        file_bytes = file

    # Calculate.
    hash = hashlib_md5(file_bytes)
    md5 = hash.hexdigest()

    return md5