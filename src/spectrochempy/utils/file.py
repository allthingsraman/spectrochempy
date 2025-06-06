# ======================================================================================
# Copyright (©) 2015-2025 LCS - Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory.
# ======================================================================================
"""File utilities."""

import importlib.util
import re
import struct
import warnings
from os import environ
from pathlib import Path
from pathlib import PosixPath
from pathlib import WindowsPath

import numpy as np

# ======================================================================================
# API utilities
# ======================================================================================
# When a function is in __all__, it is imported in the API
__all__ = ["pathclean"]


# region api
def pathclean(paths):
    """
    Clean a path or a series of path.

    The aim is to be compatible with windows and unix-based system.

    Parameters
    ----------
    paths :  `str` or a `list` of `str`
        Path to clean. It may contain Windows or conventional python separators.

    Returns
    -------
    pathlib or list of pathlib
        Cleaned path(s).
    """
    import platform

    def is_windows():
        return "Windows" in platform.platform()

    def _clean(path):
        if isinstance(path, (Path, PosixPath, WindowsPath)):  # noqa: UP038  (syntax error in pyfakefs with modern union operators)
            path = path.name
        if is_windows():
            path = WindowsPath(path)  # pragma: no cover
        else:  # some replacement so we can handle window style path on unix
            path = path.strip()
            path = path.replace("\\", "/")
            path = path.replace("\n", "/n")
            path = path.replace("\t", "/t")
            path = path.replace("\b", "/b")
            path = path.replace("\a", "/a")
            path = PosixPath(path)
        return Path(path)

    if paths is not None:
        if isinstance(paths, (str, Path, PosixPath, WindowsPath)):  # noqa: UP038
            path = str(paths)
            return _clean(path).expanduser()
        if isinstance(paths, (list, tuple)):  # noqa: UP038
            return [_clean(p).expanduser() if isinstance(p, str) else p for p in paths]

    return paths


# endregion api


# ======================================================================================
# Utility functions
# ======================================================================================


# region utility
def is_editable_install(package_name):
    """
    Check if a package is installed in editable mode.

    Parameters
    ----------
    package_name : str
        The name of the package to check.

    Returns
    -------
    bool
        True if the package is installed in editable mode, False otherwise.
    """
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return False
    print("origin", spec.origin)  # noqa: T201
    return f"{package_name}/src" in spec.origin


def get_repo_path():
    """
    Get the repository path based on the installation mode.

    Returns
    -------
    Path
        The path to the repository.
    """
    if is_editable_install("spectrochempy"):
        return Path(__file__).parent.parent.parent.parent
    return Path(__file__).parent.parent


def fromfile(fid, dtype, count):
    # to replace np.fromfile in case of io.BytesIO object instead of byte
    # object
    t = {
        "uint8": "B",
        "int8": "b",
        "uint16": "H",
        "int16": "h",
        "uint32": "I",
        "int32": "i",
        "float32": "f",
        "char8": "c",
    }
    typ = t[dtype] * count
    if dtype.endswith("16"):
        count *= 2
    elif dtype.endswith("32"):
        count *= 4

    out = struct.unpack(typ, fid.read(count))
    if len(out) == 1:
        return out[0]
    return np.array(out)


def _insensitive_case_glob(pattern):
    def either(c):
        return f"[{c.lower()}{c.upper()}]" if c.isalpha() else c

    return "".join(map(either, pattern))


def patterns(filetypes, allcase=True):
    regex = r"\*\.*\[*[0-9-]*\]*\w*\**"
    patterns = []
    if not isinstance(filetypes, (list, tuple)):  # noqa: UP038
        filetypes = [filetypes]
    for ft in filetypes:
        m = re.finditer(regex, ft)
        patterns.extend([match.group(0) for match in m])
    if not allcase:
        return patterns
    return [_insensitive_case_glob(p) for p in patterns]


def _get_file_for_protocol(f, **kwargs):
    protocol = kwargs.get("protocol")
    if protocol is not None:
        if isinstance(protocol, str):
            if protocol in ["ALL"]:
                protocol = "*"
            if protocol in ["opus"]:
                protocol = "*.0*"
            protocol = [protocol]

        lst = []
        for p in protocol:
            lst.extend(list(f.parent.glob(f"{f.stem}.{p}")))
        if not lst:
            return None
        return f.parent / lst[0]
    return None


def check_filenames(*args, **kwargs):
    """
    Return a list or a dictionary of filenames.

    Parameters
    ----------
    *args
        If passed it is a str, a list of str or a dictionary containing filenames or a byte's contents.
    **kwargs
        Optional keywords parameters. See Other parameters

    Other Parameters
    ----------------
    filename :
    filetypes :
    content :
    protocol :
    processed :
    expno :
    procno :
    iterdir :
    glob :

    See Also
    --------
    check_filename_to_open
    check_filename_to_save
    """
    # from spectrochempy.application.application import info_
    from spectrochempy.application.preferences import preferences as prefs

    datadir = pathclean(prefs.datadir)

    filenames = None

    if args:
        if (
            isinstance(args[0], str)
            and (args[0].startswith("http://") or args[0].startswith("https://"))
            # and kwargs.get("remote")
        ):
            # return url
            return args
        if isinstance(args[0], (str, Path, PosixPath, WindowsPath)):  # noqa: UP038
            # one or several filenames are passed - make Path objects
            filenames = pathclean(args)
        elif isinstance(args[0], bytes):
            # in this case, one or several byte contents has been passed instead of filenames
            # as filename where not given we passed the 'unnamed' string
            # return a dictionary
            return {pathclean(f"no_name_{i}"): arg for i, arg in enumerate(args)}
        elif isinstance(args[0], (list, tuple)) and (  # noqa: UP038
            isinstance(  # noqa: UP038
                args[0][0], (str, Path, PosixPath, WindowsPath)
            )
        ):
            filenames = pathclean(args[0])
        elif isinstance(args[0], list) and isinstance(args[0][0], bytes):
            return {pathclean(f"no_name_{i}"): arg for i, arg in enumerate(args[0])}
        elif isinstance(args[0], dict):
            # return directly the dictionary
            return args[0]

    if not filenames:
        # look into keywords (only the case where a str or pathlib filename is given are
        # accepted)
        filenames = kwargs.pop("filename", None)
        filenames = [pathclean(filenames)] if pathclean(filenames) is not None else None

    # Look for content in kwargs
    content = kwargs.pop("content", None)
    if content:
        if not filenames:
            filenames = [pathclean("no_name")]
        return {filenames[0]: content}

    if not filenames:
        # no filename specified open a dialog
        filetypes = kwargs.pop("filetypes", ["all files (*)"])
        directory = pathclean(kwargs.pop("directory", None))
        filenames = get_filenames(
            directory=directory,
            dictionary=True,
            filetypes=filetypes,
            **kwargs,
        )
    if filenames and not isinstance(filenames, dict):
        filenames_ = []
        for filename in filenames:
            # in which directory ?
            directory = filename.parent

            if directory.resolve() == Path.cwd() or directory == Path():
                directory = ""
            kw_directory = pathclean(kwargs.get("directory"))
            if directory and kw_directory and directory != kw_directory:
                # conflict we do not take into account the kw.
                warnings.warn(
                    "Two different directory where specified (from args and keywords arg). "
                    "Keyword `directory` will be ignored!",
                    stacklevel=2,
                )
            elif not directory and kw_directory:
                filename = pathclean(kw_directory / filename)

            # check if the file exists here
            if not directory or str(directory).startswith("."):
                # search first in the current directory
                directory = Path.cwd()

            f = pathclean(directory / filename)

            fexist = f if f.exists() else _get_file_for_protocol(f, **kwargs)
            # info_(f"fexist  {fexist}")
            if fexist is None:
                f = pathclean(datadir / filename)
                # info_(f"f (line 255) {f}")
                fexist = f if f.exists() else _get_file_for_protocol(f, **kwargs)
                # info_(f"fexist  {fexist}")

            if fexist:
                filename = fexist

            # Particular case for topspin where filename can be provided
            # as a directory only
            if filename.is_dir() and "topspin" in kwargs.get("protocol", []):
                filename = _topspin_check_filename(filename, **kwargs)

            if not isinstance(filename, list):
                filename = [filename]

            filenames_.extend(filename)

        filenames = filenames_

    return filenames


def _topspin_check_filename(filename, **kwargs):
    if kwargs.get("iterdir", False) or kwargs.get("glob") is not None:
        # when we list topspin dataset we have to read directories, not directly files
        # we can retrieve them using glob patterns
        glob = kwargs.get("glob")
        if glob:
            files_ = list(filename.glob(glob))
        elif not kwargs.get("processed", False):
            files_ = list(filename.glob("**/ser"))
            files_.extend(list(filename.glob("**/fid")))
        else:
            files_ = list(filename.glob("**/1r"))
            files_.extend(list(filename.glob("**/2rr")))
            files_.extend(list(filename.glob("**/3rrr")))
    else:
        expno = kwargs.pop("expno", None)
        procno = kwargs.pop("procno", None)

        if expno is None:
            expnos = sorted(filename.glob("[0-9]*"))
            expno = expnos[0] if expnos else expno

        # read a fid or a ser
        if procno is None:
            f = filename / str(expno)
            files_ = [f / "ser"] if (f / "ser").exists() else [f / "fid"]

        else:
            # get the adsorption spectrum
            f = filename / str(expno) / "pdata" / str(procno)
            if (f / "3rrr").exists():
                files_ = [f / "3rrr"]
            elif (f / "2rr").exists():
                files_ = [f / "2rr"]
            else:
                files_ = [f / "1r"]

    # depending on the glob patterns too many files may have been selected : restriction to the valid subset
    filename = []
    for item in files_:
        if item.name in ["fid", "ser", "1r", "2rr", "3rrr"]:
            filename.append(item)

    return filename


def get_filenames(*filenames, **kwargs):
    """
    Return a list or dictionary of the filenames of existing files, filtered by extensions.

    Parameters
    ----------
    filenames : `str` or pathlib object, `tuple` or `list` of strings of pathlib object, optional.
        A filename or a list of filenames.
        If not provided, a dialog box is opened to select files in the current
        directory if no `directory` is specified).
    **kwargs
        Other optional keyword parameters. See Other Parameters.

    Returns
    -------
    out
        List of filenames.

    Other Parameters
    ----------------
    directory : `str` or pathlib object, optional.
        The directory where to look at. If not specified, read in
        current directory, or in the datadir if unsuccessful.
    filetypes : `list` , optional, default=['all files, '.*)'].
        File type filter.
    dictionary : `bool` , optional, default=True
        Whether a dictionary or a list should be returned.
    iterdir : bool, default=False
        Read all file (possibly limited by `filetypes` in a given `directory` .
    recursive : bool, optional,  default=False.
        Read also subfolders.

    Warnings
    --------
    if several filenames are provided in the arguments,
    they must all reside in the same directory!
    """
    from spectrochempy.application.preferences import preferences as prefs

    # allowed filetypes
    # -----------------
    # alias filetypes and filters as both can be used
    filetypes = kwargs.get("filetypes", kwargs.get("filters", ["all files (*)"]))

    # filenames
    # ---------
    if len(filenames) == 1 and isinstance(filenames[0], (list, tuple)):  # noqa: UP038
        filenames = filenames[0]

    filenames = pathclean(list(filenames))

    directory = None
    if len(filenames) == 1:
        # check if it is a directory
        try:
            f = get_directory_name(filenames[0])
        except OSError:
            f = None
        if f and f.is_dir():
            # this specify a directory not a filename
            directory = f
            filenames = None
    # else:
    #    filenames = pathclean(list(filenames))

    # directory
    # ---------
    kw_dir = pathclean(kwargs.pop("directory", None))
    if directory is None:
        directory = kw_dir

    if directory is not None:
        if filenames:
            # prepend to the filename (incompatibility between filename and directory specification
            # will result to a error
            filenames = [pathclean(directory / filename) for filename in filenames]
        else:
            directory = get_directory_name(directory)

    # check the parent directory
    # all filenames must reside in the same directory
    if filenames:
        parents = set()
        for f in filenames:
            parents.add(f.parent)
        if len(parents) > 1:
            raise ValueError(
                "filenames provided have not the same parent directory. "
                "This is not accepted by the read function.",
            )

        # use get_directory_name to complete eventual missing part of the absolute path
        directory = get_directory_name(parents.pop())

        filenames = [filename.name for filename in filenames]

    # now proceed with the filenames
    if filenames:
        # look if all the filename exists either in the specified directory,
        # else in the current directory, and finally in the default preference data directory
        temp = []
        for _i, filename in enumerate(filenames):
            if not (pathclean(directory / filename)).exists():
                # the filename provided doesn't exists in the working directory
                # try in the data directory
                directory = pathclean(prefs.datadir)
                if not (pathclean(directory / filename)).exists():
                    raise OSError(f"Can't find  this filename {filename}")
            temp.append(directory / filename)

        # now we have checked all the filename with their correct location
        filenames = temp

    else:
        # no filenames:
        # open a file dialog    # TODO: revise this as we have suppressed the dialogs
        # except if a directory is specified or iterdir is True.

        getdir = kwargs.get(
            "iterdir",
            directory is not None or kwargs.get("protocol") == ["topspin"],
            # or kwargs.get("protocol", None) == ["carroucell"],
        )

        if not getdir:
            # we open a dialog to select one or several files manually
            if environ.get("TEST_FILE", None) is not None:
                # happen for testing
                filenames = [prefs.datadir / environ.get("TEST_FILE")]

        else:
            if not directory:
                directory = get_directory_name(environ.get("TEST_FOLDER"))

            elif kwargs.get("protocol") == ["topspin"]:
                directory = get_directory_name(environ.get("TEST_NMR_FOLDER"))

            if directory is None:
                return None

            filenames = []

            if kwargs.get("protocol") != ["topspin"]:
                # automatic reading of the whole directory
                fil = []
                for pat in patterns(filetypes):
                    if kwargs.get("recursive", False):
                        pat = f"**/{pat}"
                    fil.extend(list(directory.glob(pat)))
                pattern = kwargs.get("pattern", ["*"])
                pattern = pattern if isinstance(pattern, list) else [pattern]
                for kw_pat in pattern:
                    kw_pat = _insensitive_case_glob(kw_pat)
                    if kwargs.get("recursive", False):
                        kw_pat = f"**/{kw_pat}"
                    fil2 = [f for f in list(directory.glob(kw_pat)) if f in fil]
                    filenames.extend(fil2)
            else:
                # Topspin directory detection
                filenames = [directory]

            # on mac case insensitive OS this cause doubling the number of files.
            # Eliminates doublons:
            filenames = list(set(filenames))
            filenames = [
                f for f in filenames if f.name not in [".DS_Store", "__index__"]
            ]
            filenames = pathclean(filenames)

        if not filenames:
            # problem with reading?
            return None

    # now we have either a list of the selected files
    if isinstance(filenames, list) and not all(
        isinstance(elem, (Path, PosixPath, WindowsPath))  # noqa: UP038
        for elem in filenames  # noqa: UP038
    ):
        raise OSError("one of the list elements is not a filename!")

    # or a single filename
    if isinstance(filenames, (str, Path, PosixPath, WindowsPath)):  # noqa: UP038
        filenames = [filenames]

    filenames = pathclean(filenames)
    for filename in filenames[:]:
        if filename.name.endswith(".DS_Store"):
            # sometime present in the directory (MacOSX)
            filenames.remove(filename)

    dictionary = kwargs.get("dictionary", True)
    protocol = kwargs.get("protocol")
    if dictionary and protocol != ["topspin"]:
        # make and return a dictionary
        filenames_dict = {}
        for filename in filenames:
            if filename.is_dir() and protocol != ["carroucell"]:
                continue
            extension = filename.suffix.lower()
            if not extension:
                if re.match(r"^fid$|^ser$|^[1-3][ri]*$", filename.name) is not None:
                    extension = ".topspin"
            elif extension[1:].isdigit():
                # probably an opus file
                extension = ".opus"
            if extension in filenames_dict:
                filenames_dict[extension].append(filename)
            else:
                filenames_dict[extension] = [filename]
        return filenames_dict
    return filenames


def find_or_create_spectrochempy_dir():
    directory = Path.home() / ".spectrochempy"

    directory.mkdir(exist_ok=True)  # Create directory only if it does not exist

    if directory.is_file():  # pragma: no cover
        msg = "Intended SpectroChemPy directory `{0}` is actually a file."
        raise OSError(msg.format(directory))

    return directory


def get_directory_name(directory, **kwargs):
    """
    Return a valid directory name.

    Parameters
    ----------
    directory : `str` or `pathlib.Path` object, optional.
        A directory name. If not provided, a dialog box is opened to select a directory.

    Returns
    -------
    out: `pathlib.Path` object
        valid directory name.

    """
    from spectrochempy.application.application import warning_
    from spectrochempy.application.preferences import preferences as prefs

    data_dir = pathclean(prefs.datadir)
    working_dir = Path.cwd()

    directory = pathclean(directory)

    if directory:
        # Search locally
        if directory.is_dir():
            # nothing else to do
            return directory

        if (working_dir / directory).is_dir():
            # if no parent directory: look at current working dir
            return working_dir / directory

        if (data_dir / directory).is_dir():
            return data_dir / directory

        raise OSError(f'"{directory!s}" is not a valid directory')

    warning_("No directory provided!")
    return None


def check_filename_to_save(dataset, filename=None, overwrite=False, **kwargs):
    from spectrochempy.application.application import info_

    filename = pathclean(filename)

    if filename and pathclean(filename).parent.resolve() == Path.cwd():
        filename = Path.cwd() / filename

    if not filename or overwrite or filename.exists():
        # no filename provided
        if filename is None or pathclean(filename).is_dir():
            filename = dataset.name
            filename = pathclean(filename).with_suffix(kwargs.get("suffix", ".scp"))

        # existing filename provided
        if filename.exists():
            if overwrite:
                info_(f"A file {filename} is already present and will be overwritten.")
            else:
                raise FileExistsError(
                    f"A file {filename} is already present. "
                    "Please use the `overwrite=True` flag to overwrite it."
                )

    return pathclean(filename)


def check_filename_to_open(*args, **kwargs):
    # Check the args and keywords arg to determine the correct filename

    filenames = check_filenames(*args, **kwargs)

    if filenames is None:  # not args and
        # this is probably due to a cancel action for an open dialog.
        return None

    if not isinstance(filenames, dict):
        if len(filenames) == 1 and filenames[0] is None:
            raise (FileNotFoundError)

        # deal with some specific cases
        if isinstance(filenames[0], Path):
            # all filename should be Path, except case of urls
            key = filenames[0].suffix.lower()
        elif filenames[0].startswith("http://") or filenames[0].startswith("https://"):
            key = pathclean(filenames[0]).suffix.lower()

        if (
            not key
            and re.match(r"^fid$|^ser$|^[1-3][ri]*$", filenames[0].name) is not None
        ):
            key = ".topspin"
        if key[1:].isdigit():
            # probably an opus file
            key = ".opus"
        return {key: filenames}

    if len(args) > 0 and args[0] is not None:
        # args where passed so in this case we have directly byte contents instead of filenames only
        contents = filenames
        return {"frombytes": contents}

    # probably no args (which means that we are coming from a dialog or from a full list of a directory
    return filenames


# endregion utility
