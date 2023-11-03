import pathlib

import sh

from .base import print_step


def sub_zip(src_dir: pathlib.Path, target_zip_file, flag_absolute=False, is_remove_old=True):
    _p = pathlib.Path(target_zip_file)
    if _p.exists():
        if is_remove_old:
            _p.unlink()
        else:
            raise Exception(f"目标压缩文件已存在:{target_zip_file}")

    path_src_dir = pathlib.Path(src_dir)
    if not path_src_dir.exists():
        raise Exception(f"准备备份的路径不存在:{path_src_dir}")
    if not path_src_dir.is_dir():
        raise Exception(f"准备备份的路径不是文件夹:{path_src_dir}")

    cmd_zip = sh.Command("zip")
    if flag_absolute:
        cmd_zip_bake = cmd_zip.bake([
            "-r", str(target_zip_file), str(path_src_dir)
        ])
    else:
        src_dir_parent = path_src_dir.parent
        src_dir_name = path_src_dir.name
        cmd_zip_bake = cmd_zip.bake([
            "-r", str(target_zip_file), str(src_dir_name)
        ], _cwd=src_dir_parent)
    cmd_zip_bake_r = cmd_zip_bake()
    print_step(f"1.0 压缩文件\n{cmd_zip_bake_r}")
    return cmd_zip_bake_r