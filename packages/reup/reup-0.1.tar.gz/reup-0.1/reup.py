import re
import webbrowser
import urllib.parse

__all__ = [
    "match",
    "fullmatch",
    "search",
    "sub",
    "subn",
    "split",
    "findall",
    "finditer",
    "compile",
    "purge",
    "template",
    "escape",
    "error",
    "Pattern",
    "Match",
    "A",
    "I",
    "L",
    "M",
    "S",
    "X",
    "U",
    "ASCII",
    "IGNORECASE",
    "LOCALE",
    "MULTILINE",
    "DOTALL",
    "VERBOSE",
    "UNICODE",
]


def flags_to_chars(flags: [int]):
    """
    flags_to_chars(re.M | re.IGNORECASE) -> ["m", "i"]
    """
    flag_mapping = {
        re.I: "i",  # Case-insensitive
        re.M: "m",  # Multi-line
        re.S: "s",  # Dot matches newline
        re.U: "u",  # Unicode
        re.X: "x",  # Extended (Ignore whitespace)
        re.A: "a",  # ASCII (Make escape sequences perform ASCII-only matching)
    }

    result = []

    for flag, char in flag_mapping.items():
        if flags & flag:
            result.append(char)

    return result


def make_regex101_url(pattern, string, flags=0, flavor="python"):
    """
    Docs: https://github.com/firasdib/Regex101/wiki/FAQ#how-to-prefill-the-fields-on-the-interface-via-url
    """
    # URL-encode pattern and string
    encoded_pattern = urllib.parse.quote(pattern)
    encoded_string = urllib.parse.quote(string)

    # Create the URL
    flags = ",".join(flags_to_chars(flags))
    url = f"https://regex101.com/?regex={encoded_pattern}&testString={encoded_string}&flavor={flavor}&flags={flags}"
    return url


def open_regex101_then_apply(original_method):
    """
    Decorator to create a URL, open it in the browser, and delegate to the original re method
    """

    def wrapper(pattern, string, *args, **kwargs):
        flags = kwargs.get("flags", 0)  # Get the regex flags
        url = make_regex101_url(pattern, string, flags)
        webbrowser.open(url)

        # Call the original method and return the result
        return original_method(pattern, string, *args, **kwargs)

    return wrapper


def open_regex101_then_apply_replace(original_method):
    """
    re.sub and re.subn take a replacement string as their second argument,
    rather than a string to search for.
    Currently regex101.com doesn't setting the replacement string in the URL.
    """

    def wrapper(pattern, replacement, string, *args, **kwargs):
        flags = kwargs.get("flags", 0)  # Get the regex flags
        url = make_regex101_url(pattern, string, flags)
        webbrowser.open(url)

        # Call the original method and return the result
        return original_method(pattern, replacement, string, *args, **kwargs)

    return wrapper


# Apply the decorator to the relevant re module functions
match = open_regex101_then_apply(re.match)
fullmatch = open_regex101_then_apply(re.fullmatch)
search = open_regex101_then_apply(re.search)
sub = open_regex101_then_apply_replace(re.sub)
subn = open_regex101_then_apply_replace(re.subn)
split = open_regex101_then_apply(re.split)
findall = open_regex101_then_apply(re.findall)
finditer = open_regex101_then_apply(re.finditer)

# Re-export everything from the original re module
compile = re.compile
purge = re.purge
template = re.template
escape = re.escape
error = re.error
Pattern = re.Pattern
Match = re.Match


A = re.A
ASCII = re.ASCII
I = re.I
IGNORECASE = re.IGNORECASE
L = re.L
LOCALE = re.LOCALE
M = re.M
MULTILINE = re.MULTILINE
S = re.S
DOTALL = re.DOTALL
X = re.X
VERBOSE = re.VERBOSE
U = re.U
UNICODE = re.UNICODE
