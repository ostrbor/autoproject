import json
import requests
from pathlib import Path
import subprocess
import os
from config import USER, GITHUB_TOKEN

TEMPLATE_DIR = "Templates"
PROJECT_HOME_ENV = "PROJECT_HOME"
MAKE_VENV_CMD = "source /usr/local/bin/virtualenvwrapper.sh && mkproject {}"
COPY_CMD = "cp -R {SRC}/* {DEST}"
GIT_INIT_CMD = "cd {DEST} && git init && git add . && git commit -m 'First commit'"
GITHUB_API_URL = "https://api.github.com/user/repos?access_token={TOKEN}"
GITHUB_PUSH_CMD = "cd {DEST} && git remote add origin git@github.com:{USER}/{REPOS}.git "\
                  "&& git push origin master"


def shell_cmd(cmd):
    res = subprocess.run(cmd, shell=True, executable='/bin/zsh')
    if res.returncode != 0:
        raise Exception("Couldn't execute shell command.", cmd)

if __name__ == '__main__':
    NAME = REPOS = input("Enter project name: ")
    shell_cmd(MAKE_VENV_CMD.format(NAME))
    PROJECT_HOME = os.environ['PROJECT_HOME']
    DEST = Path(PROJECT_HOME) / NAME
    SRC = Path(PROJECT_HOME) / TEMPLATE_DIR
    shell_cmd(COPY_CMD.format(SRC=SRC, DEST=DEST))
    shell_cmd(GIT_INIT_CMD.format(DEST=DEST))
    DATA_JSON = json.dumps({"name": NAME})
    res = requests.post(GITHUB_API_URL.format(TOKEN=GITHUB_TOKEN),
                        data=DATA_JSON)
    if res.status_code != 201:
        print("Request to create repos failed!")
    shell_cmd(GITHUB_PUSH_CMD.format(DEST=DEST, USER=USER, REPOS=REPOS))
