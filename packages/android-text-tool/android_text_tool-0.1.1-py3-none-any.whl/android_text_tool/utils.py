import sys


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    if count == 0:
        count = 1

    def show(j):
        x = int(size * j / count)
        file.write(
            "%s[%s%s] %i/%i\r" % (prefix, "#" * x, "." * (size - x), j, count)
        )
        file.flush()

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    file.write("\n")
    file.flush()


def trim_value_prefix(value: str, default_language="en") -> str:
    if value.startswith("values-"):
        return value[7:]

    if len(value) == 2:
        return value

    return default_language
