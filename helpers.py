from io import BytesIO

from IPython.display import display, Image

from string import ascii_letters, digits, punctuation


SANE_ASCII = {ord(ch): ch for ch in ascii_letters + digits + punctuation}


def find_iter(value, sub):
    index = value.find(sub)
    while index > -1:
        yield index
        index = value.find(sub, index + 1)


def find_all(value, sub):
    return list(find_iter(value, sub))


def display_image(image, **options):
    """Convert a PIL image to an IPython image which can be displayed inline."""
    with BytesIO() as f:
        image.save(f, format="png")
        img = Image(data=f.getvalue(), format="png", embed=True, metadata=options)
    display(img)


def asciify(data, zero=".", nonascii="."):
    """Display binary data as ASCII characters.

    Not all printable characters are used. For example,
    whitespace is a pain to display and is escaped as non-ASCII.
    """
    translation = {**SANE_ASCII, 0: zero}
    return "".join(translation.get(byte, nonascii) for byte in data)


def hexdump(data, width=8):
    length = len(data)
    w = len(str(length))
    fmt = f"{{:0{w}}}"
    for i in range(0, length, width):
        chunk = data[i:i + width]
        pad = "   " * (width - len(chunk))
        print(fmt.format(i), " ".join(f"{b:02X}" for b in chunk) + pad, asciify(chunk), sep="|")
