"""Move files based on date."""
import argparse as arg
import os
import sys
import time
from pathlib import Path
import shutil

from pyfiglet import Figlet
from loguru import logger
from tqdm import tqdm
from mvdate import __version__

# Copyright 2023 Neil Shephard
#
# This file is part of mvdate.
#
# mvdate is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, version 3 of the License.
#
#
# mvdate is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with mvdate. If not, see
# <https://www.gnu.org/licenses/>.

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | <level>{message}</level>",
)
logger.add(
    sys.stderr,
    level="ERROR",
    format="<red>{time:YYYY-MM-DD HH:mm:ss.SSS}</red> | <level>{level:<8}</level> | <level>{message}</level>",
)


def create_parser() -> arg.ArgumentParser:
    """Create a parser for reading options"""
    parser = arg.ArgumentParser(description="Move files to directory structure based on files date.")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Installed version of mvdate : {__version__}",
        help="Report the current installed version of mvdate.",
    )
    parser.add_argument("-e", "--ext", dest="ext", required=False, default="jpg", help="File extension to search for.")
    parser.add_argument(
        "-b",
        "--base",
        dest="base",
        type=str,
        required=False,
        default="./",
        help="Base directory to search for files with extension type.",
    )
    parser.add_argument(
        "-d",
        "--destination",
        dest="dest",
        type=str,
        required=False,
        default="./",
        help="Destination directory to   move files to.",
    )
    parser.add_argument(
        "-l", "--log_file", dest="log_file", type=str, required=False, default=None, help="File to log output to."
    )
    parser.add_argument(
        "-n",
        "--nesting",
        dest="nesting",
        type=str,
        required=False,
        default="d",
        help="Structure of target directory, 'Y'ear, 'm'onth, 'd'ay, 'H'our, 'M'inutes.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        required=False,
        default=False,
        help="Execute quiet and supress all output.",
    )
    parser.add_argument(
        "-s",
        "--single",
        dest="single",
        required=False,
        default=False,
        help="Whether to have a single directory of the form 'YYYY-MM[-DD[-HH[-MM]]' rather than nesting.",
    )
    return parser


def find(base: str | Path = "./", ext: str = "jpg") -> list:
    """Find files of a given type.

    Parameters
    ----------
    base: str | Path
        Directory to search for files.
    ext: str
        File extension to search for.

    Returns
    -------

    """
    return list(Path(base).rglob(f"*.{ext}"))


def get_file_date(file: Path) -> time.struct_time:
    """Extract created date from file.

    Parameters
    ----------
    file: Path
        File to extract created date from.

    Returns
    float
        Returns the date as an elapsed float from origin.
    """
    try:
        return os.path.getmtime(file)
    except FileNotFoundError as fnfe:
        raise fnfe


def create_target_dir(destination: str | Path = "./") -> str:
    """Create the target directory.

    Parameters
    ----------
    base : str | Path
        Path where target directory structure is to be created.

    Returns
    -------
    None

    """
    Path(destination).mkdir(parents=True, exist_ok=True)


def extract_date_time(file_creation: time.struct_time, nesting: str = None, single: bool = False) -> str:
    """Extract date and time from a file creation date.

    Parameters
    ----------
    file_creation : time.struct_time
        Date and time of file creation.
    nesting : str
        Level of nesting to extract, values are 'Y'ear, 'm'onth, 'd'ay, 'H'our, 'M'inutes. Defaults to 'd'ay if not
        specified.
    single : bool
        Whether to make target directory a single rather than nested structure.

    Returns
    -------
    str
        Directory structure to create with given level of nesting.

    """
    local_file_creation = time.localtime(file_creation)
    sep = "-" if single else "/"
    if nesting == "Y":
        return time.strftime("%Y", local_file_creation)
    if nesting == "m":
        return time.strftime(f"%Y{sep}%m", local_file_creation)
    if nesting == "d":
        return time.strftime(f"%Y{sep}%m{sep}%d", local_file_creation)
    if nesting == "H":
        return time.strftime(f"%Y{sep}%m{sep}%d{sep}%H", local_file_creation)
    if nesting == "M":
        return time.strftime(f"%Y{sep}%m{sep}%d{sep}%H{sep}%m", local_file_creation)
    return time.strftime(f"%Y{sep}%m{sep}%d", local_file_creation)


def move_file(source: Path, destination: Path, quiet: bool = True) -> None:
    """Move a file

    Parameters
    ----------
    source : Path
        Path to the source file.
    destination : Path
        Destination directory.
    quiet : bool
        Suppress logging output.
    """
    source = Path(source)
    destination = Path(destination) / source.name
    try:
        shutil.move(source, destination)
        if quiet:
            logger.info(f"Moved : {source} -> {destination}")
    except FileNotFoundError as fnfe:
        raise fnfe


def main(args: arg.ArgumentParser = None) -> None:
    """Find and move files.

    Parameters
    ----------
    args: arg.ArgumentParser
        Arguments to run the function with.
    """
    parser = create_parser()
    args = parser.parse_args() if args is None else parser.parse_args(args)
    arguments = vars(args)
    # Find files
    files_to_move = find(base=Path(arguments["base"]), ext=arguments["ext"])
    if arguments["quiet"]:
        f = Figlet(font="slant")
        print(f.renderText("mvdate"))
        logger.info(f"Search directory                           : {arguments['base']}")
        logger.info(f"Searching for files with extension         : {arguments['ext']}")
        logger.info(f"Files found                                : {len(files_to_move)}")
    # Extract all file dates
    all_file_dates = [get_file_date(x) for x in list(files_to_move)]
    # Extract target directories, making a unique set
    all_target_dirs = [
        extract_date_time(x, nesting=arguments["nesting"], single=arguments["single"]) for x in all_file_dates
    ]
    target_dirs = set(all_target_dirs)
    # Create target directories
    [create_target_dir(x) for x in target_dirs]  # pylint: disable=expression-not-assigned
    # Move files
    for file_to_move, all_target_dir in tqdm(
        zip(list(files_to_move), all_target_dirs), desc=f"Moving {len(files_to_move)} files."
    ):
        move_file(Path(file_to_move), Path(all_target_dir), arguments["quiet"])
