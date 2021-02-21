import re
from collections import namedtuple
from pprint import pprint
import string
import itertools
import os
import shutil
import subprocess
from tqdm import tqdm
import threading
import queue
import time

Commit = namedtuple("Commit", ["sha", "name", "email", "date", "message"])


def parse_log():
    s = open("log.txt").read()
    s = s.split("\n")

    commits = []

    i = 0
    while i < len(s):
        sha = s[i].split()[-1]
        i += 1
        res = re.match("Author: (.*) <(.*)>", s[i])
        name = res.group(1)
        email = res.group(2)
        i += 1
        date = " ".join(s[i].split()[1:])
        i += 1
        i += 1
        message = s[i][4:]

        commit = Commit(sha, name, email, date, message)
        commits.append(commit)
        i += 1
        i += 1

    return commits


def get_unknowns(commit):
    s = commit.message.split(": ")[1]
    s = s.split(", ")
    return [int(c) for c in s]


def do_commit(commit, trigram, thread_i, keep=False):
    unknowns = get_unknowns(commit)
    d = f"tmp{thread_i}"
    s = list(open(f"{d}/flag.txt").read())

    for i, uk in enumerate(unknowns):
        s[uk + 5] = trigram[i]

    s = "".join(s)
    open(f"{d}/flag.txt", "w").write(s)

    script = f"""
cd {d} && \\
    export GIT_AUTHOR_DATE="{commit.date}" && \\
    export GIT_COMMITTER_DATE="{commit.date}" && \\
    git config user.name "Flag-deciding Committee" && \\
    git config user.email "committee@legal.committee";
git commit -a \\
    -m "{commit.message}" \\
    --author="{commit.name} <{commit.email}>" \\
    --date="{commit.date}" \\
    --quiet;
git rev-parse HEAD;
"""
    if not keep:
        script += f"cd .. && rm -rf {d} && cp -r leak {d};\n"

    # print(script)
    sha = subprocess.check_output(script, shell=True)
    sha = sha.decode().strip()
    return sha


def char_pool():
    ans = string.digits + "_" + string.ascii_lowercase + string.ascii_uppercase
    # ans = string.digits + "_" + string.ascii_lowercase
    # ans = string.digits + "abcdef"
    return ans


# poss_chars = get_poss_chars()
# a_chars = char_pool()
# b_chars = char_pool()
# c_chars = char_pool()
a_chars = "_"
b_chars = char_pool()
c_chars = char_pool()

n_threads = 4


def permute(commit, thread_i, q):
    t = threading.currentThread()

    d = f"tmp{thread_i}"
    if os.path.exists(d):
        shutil.rmtree(d)
    shutil.copytree("repo", d)

    total = len(a_chars) * len(b_chars) * len(c_chars) // n_threads
    # if True:
    with tqdm(total=total) as pbar:
        # for i, trigram in enumerate(itertools.permutations(poss_chars, r=3)):
        # for i, trigram in enumerate(itertools.product(poss_chars, repeat=3)):
        i = 0
        for a in a_chars:
            for b in b_chars:
                for c in c_chars:
                    trigram = (a, b, c)
                    if i % n_threads != thread_i:
                        i += 1
                        continue

                    if not getattr(t, "do_run", True):
                        break

                    sha = do_commit(commit, trigram, thread_i)
                    pbar.update()
                    # print(trigram, sha, commit.sha)
                    if sha == commit.sha:
                        # print(f"Found match: {trigram}")
                        flag = open(f"{d}/flag.txt").read()
                        # print(f"Flag so far: {flag}")
                        q.put(trigram)
                        break
                    i += 1

        pbar.close()


def run_all(commits):
    for commit in commits:
        print(f"Doing {commit.sha}")

        q = queue.Queue()
        threads = [
            threading.Thread(target=permute, args=(commit, i, q))
            for i in range(n_threads)
        ]

        for th in threads:
            th.start()

        trigram = q.get()
        q.task_done()

        for th in threads:
            setattr(th, "do_run", False)

        q.join()
        # print("Threads done")
        time.sleep(1)

        del th
        del q

        print("\n" * 2)
        print(f"Thread return {trigram}")
        d = "tmp0"
        shutil.rmtree(d)
        shutil.copytree("repo", d)
        sha = do_commit(commit, trigram, 0, keep=True)
        flag = open(f"{d}/flag.txt").read()
        print(f"Flag so far: {flag}")
        assert sha == commit.sha
        shutil.rmtree("repo")
        shutil.copytree(d, "repo")

        break


commits = parse_log()

commits = commits[::-1]
commits = commits[16:]
# pprint(commits)

if os.path.exists("repo"):
    shutil.rmtree("repo")

shutil.copytree("leak", "repo")


def run_single():
    thread_i = 0
    d = f"tmp{thread_i}"
    if os.path.exists(d):
        shutil.rmtree(d)
    shutil.copytree("repo", d)

    commit = commits[0]

    sha = do_commit(commit, ("A", "B", "C"), 0, True)
    print(sha, commit.sha)


# run_single()
run_all(commits)
