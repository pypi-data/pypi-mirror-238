import pathlib


def get_default_iidxbak_home_dir() -> pathlib.Path:
    p = pathlib.Path().home() / ".iidxbak"
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
    return p


def get_default_iidxbak_home_conf_dir():
    p = get_default_iidxbak_home_dir() / "conf"
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
    return p


def ensure_home_path(pubkey_path: str):
    if not pubkey_path.startswith("/"):
        return get_default_iidxbak_home_dir() / pubkey_path

    return pathlib.Path(pubkey_path)
