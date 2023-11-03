import click
import sh


def print_step(info):
    click.echo(click.style(f">>>> {info}", fg="green"))


def _click_fg_blue(text):
    click.echo(click.style(text, fg="blue"))


def _click_fg_red(text):
    click.echo(click.style(text, fg="red"))


def _exec(cmd_str, args=None):
    try:
        cmd = sh.Command(cmd_str)
        if args and (isinstance(args, str) or isinstance(args, list)):
            cmd = cmd.bake(args)

        _click_fg_blue(f">>>>{cmd}")
        cmd_r = cmd()
        _click_fg_blue(cmd_r)
        return 0, cmd_r
    except sh.ErrorReturnCode as e:
        _click_fg_red(e.stderr.decode())
        return 1, e.stderr.decode()


def gen_tmp_key(tmp_key_path):
    cmd_openssl = sh.Command("openssl")
    # 32字节==256位的随机密钥
    cmd_openssl_bake = cmd_openssl.bake(["rand", "32"])
    r = cmd_openssl_bake(_out=tmp_key_path)
    return r


def enc_data_file(data_file, key_file, data_file_enc):
    cmd_openssl = sh.Command("openssl")
    cmd_openssl_bake = cmd_openssl.bake([
        "enc", "-aes-256-cbc", "-salt",
        "-md", "sha256",
        "-in", str(data_file),
        "-out", str(data_file_enc),
        "-pass", f"file:{key_file}"
    ])
    cmd_openssl_bake_r = cmd_openssl_bake()
    return cmd_openssl_bake_r


def enc_tmp_key(public_key_path, key_file_raw, key_file_bak):
    cmd_openssl = sh.Command("openssl")
    cmd_openssl_bake = cmd_openssl.bake(
        ["rsautl", "-encrypt", "-pubin",
         "-inkey", str(public_key_path),
         "-in", str(key_file_raw),
         "-out", str(key_file_bak)])
    cmd_openssl_bake_r = cmd_openssl_bake()
    return cmd_openssl_bake_r
