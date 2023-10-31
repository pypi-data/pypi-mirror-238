import os
import re
import sys


def find_available_path(path, ext=None, sep=".", also_match=None, start_at=None):
    original_path = path
    parent_path = os.path.dirname(path)
    ext = ext or ""
    also_match = also_match or []
    if start_at is None:
        number = 1
    else:
        number = start_at
        path = f"{original_path}{sep}{number}"
    if not os.path.isdir(parent_path):
        return f"{path}{ext}"
    while os.path.exists(f"{path}{ext}") or f"{path}{ext}" in also_match:
        number += 1
        path = f"{original_path}{sep}{number}"
    return f"{path}{ext}"


def log(*message, join=" ", end="\n", flush=True):
    message = join.join(str(part) for part in message)
    sys.stderr.write(message)
    sys.stderr.write(end)
    if flush:
        sys.stderr.flush()
    return message


def log_key_value(key, *values, padding=25, end="\n", flush=True):
    key = f"{key}: ".ljust(padding - 1, "-").ljust(padding)
    values = ("\n" + " " * padding).join(str(value) or "< none >" for value in values)
    if not values:
        values = "< none >"
    return log(key, values, join="", end=end, flush=flush)


def abort():
    raise RuntimeError("aborted")


def ask_continue(prompt="continue?", default=None):
    response = None
    while response not in ["y", "yes", "n", "no"]:
        if response is not None:
            sys.stderr.write("\r")
        sys.stderr.write(f"{prompt} [y/n] ")
        if os.isatty(sys.stdin.fileno()):
            response = input()
        elif default is None:
            raise RuntimeError("unable to get answer and no default")
        else:
            response = "y" if default else "n"
            sys.stderr.write(f"{response}\n")
    return response in ["y", "yes"]


def duration_to_seconds(raw):
    d, h, m, s = re.match(r"(?:(\d+)-)?(\d\d):(\d\d):(\d\d)", raw).groups()
    h, m, s = (int(x) for x in [h, m, s])
    if (d is not None and h >= 24) or m >= 60 or s >= 60:
        raise ValueError("invalid duration format")
    d = 0 if d is None else int(d)
    return d * 86400 + h * 3600 + m * 60 + s


def validate_setting(key, value, validation):
    def warning(info=None):
        return \
            f"setting {key} failed validation:\n" \
            f"    required: {' '.join(validation)}\n" \
            f"    specified: {value or '< none >'}{f' ({info})' if info else ''}"
    if validation[0] == "optional":
        if value is None or value == "":
            return "", None
        validation = validation[1:]
    if value is None:
        raise ValueError(f"setting {key} not specified")
    if validation[0] == "" or validation[0] == "any":
        pass
    elif validation[0] == "path":
        expanded = os.path.expandvars(value)
        if len(validation) == 1:
            pass
        elif validation[1] == "exists":
            if not os.path.exists(expanded):
                return value, warning()
        elif validation[1] == "file_exists":
            if not os.path.isfile(expanded):
                return value, warning()
        elif validation[1] == "dir_exists":
            if not os.path.isdir(expanded):
                return value, warning()
        elif validation[1] == "base_exists":
            parent = os.path.dirname(expanded)
            if os.path.isdir(parent):
                base_name = os.path.basename(expanded)
                for file in os.listdir(parent):
                    if file.startswith(base_name):
                        break
                else:
                    return value, warning()
            else:
                return value, warning()
        else:
            raise ValueError(f"invalid path validation: {validation}")
    elif validation[0] == "number":
        if re.match(r"^[+-]?([0-9]*[.])?[0-9]+$", value):
            if len(validation) > 1:
                if not eval(value + " " + " ".join(validation[1:])):
                    return value, warning()
        else:
            return value, warning()
    elif validation[0] == "integer":
        if re.match(r"^[+-]?[0-9]+$", value):
            if len(validation) > 1:
                if not eval(value + " " + " ".join(validation[1:])):
                    return value, warning()
        else:
            return value, warning()
    elif validation[0] == "regex":
        if not re.match(rf"^{validation[1]}$", value):
            return value, warning()
    elif validation[0] == "choice":
        choices = validation[1].split("|")
        if value not in choices:
            return value, warning()
    elif validation[0] == "duration":
        validation[0] = "duration as dd-hh:mm:ss or hh:mm:ss"
        try:
            duration = duration_to_seconds(value)
        except Exception:
            return value, warning()
        if len(validation) > 1:
            threshold = duration_to_seconds(validation[2])
            if not eval(f"{duration} {validation[1]} {threshold}"):
                return value, warning()
    else:
        raise ValueError(f"invalid setting validation: {validation}")
    return value, None
