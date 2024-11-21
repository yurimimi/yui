import os

def resolve_envvars(sh_string):
    return os.popen(f"echo {sh_string}").read()[:-1]
