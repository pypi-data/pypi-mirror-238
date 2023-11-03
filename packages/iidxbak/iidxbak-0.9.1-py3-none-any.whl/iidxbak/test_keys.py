import sh

KEYS_PRIVATE_PEM_FILE = "../tests/etc/keys.private.pem"
KEYS_PUBLIC_PEM_FILE = "../tests/etc/keys.public.pem"


def main():
    pass


def gen_private():
    cmd_openssl = sh.Command("openssl")
    cmd_openssl_bake = cmd_openssl.bake(["genrsa", "-out", KEYS_PRIVATE_PEM_FILE, "2048"])
    cmd_openssl_r = cmd_openssl_bake()
    print(cmd_openssl_r)


def get_public_from_private(private_pem_file=None):
    private_pem_file = private_pem_file or KEYS_PRIVATE_PEM_FILE
    cmd_openssl = sh.Command("openssl")
    cmd_openssl_bake = cmd_openssl.bake(["rsa", "-in", private_pem_file, "-pubout", "-out", KEYS_PUBLIC_PEM_FILE])
    cmd_openssl_bake_r = cmd_openssl_bake()


def gen_tmp_key():
    cmd_openssl = sh.Command("openssl")
    # 32字节==256位的随机密钥
    cmd_openssl_bake = cmd_openssl.bake(["rand", "32"])
    cmd_openssl_bake(_out="keys.tmp.key.txt")


def enc_tmp_key(key_file=None):
    key_file = key_file or "keys.tmp.key.txt"
    cmd_openssl = sh.Command("openssl")
    cmd_openssl_bake = cmd_openssl.bake(
        ["rsautl", "-encrypt", "-pubin", "-inkey", KEYS_PUBLIC_PEM_FILE, "-in", key_file, "-out", f"{key_file}.enc"])
    cmd_openssl_bake_r = cmd_openssl_bake()


def dec_tmp_key(key_file_enc=None):
    key_file_enc = key_file_enc or "keys.tmp.key.txt.enc"
    cmd_openssl = sh.Command("openssl")
    cmd_openssl_bake = cmd_openssl.bake(
        ["rsautl", "-decrypt", "-inkey", KEYS_PRIVATE_PEM_FILE, "-in", key_file_enc, "-out", f"{key_file_enc}.dec"])
    cmd_openssl_bake_r = cmd_openssl_bake()


def enc_data_file(data_file, key_file):
    cmd_openssl = sh.Command("openssl")
    cmd_openssl_bake = cmd_openssl.bake([
        "enc", "-aes-256-cbc", "-salt",
        "-md", "sha256",
        "-in", data_file,
        "-out", f"{data_file}.enc",
        "-pass", f"file:{key_file}"
    ])
    cmd_openssl_bake_r = cmd_openssl_bake()


def dec_data_file(data_file_enc, key_file):
    cmd_openssl = sh.Command("openssl")
    cmd_openssl_bake = cmd_openssl.bake(
        [
            "enc", "-d", "-aes-256-cbc",
            "-md", "sha256",
            "-in", data_file_enc,
            "-out", f"{data_file_enc}.dec",
            "-pass", f"file:{key_file}"
        ]
    )
    cmd_openssl_bake_r = cmd_openssl_bake()


def cmp(k_src, k_dec):
    cmd_cmp = sh.Command("cmp")
    cmd_cmp_bak = cmd_cmp.bake([k_src, k_dec])
    cmd_cmp_bak_r = cmd_cmp_bak()
    print(cmd_cmp_bak_r)


if __name__ == '__main__':
    # gen_tmp_key()
    gen_private()
    get_public_from_private()
    # enc_tmp_key()
    # dec_tmp_key()
    # cmp("keys.tmp.key.txt", "keys.tmp.key.txt.enc.dec")
    # enc_data_file("main.py", "keys.tmp.key.txt")
    # dec_data_file("main.py.enc", "keys.tmp.key.txt")
