from importlib import import_module
from os.path import basename, dirname, splitext
from sys import argv, path, stderr, exc_info
from traceback import extract_tb


if __package__:
    from .launch import main
else:
    package = dirname(__file__)
    parent, target = dirname(package), basename(package)
    path.insert(0, parent)
    main = import_module(f"{target}.launch", target).main


def process_exc_trace(exc_trace):
    stack = extract_tb(exc_trace)
    location = " > ".join(
        f"{splitext(basename(part[0]))[0]}.{part[2]}:{part[1]}"
        for part in stack[1:])
    return stack, location


def write_error(exc_type, exc_value, exc_trace):
    stack, location = process_exc_trace(exc_trace)
    message = "ERROR\n" \
        f" -> Location: {location}\n" \
        f" -> Line: {stack[-1][3]}\n" \
        f" -> {exc_type.__name__}: {exc_value}"
    stderr.write(f"{message}\n")


def write_abort(exc_type, exc_value, exc_trace):
    message = "ABORTED"
    stderr.write(f"{message}\n")


def write_interrupt(exc_type, exc_value, exc_trace):
    stack, location = process_exc_trace(exc_trace)
    message = " INTERRUPTED\n" \
        f" -> Location: {location}\n" \
        f" -> Line: {stack[-1][3]}"
    stderr.write(f"{message}\n")


if __name__ == "__main__":
    try:
        main(argv[1:])
    except KeyboardInterrupt:
        write_interrupt(*exc_info())
        raise SystemExit(1)
    except Exception as exc:
        if str(exc).lower() == "aborted":
            write_abort(*exc_info())
        else:
            write_error(*exc_info())
        raise SystemExit(1)
