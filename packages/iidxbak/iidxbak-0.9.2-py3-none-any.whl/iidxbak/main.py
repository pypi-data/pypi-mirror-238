import os
import sys
import pathlib
import json
from datetime import datetime

import click
import sh
import oss2

from .base import _exec, gen_tmp_key, enc_data_file, enc_tmp_key
from .conf import get_default_iidxbak_home_conf_dir, ensure_home_path
from .core_zip import sub_zip


@click.command()
@click.option("--conf", default="", help="使用配置文件")
@click.option("--dir_to_bak", help="准备备份的目录")
@click.option("--work_dir", default="", help="工作目录")
@click.option("--conf_dir", default="", help="配置目录")
def main_detail(conf, dir_to_bak, work_dir, conf_dir):
    if len(sys.argv) == 1:
        click.echo(click.style("实例如下：", fg="blue"))

    if conf:
        cwd = os.getcwd()
        click.echo(click.style(f"当前工作目录：{cwd}:{type(conf) is str}"))
        click.echo(click.style(f"使用配置文件：{conf}", fg="green"))
        return
    _home = pathlib.Path().home()

    if not conf_dir:
        conf_dir = _home / ".iidxbak" / "conf"
        conf_dir.mkdir(parents=True,exist_ok=True)
    else:
        conf_dir = pathlib.Path(conf_dir)

    if not work_dir:
        work_dir = _home / ".iidxbak" / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
    else:
        work_dir = pathlib.Path(work_dir)

    # TODO: 1. 检查公钥存不存在

    # 1. zip
    sub_zip(dir_to_bak, work_dir / "bak.zip")

    # 2. gen_tmp_key


@click.command()
@click.option("--dir_to_bak", help="准备备份的目录")
@click.option("--conf", default="", help="加载的配置目录")
@click.option("--work_dir_mid_str", default="", help="")
def main(dir_to_bak, conf, work_dir_mid_str):
    if conf:
        conf = pathlib.Path(conf)
    else:
        conf = get_default_iidxbak_home_conf_dir() / "iidxbak.json"
    if not conf.exists():
        raise Exception(f"配置文件不存在：{conf}")

    work_dir_mid_str = work_dir_mid_str or datetime.now().strftime("%Y%m%d-%H%M")

    conf_item_public_key = ""
    conf_item_work_dir = ""
    conf_item_node_info = False

    oss_ak_id = ""
    oss_ak_secret = ""
    oss_ep = ""
    oss_bucket_name = ""

    with open(conf, mode="r") as conf_fp:
        conf_map = json.load(conf_fp)
        conf_item_public_key = conf_map.get("public_key", None)
        if not conf_item_public_key:
            print(conf_map)
            raise Exception(f"配置错误：配置项不存在public_key:{conf_item_public_key}")
        conf_item_work_dir = conf_map.get("work_dir", None)
        if not conf_item_work_dir:
            print(conf_map)
            raise Exception(f"配置错误：配置项不存在public_key:{conf_item_public_key}")
        conf_item_node_info = conf_map.get("i_node_info", False)
        conf_item_node_info = not not conf_item_node_info

        oss_ak_id = conf_map.get("oss_ak_id", "")
        oss_ak_secret = conf_map.get("oss_ak_secret", "")
        oss_ep = conf_map.get("oss_ep", "")
        oss_bucket_name = conf_map.get("oss_bucket_name", "")

    public_key_path = ensure_home_path(conf_item_public_key)
    if not public_key_path.exists():
        raise Exception(f"公钥不存在：{public_key_path}")

    work_dir_conf = ensure_home_path(conf_item_work_dir)
    if not work_dir_conf.exists():
        work_dir_conf.mkdir(parents=True, exist_ok=True)

    work_dir = work_dir_conf / work_dir_mid_str
    work_dir.mkdir(parents=True, exist_ok=True)

    # 1. 压缩
    data_file_raw = work_dir / f"bak.zip.raw"
    data_file_enc = f"{data_file_raw}.enc"
    tmp_key_raw = work_dir / f"bak.zip.tmp.key.raw"
    tmp_key_enc = f"{tmp_key_raw}.enc"

    zip_r = sub_zip(dir_to_bak, data_file_raw)

    # 2. 生成临时key
    # 临时对称加密key， 执行结果
    gen_key_r = gen_tmp_key(tmp_key_raw)
    enc_key_r = enc_tmp_key(public_key_path, tmp_key_raw, tmp_key_enc)

    # 3. 对称加密备份文件
    # 加密的文件路径，执行命令结果
    encdata_r = enc_data_file(data_file_raw, tmp_key_raw, data_file_enc)

    # 4. 备份enc
    data_file_raw.unlink()
    tmp_key_raw.unlink()

    final_zip = f"bak.{work_dir_mid_str}.zip"
    if conf_item_node_info:
        node_info_str = os.uname().nodename
        final_zip = f"{final_zip}.{node_info_str}.zip"

    cmd_zip_enc = sh.Command("zip").bake(["-r", final_zip])
    cmd_zip_enc_r = cmd_zip_enc(work_dir_mid_str, _cwd=work_dir_conf)

    pathlib.Path(tmp_key_enc).unlink(missing_ok=True)
    pathlib.Path(data_file_enc).unlink(missing_ok=True)
    work_dir.rmdir()

    final_zip_full_path = work_dir_conf / final_zip
    oss_upload(oss_ak_id, oss_ak_secret, oss_ep, oss_bucket_name, str(final_zip_full_path), final_zip)
    final_zip_full_path.unlink()


def oss_upload(ak_id, ak_secret, ep, bucket_name, file_path, file_name):
    auth = oss2.Auth(ak_id, ak_secret)
    # 填写Bucket名称。
    bucket = oss2.Bucket(auth, ep, bucket_name)

    # 必须以二进制的方式打开文件。
    # 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
    with open(file_path, 'rb') as fileobj:
        # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
        # fileobj.seek(1000, os.SEEK_SET)
        # Tell方法用于返回当前位置。
        # current = fileobj.tell()
        # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
        bucket.put_object(file_name, fileobj)


@click.command()
@click.option("--check", help="检查依赖环境")
def main_check():
    _exec("pwd")
    _exec("uname", "-a")
    _exec("ssh", "-V")
    _exec("openssl", "version")
    _exec("python3", "--version")
    _exec("zip", "-v")


if __name__ == '__main__':
    main()
