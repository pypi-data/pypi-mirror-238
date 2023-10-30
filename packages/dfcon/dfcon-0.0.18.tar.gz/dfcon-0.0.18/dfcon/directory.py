"""Directory instance for database collector"""

from __future__ import annotations

import os
import re
import shutil
from typing import Any, Callable, List, Dict, Optional, Union
from tqdm import tqdm

from .filters import Filter, EmpFilter


class Directory:
    """This class is used to represent a directory in a database collector."""

    def __init__(self, path: str, empty: bool = False) -> None:
        if path == "":
            raise ValueError(
                "'path' must not be empty. If you wont to set current directory, set './' or '.'."
            )
        if re.match(r"[\\|/]", path[-1]):
            path = path[:-1]

        path = os.sep.join(re.split(r"[\\|/]", path))
        name = path.rsplit(os.sep, maxsplit=1)[-1]

        self.name = name
        self.path = path
        self.abspath = os.path.abspath(path)

        self.empty = empty

        self.file_member = []
        self.dirc_member = []
        self.terminal = True

    def __str__(self) -> str:
        return self.path

    def __eq__(self, __o: str) -> bool:
        if not isinstance(__o, str):
            raise NotImplementedError()
        else:
            return __o == self.name

    def __call__(self, path: str) -> Optional[Directory]:
        """Search the members of the hierarchy below this instance itself"""
        path_route = re.split(r"[\\|/]", path)
        if path_route[0] == ".":
            path_route = path_route[1:]

        if len(path_route) == 1:
            if path_route[0] == "":
                return self
            if path_route[0] in self.file_member:
                return self
            for dirc in self.dirc_member:
                if path_route[0] == dirc:
                    return dirc
            return None
        else:
            for dirc in self.dirc_member:
                if path_route[0] == dirc:
                    return dirc("/".join(path_route[1:]))
            return None

    def build_structure(self, filters: Optional[Filter] = None):
        """Generate & build directory structure"""

        self.update_member(filters, self.empty)

        return self

    def get_file_path(
        self, filters: Optional[Filter] = None, serialize: bool = False
    ) -> List[str]:
        """Get the path to the file matching the condition.

        Args:
            filters (Condition):
                The criteria of the file to be acquired are described.
            serialize (bool):
                Specifies how the directory list is returned.

        Returns:
            List[str]: file path list that match criteria.
        """
        file_list = []

        if filters is None:
            filters = EmpFilter()

        if not isinstance(filters, Filter):
            raise TypeError(
                "The argument 'filters' type must be 'Filter', "
                + f"but detect '{filters.__class__.__name__}'",
            )

        for file in self.file_member:
            if filters(file):
                out_form_path = "/".join(file.split(os.sep))
                file_list.append(out_form_path)

        for dirc in self.dirc_member:
            if serialize:
                file_list += dirc.get_file_path(filters, serialize=serialize)
            else:
                file_list.append(dirc.get_file_path(filters, serialize=serialize))

        return file_list

    def get_grouped_path_list(self, key: Callable[[str], str]) -> Dict[str, List[str]]:
        """Get grouped file path list with 'key'.

        Args:
            key (str): keyword for groping.

        Returns:
            Dict[List[str]]: grouped path list.
        """

        grouped = {}

        for mem in self.file_member:
            name = os.path.basename(mem)

            group = key(name)
            if not group in grouped:
                grouped[group] = [mem]
            else:
                grouped[group].append(mem)

        return grouped

    def get_terminal_instances(
        self, filters: Optional[Filter] = None, serialize: bool = False
    ) -> Union[List[Directory], List[Any]]:
        """Get the terminal Directory instance list while preserving file structure
        or Get the terminal Directory instance serialized list.

        Args:
            filters (Filter):
                Criteria. When `filters=None`, return all terminal instance.
            serialize (bool):
                Specifies how the directory list is returned.

        Returns:
            List[Directory]: The terminal Directory instance.
        """
        return self.get_instances(
            filters=filters, serialize=serialize, terminal_only=True
        )

    def get_instances(
        self,
        filters: Optional[Filter] = None,
        serialize: bool = False,
        terminal_only: bool = False,
    ) -> Union[List[Directory], List[Any]]:
        """Get the Directory instance list while preserving file structure
        or Get Directory instance serialized list.

        Args:
            filters (Filter):
                Criteria. When `filters=None`, return all instance.
            serialize (bool):
                When `serialize=True`, return-value 1d list.
            terminal_only (bool):
                When `terminal_only=True`, return only terminal instance.

        Returns:
            List[Directory]: The Directory instance.
        """
        dir_list = []

        if filters is None:
            filters = EmpFilter()
        elif not isinstance(filters, Filter):
            raise TypeError(
                "The argument 'filters' type must be 'Filter', "
                + f"but detect '{filters.__class__.__name__}'",
            )

        if self.terminal:
            if filters(self):
                return [self]
            else:
                return []

        for dirc in self.dirc_member:
            dir_list += dirc.get_instances(
                filters=filters, serialize=serialize, terminal_only=terminal_only
            )

        if not terminal_only and filters(self):
            if serialize:
                dir_list = [self] + dir_list
            else:
                dir_list = [self, dir_list]

        if serialize or not terminal_only:
            return dir_list
        else:
            return [dir_list]

    def get_specify_instance(self, path: str) -> Directory | None:
        """Get Directory instance which specified `path`.
        When file path specified as path, return its owner directory instance.
        Please exclude this directory's name from `path`.

        Args:
            path (str): Relative path from `self.path`

        Returns:
            Directory|None
        """
        if os.path.isfile(path):
            path = os.path.dirname(path)
        if path == "":
            return self

        dirc_list = re.split(r"[\\|/]", path)
        for direc in self.dirc_member:
            if direc == dirc_list[0]:
                if len(dirc_list) == 1:
                    return direc
                return direc.get_specify_instance(os.sep.join(dirc_list[1:]))
        return None

    def get_abspath(self) -> str:
        """get absolute path which is sep by '/'"""
        return "/".join(self.abspath.split(os.sep))

    def clone(self, filters: Optional[Filter] = None) -> Directory:
        """clone Directory instance structure (option: with condition

        Returns:
            Directory: cloned Directory instance with `filters`.
        """

        clone = Directory(self.path, self.empty)

        if filters is None:
            filters = EmpFilter()
        elif not isinstance(filters, Filter):
            raise TypeError(
                "The argument 'filters' type must be 'Filter', "
                + f"but detect '{filters.__class__.__name__}'",
            )

        clone.file_member = []
        for file in self.file_member:
            if filters(file):
                clone.file_member.append(file)
        clone.dirc_member = []
        for directory in self.dirc_member:
            if filters(str(directory)):
                clone.dirc_member.append(directory.clone(filters))
        clone.terminal = self.terminal

        return clone

    def incarnate(
        self,
        path: str,
        filters: Optional[Filter] = None,
        printer: Callable[[str], Any] = print,
    ) -> Directory:
        """
        Incarnating instance as an actual directory.
        If a `filters` is specified, the corresponding file will also be copied.

        Args:
            path (str):
                Target site for incarnation.
            filters (Filter):
                Criteria for incarnation.
            printer (Callable[[str], Any]):
                To print log. When `printer=None`, log can't be output.

        Returns
            Directory: incarnated directory instance.
        """
        if printer is None:

            def no_wark(_):
                pass

            printer = no_wark

        path = os.sep.join(path.split("/"))

        mk_num = self.sub_incarnate(path, filters, printer)
        if printer is not None:
            printer("made " + str(mk_num) + " files.")

        return Directory(path=os.path.join(path, self.name)).build_structure()

    def sub_incarnate(
        self,
        path: str,
        filters: Optional[Filter] = None,
        printer: Callable[[str], Any] = print,
    ) -> int:
        """Sub function for incarnate."""

        if filters is None:
            filters = EmpFilter()
        elif not isinstance(filters, Filter):
            raise TypeError(
                "The argument 'filters' type must be 'Filter', "
                + f"but detect '{filters.__class__.__name__}'",
            )

        mk_number = 0

        mk_path = os.path.join(path, self.name)
        if not os.path.isdir(mk_path):
            os.mkdir(mk_path)
            mk_number += 1

        self.copy_file(mk_path, filters, printer)

        for dirc in self.dirc_member:
            if filters(dirc):
                mk_number += dirc.sub_incarnate(mk_path, filters, printer)

        return mk_number

    def hollow(self) -> Directory:
        """clone instance & remove its file member"""

        target = self.clone()
        target.file_member = []
        for children in target.dirc_member:
            children.hollow()

        return target

    def update_member(self, filters: Optional[Filter] = None, empty: bool = False):
        """update directory member"""

        if filters is None:
            filters = EmpFilter()
        elif not isinstance(filters, Filter):
            raise TypeError(
                "The argument 'filters' type must be 'Filter', "
                + f"but detect '{filters.__class__.__name__}'",
            )

        list_member = os.listdir(self.path)
        dirc_member = []
        file_member = []
        for member in list_member:
            fpath = os.path.join(self.path, member)
            if not filters(fpath):
                continue
            if os.path.isfile(fpath) and not empty:
                file_member.append(fpath)
            else:
                dirc_member.append(member)

        self.destruct()

        file_member = sorted(file_member)
        dirc_member = sorted(dirc_member)

        self.dirc_member = [
            Directory(os.path.join(self.path, dirc_name), empty)
            for dirc_name in dirc_member
        ]
        self.file_member = file_member

        self.terminal = len(dirc_member) == 0
        for dirc in self.dirc_member:
            dirc.update_member(filters, empty)

    def update_dir_name(self, new_dir_name: str):
        """Update Directory's Name

        Args:
            new_dir_name (str):
                New name of directory.

        Returns:
            Directory: Updated Directory instance.
        """

        if re.match(r"[\\|/]", self.path[-1]):
            self.path = self.path[:-1]

        self.name = new_dir_name

        split_path = re.split(r"[\\|/]", self.path)
        split_path[:-1].append(self.name)
        self.path = os.sep.join(split_path)

        for direc in self.dirc_member:
            direc.sub_update_dir_name(self.path)

        new_file_member = []
        for file_path in self.file_member:
            filename = os.path.basename(file_path)
            new_file_member.append(os.path.join(self.path, filename))

        self.file_member = new_file_member

        return self

    def sub_update_dir_name(self, parent_path: str):
        """Sub function for update_dir_name."""
        split_path = re.split(r"[\\|/]", parent_path)
        split_path.append(self.name)
        self.path = os.sep.join(split_path)

        for direc in self.dirc_member:
            direc.sub_update_dir_name(self.path)

        new_file_member = []
        for file_path in self.file_member:
            filename = os.path.basename(file_path)
            new_file_member.append(os.path.join(self.path, filename))

        self.file_member = new_file_member

    def remove_member(
        self,
        filters: Optional[Filter] = None,
        printer: Callable[[str], Any] = print,
    ) -> int:
        """Remove file members

        Args:
            filters (Filter, optional):
                File remove conditons. Defaults to None.
            printer (Callable[[str], Any], optional):
                Output stream.
                When printer is None, output stream is stoped. Defaults to `print`.

        Returns:
            int: Removed file member num.
        """
        if printer is None:

            def no_wark(_):
                pass

            printer = no_wark

        remove_files = self.get_file_path(filters=filters, serialize=True)
        for file in remove_files:
            printer(f"remove: {file}")
            os.remove(file)

        self.update_member()

        return len(remove_files)

    def destruct(self) -> None:
        """Destruct members"""

        if self.terminal:
            return

        for dirc_obj in self.dirc_member:
            dirc_obj.destruct()
            del dirc_obj

        return

    def copy_file(
        self,
        path: str,
        filters: Optional[Filter] = None,
        printer: Callable[[str], Any] = print,
        override: bool = False,
        tqdm_progress: bool = False,
    ):
        """copy member files to path (option: with `filters` for criteria)

        Args:
            path (str):
                Path for copy site.
            filters (Filter, optional):
                Criteria for copy. Defaults to None.
            printer (Callable[[str], Any], optional):
                When `printer=None`, output stream is stopped. Defaults to print.
            override (bool, optional):
                Flag whether or not to overwrite existing files. Defaults to False.
        """

        path = os.sep.join(path.split("/"))

        if filters is None:
            filters = EmpFilter()
        elif not isinstance(filters, Filter):
            raise TypeError(
                "The argument 'filters' type must be 'Filter', "
                + f"but detect '{filters.__class__.__name__}'",
            )

        if tqdm_progress:
            loop_iter = tqdm(self.file_member, desc="copying ... ")
        else:
            loop_iter = self.file_member

        for file in loop_iter:
            file_path = "/".join(file.split(os.sep))
            file_name = os.path.basename(file_path)
            target_path = "/".join([path, file_name])

            if filters(file):
                if not os.path.isfile(target_path) or override:
                    shutil.copyfile(file_path, target_path)
                    if printer is not None:
                        if os.path.isfile(target_path) and override:
                            printer(f"ovrd: {file_path} -> {target_path}")
                        else:
                            printer(f"copy: {file_path} -> {target_path}")
                elif printer is not None:
                    printer(f"exst: {file_path} -> {target_path}")

    def copy_files(
        self,
        path: str,
        filters: Optional[Filter] = None,
        printer: Callable[[str], Any] = print,
        override: bool = False,
        tqdm_progress: bool = False,
    ):
        """copy member files in directory & child directorys to path
        (option: with `filters` for criteria)

        Args:
            path (str):
                Path for copy site.
            filters (Filter, optional):
                Criteria for copy. Defaults to None.
            printer (Callable[[str], Any], optional):
                When `printer=None`, output stream is stopped. Defaults to print.
            override (bool, optional):
                Flag whether or not to overwrite existing files. Defaults to False.
        """

        if re.match(r"[\\|/]", path[-1]):
            path = path[:-1]
        path = os.sep.join(re.split(r"[\\|/]", path))

        files = self.get_file_path(filters, serialize=True)

        if tqdm_progress:
            loop_iter = tqdm(files, desc="copying ... ")
        else:
            loop_iter = files

        for file_path in loop_iter:
            target_path = os.path.join(path, os.path.basename(file_path))
            if not os.path.isfile(target_path) or override:
                shutil.copyfile(file_path, target_path)
                if printer is not None:
                    if os.path.isfile(target_path) and override:
                        printer(f"ovrd: {file_path} -> {target_path}")
                    else:
                        printer(f"copy: {file_path} -> {target_path}")
            elif printer is not None:
                printer(f"exst: {file_path} -> {target_path}")
