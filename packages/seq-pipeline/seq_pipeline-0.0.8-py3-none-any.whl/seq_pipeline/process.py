import getpass
import os
import re
import subprocess

from .config import INPUT_TYPES, PIPELINES_DIR, VERSION
from .util import abort, ask_continue, find_available_path, log, log_key_value, validate_setting


def get_pipeline(name, version=None, command=None):
    name = name.replace("-", "_")
    path = os.path.join(PIPELINES_DIR, f"{name}.sh")
    if not os.path.isfile(path):
        raise ValueError(f"unknown pipeline: {name}")
    with open(path, "r") as file:
        script = [line.rstrip() for line in file]
    info = {}
    variables = {}
    if script[0].startswith("# ---"):
        for key, value in [("version", version), ("command", command)]:
            if value is not None:
                escaped_value = value.replace("\n", "\n# > ... ")
                script.insert(1, f"# > {key} = {escaped_value}")
    for index, line in enumerate(script):
        if not index or not line:
            continue
        if line.startswith("# ---"):
            break
        if line.startswith("# >"):
            if line.startswith("# > ..."):
                continue
            key, value = re.match(r"^# >\s*(\w+)\s*=\s*(.*)$", line).groups()
            info[key] = [index, value]
            continue
        key, value = re.match(r'^(\w+)="{([^}]*)}"$', line).groups()
        value = re.split(r'\s+', value.strip())
        variables[key] = [index, value]
    extensions = INPUT_TYPES[info["input_type"][1]]
    pipeline = {
        "script": script,
        "info": info,
        "variables": variables,
        "extensions": extensions}
    return pipeline


def parse_settings(settings, pipeline):
    parsed_settings = {}
    required_header_settings = [
        ("ACCOUNT", ["any"]),
        ("TIME", ["duration", ">", "00:00:00"]),
        ("CPU_CORES", ["integer", ">", "0"]),
        ("MEMORY_PER_CORE", ["regex", r"[0-9]+[KMGT]?"])]
    for key, validation in required_header_settings:
        value = settings.get(key.lower(), None)
        key = f"{key} (SCRIPT HEADER)"
        value, warning = validate_setting(key, value, validation)
        parsed_settings[key] = {"value": value, "warning": warning}
    for key, (_, validation) in pipeline["variables"].items():
        if key.lower() == "base_path":
            continue
        _, validation = pipeline["variables"][key]
        value = settings.get(key.lower(), None)
        value, warning = validate_setting(key, value, validation)
        parsed_settings[key] = {"value": value, "warning": warning}
    return parsed_settings


def process_inputs(paths, extensions):
    inputs = {}
    for path in paths:
        if os.path.isdir(path):
            for name in os.listdir(path):
                for extension in extensions:
                    if not name.endswith(extension):
                        continue
                    file_path = os.path.join(path, name)[:-len(extension)]
                    inputs[os.path.realpath(file_path)] = file_path
                    break
            continue
        for extension in extensions:
            if path.endswith(extension):
                path = path[:-len(extension)]
                break
        inputs[os.path.realpath(path)] = path
    inputs = [{"in_base_path": base_path} for base_path in inputs.values()]
    for input in inputs:
        input['in_base_path'] = os.path.normpath(input['in_base_path'])
        input['base_name'] = os.path.basename(input['in_base_path'])
        input['in_paths'] = []
        for extension in extensions:
            in_path = f'{input["in_base_path"]}{extension}'
            if not os.path.exists(in_path):
                raise FileNotFoundError(f'input file {in_path} missing')
            input['in_paths'].append(in_path)
    return inputs

        
def set_out_paths(input, out_dir, no_sub_dir):
    if out_dir is None:
        out_dir = os.path.dirname(input['in_base_path'])
    out_dir = os.path.realpath(out_dir)
    if no_sub_dir:
        input['out_dir'] = out_dir
    else:
        input['out_dir'] = os.path.join(out_dir, input['base_name'])
    input['base_path'] = os.path.join(input['out_dir'], input['base_name'])
    input['out_paths'] = []
    for in_path in input['in_paths']:
        out_path = os.path.join(input['out_dir'], os.path.basename(in_path))
        input['out_paths'].append(out_path)
    input['job_path'] = find_available_path(os.path.join(input['out_dir'], input['base_name'] + ".job"), ext='.sh')
    input['log_path'] = find_available_path(os.path.join(input['out_dir'], input['base_name'] + ".job"), ext='.log')


def make_script(input, settings, pipeline):
    script = pipeline["script"].copy()
    for key, (index, _) in pipeline["variables"].items():
        if key.lower() == "base_path":
            value = input["base_path"]
        else:
            value = settings[key]["value"]
        script[index] = f"{key}=\"{value}\""
    header = \
        f"#!/bin/bash\n" \
        f"#SBATCH --account='{settings['ACCOUNT (SCRIPT HEADER)']['value']}'\n" \
        f"#SBATCH --time='{settings['TIME (SCRIPT HEADER)']['value']}'\n" \
        f"#SBATCH --cpus-per-task='{settings['CPU_CORES (SCRIPT HEADER)']['value']}'\n" \
        f"#SBATCH --mem-per-cpu='{settings['MEMORY_PER_CORE (SCRIPT HEADER)']['value']}'\n" \
        f"#SBATCH --job-name='{input['base_name']}'\n" \
        f"#SBATCH --output='{input['log_path']}'"
    input["script"] = header + "\n\n\n" + "\n".join(script)


def check_no_overwrite(inputs):
    existing = []
    for input in inputs:
        in_paths = [os.path.realpath(path) for path in input["in_paths"]]
        for path in (*input["out_paths"], input["job_path"]):
            if os.path.realpath(path) in in_paths:
                continue
            if os.path.exists(path):
                existing.append(path)
    if existing:
        log("warning: these files already exist and will be overwritten:")
        for path in existing:
            log(f"    {path}")
        if not ask_continue():
            abort()


def write_scripts(inputs):
    for input in inputs:
        if not os.path.isdir(os.path.dirname(input['out_dir'])):
            raise FileNotFoundError(f"parent directory of {input['out_dir']} missing")
        if not os.path.isdir(input['out_dir']):
            os.mkdir(input['out_dir'])
        with open(input['job_path'], 'w') as file:
            file.write(input['script'])


def move_inputs(inputs):
    for input in inputs:
        for in_path, out_path in zip(input['in_paths'], input['out_paths']):
            if os.path.realpath(in_path) == os.path.realpath(out_path):
                continue
            os.rename(in_path, out_path)


def start_jobs(inputs, dry):
    if dry:
        log("start commands:")
    for input in inputs:
        input['start_command'] = ['sbatch', input['job_path']]
        start_command_for_log = ['sbatch', os.path.basename(input['job_path'])]
        if dry:
            log("    " + " ".join(input["start_command"]))
        else:
            log(" ".join(start_command_for_log), end=": ")
            result = subprocess.run(input['start_command'], capture_output=True, check=True)
            log(result.stdout.decode().strip())
    if not dry:
        result = subprocess.run(['squeue', '-u', getpass.getuser()], capture_output=True, check=True)
        log(result.stdout.decode().strip())


def process(pipeline_name, inputs_locs, out_dir, no_sub_dir, settings, cmd_line=None):

    pipeline = get_pipeline(pipeline_name, VERSION, cmd_line)
    settings = parse_settings(settings, pipeline)
    setting_warnings = [setting["warning"] for setting in settings.values() if setting["warning"]]
    if setting_warnings:
        for setting_warning in setting_warnings:
            log(setting_warning)
        if not ask_continue("warning: settings have failed validation, continue anyway?"):
            abort()

    inputs = process_inputs(inputs_locs, pipeline["extensions"])
    for input in inputs:
        set_out_paths(input, out_dir, no_sub_dir)
        make_script(input, settings, pipeline)

    log_key_value("pipeline", pipeline_name)
    log_key_value("extensions", " ".join(pipeline["extensions"]))
    if not inputs:
        log_key_value("search for or in", *inputs_locs)
        log("no input file matching pipeline extensions found")
        raise SystemExit(0)
    log_key_value(
        "inputs",
        *(f"{i + 1}. {input['in_base_path']}" for i, input in enumerate(inputs)))
    for key, setting in settings.items():
        if key.endswith(" (SCRIPT HEADER)"):
            if key[:-16] in settings and setting["value"] == settings[key[:-16]]["value"]:
                continue
            elif key[:-16] not in settings:
                log_key_value(f"{key[:-16].lower()}".replace("_", " "), setting["value"])
                continue
        log_key_value(f"{key.lower()}".replace("_", " "), setting["value"])

    check_no_overwrite(inputs)
    if not ask_continue("write scripts?" if no_sub_dir else "write scripts and move inputs?"):
        abort()
    write_scripts(inputs)
    move_inputs(inputs)

    response = ask_continue("start jobs?")
    start_jobs(inputs, dry=not response)
