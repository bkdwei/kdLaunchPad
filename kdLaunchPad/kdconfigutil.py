# coding: utf-8

import json
from .fileutil import check_and_create
from . import kdconfig


def init_conf():
    check_and_create(kdconfig.config_file)
    with open(kdconfig.config_file, "r") as f:
        content = f.read()
        if content.strip() != "":
            conf = json.loads(content)
            return conf


def update_conf(confs):
    check_and_create(kdconfig.config_file)
    with open(kdconfig.config_file, "w") as f:
        print(confs)
        f.write(json.dumps(confs,ensure_ascii=False))
        f.flush()
