"""Database file path collector"""

import os
import sys
import shutil

sys.path.append("../")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dfcon.directory import Directory
from dfcon.path_filter import FileFilter, DircFilter, Filter


if __name__ == "__main__":
    if os.path.exists("test/out/exp1/ABCD"):
        shutil.rmtree("test/out/exp1/ABCD")
    if os.path.exists("test/out/out"):
        shutil.rmtree("test/out/out")
    os.mkdir("test/out/out")

    dirc = Directory(path="test/out/exp1").build_structure()

    print("################# EX1 #################\n")

    # example1
    file_filter = FileFilter().include_extention(["py", "txt"])
    dirc_filter = DircFilter().uncontained_path(["log", "data", ".git"])
    filters = Filter.overlap([file_filter, dirc_filter])

    results = dirc.get_file_path(filters=filters, serialize=True)
    all_dir_instances = dirc.get_instances(filters=None, serialize=True)
    terminal_dirs = dirc.get_terminal_instances(filters=None, serialize=True)

    for r in all_dir_instances:
        print(f"collect dirs: {r}")
    print()

    for r in terminal_dirs:
        print(f"collect term: {r}")
    print()

    for r in results:
        print(f"collect path: {r}")
    print()

    print("\n################# EX2 #################\n")

    # example2
    os.mkdir("test/out/exp1/ABCD")
    f = open("test/out/exp1/ABCD/exit.py", "w", encoding="utf-8")
    f.close()

    cloned = dirc.clone(filters=filters)

    os.remove("test/out/exp1/ABCD/exit.py")
    os.rmdir("test/out/exp1/ABCD")

    dirc.update_member(filters=filters)

    results = dirc.get_file_path(filters=None, serialize=True)
    for r in results:
        print(f"collect orgin: {r}")
    print()

    results = cloned.get_file_path(filters=None, serialize=True)
    for r in results:
        print(f"collect clone: {r}")
    print()

    print(
        "incarnated:", cloned.incarnate("test/out/out", filters=filters, printer=print)
    )

    cloned.destruct()

    print("\n################# EX3 #################\n")

    cloned = dirc.clone(filters=filters)
    cloned.update_dir_name(new_dir_name="exp2")
    print(
        "incarnated:", cloned.incarnate("test/out/out", filters=filters, printer=print)
    )

    cloned.destruct()
