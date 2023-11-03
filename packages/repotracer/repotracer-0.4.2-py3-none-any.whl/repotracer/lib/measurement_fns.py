from . import git

import subprocess
import json


def script(cmd):
    return lambda: subprocess.check_output(cmd, shell=True)


def script_now(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode("utf-8")
    except subprocess.CalledProcessError as e:
        # ignoGenericre exit code 1
        if e.returncode == 1:
            return e.output
        print("Error in script_now")
        print(e)
        print(e.output)
        raise e


def float_or_int(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except Exception as e:
            return float("NaN")


def script_auto(cmd, return_type):
    output = script_now(cmd)
    if return_type == "number":
        return {"output": float_or_int(output)}
    elif return_type == "json":
        return json.loads(output)
    else:
        raise ValueError(f"Unknown return type {return_type}")


def ripgrep_count_file(pattern):
    return int(script(f"rg -l {pattern} | wc -l"))


def rg_count(pattern: str, rg_args: str) -> int:
    filenames_with_counts = script_now(f"rg '{pattern}' --count {rg_args or ''}")
    res = {
        "total": sum(
            int(line.split(":")[-1]) for line in filenames_with_counts.splitlines()
        )
    }
    return res


def fd_count(pattern: str, extra_cli_args: str) -> int:
    filenames_with_counts = script_now(
        f"fd --glob '{pattern}' --type file {extra_cli_args or ''}"
    )
    # todo: eventually, store the individual file names as intermediate results
    res = {"total": len(filenames_with_counts.splitlines())}
    return res


def tokei_count(languages: str, extra_cli_args: str) -> int:
    if languages == "all":
        languages = ""
    language_arg = f"-t {languages}" if languages else ""
    json_out = script_now(f"tokei --output json {language_arg} {extra_cli_args or ''}")
    parsed = json.loads(json_out)
    code_totals = {language: data["code"] for language, data in parsed.items()}
    breakdown_languages = True
    if breakdown_languages:
        del code_totals["Total"]
        return code_totals
    else:
        return code_totals["Total"]


def jsx_to_tsx():
    return script_now("tokei --output json --languages jsx,tsx,js,ts")
