import keyword


def mangle_keyword(name: str) -> str:
    if keyword.iskeyword(name):
        name = f"{name}_"
    return name


def unmangle_keyword(name: str) -> str:
    assert name
    if name[-1] == "_" and keyword.iskeyword(name[:-1]):
        name = name[:-1]
    return name
