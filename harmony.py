import json
import os
import sys
import requests
import shutil
import subprocess

def fetch_repos():
    repos = {}
    page = 1
    while True:
        url = 'https://gitee.com/api/v5/search/repositories?q=OpenHarmony&per_page=100&owner=OpenHarmony&order=asc&page=' + str(page)
        r = requests.get(url)
        sub_repos = json.loads(r.content)
        if len(sub_repos) == 0:
            break
        for n in range(len(sub_repos)):
            repos[sub_repos[n]['name']] = sub_repos[n]['html_url']
        page += 1
    return repos

def do_cmd(cmd):
    try:
        return subprocess.check_call(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return 1

def clone(force):
    print('fetching latest repos...')
    repos = fetch_repos()
    index = 1
    cwd = os.getcwd()
    print('{} repos found'.format(str(len(repos))))
    for name, url in repos.items():
        abs_path = cwd + "/" + name
        if os.path.isdir(abs_path):
            if force:
                shutil.rmtree(abs_path)
            else:
                print('repo {} already exists'.format(url))
                exit(1)
        print("cloning[{}/{}] {}".format(index, len(repos), url))
        if do_cmd("git clone {}".format(url)) != 0:
            print('clone stopped due to error')
            exit(1)
        index += 1

def update(force):
    raise Exception("not implement")

def main(argv):
    if len(argv) < 1:
        print('python harmony.py clone/update [-force]')
        exit(0)
    op = argv[0]
    force = False
    if len(argv) > 1 and argv[1] == '-force':
        force = True
    if op == 'update':
        update(force)
    elif op == 'clone':
        clone(force)
    else:
        print('unknown operation "{}"'.format(op))
        exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])
