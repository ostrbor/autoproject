"""Create project folder, github repo with
content from Templates"""
import os
import json
import subprocess
from pathlib import Path
import requests
from config import GITHUB_USER, GITHUB_TOKEN

TEMPLATE_DIR = "Templates"
PROJECT_HOME_ENV = "PROJECT_HOME"
MAKE_VENV_CMD = "source /usr/local/bin/virtualenvwrapper.sh && mkproject {}"
COPY_CMD = "cp -R {SRC}/* {DEST}"
GIT_INIT_CMD = "cd {DEST} && git init && git add . && git commit -m 'First commit'"
GITHUB_API_URL = "https://api.github.com/user/repos?access_token={TOKEN}"
GITHUB_PUSH_CMD = "cd {DEST} && git remote add origin git@github.com:{GITHUB_USER}/{REPOS}.git "\
                  "&& git push origin master"


def shell_cmd(cmd):
    "run shell command"
    subprocess.run(cmd, check=True, shell=True, executable='/bin/zsh')

if __name__ == '__main__':
    NAME = REPOS = input("Enter project name: ")
    shell_cmd(MAKE_VENV_CMD.format(NAME))
    PROJECT_HOME = os.environ['PROJECT_HOME']
    DEST = Path(PROJECT_HOME) / NAME
    SRC = Path(PROJECT_HOME) / TEMPLATE_DIR
    shell_cmd(COPY_CMD.format(SRC=SRC, DEST=DEST))
    shell_cmd(GIT_INIT_CMD.format(DEST=DEST))
    DATA_JSON = json.dumps({"name": NAME})
    RES = requests.post(GITHUB_API_URL.format(TOKEN=GITHUB_TOKEN),
                        data=DATA_JSON)
    if RES.status_code != 201:
        print("Request to create repos failed!")
    # add SSH to github account
    shell_cmd(GITHUB_PUSH_CMD.format(DEST=DEST,
                                     GITHUB_USER=GITHUB_USER,
                                     REPOS=REPOS))
