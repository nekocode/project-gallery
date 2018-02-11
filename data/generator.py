#!/usr/bin/env python
# -*- coding: utf-8 -*-
from github import Github
import os.path
import getopt
import sys


def str_user(avatar, name, url):
    return """
var user_data = {
    "avatar": "%s",
    "name": "%s",
    "url": "%s",
}
"""[1:] % (avatar, name, url)


def str_items(items):
    return """
var items_data = [
%s
]
"""[1:] % items


def str_category_item(name):
    return """
    {
        "type": "category",
        "name": "%s",
    },
"""[1:] % name


def str_repo_item(name, description, stars, forks, lang, url):
    return """
    {
        "type": "repo",
        "name": "%s",
        "description": "%s",
        "stars": "%d",
        "forks": "%d",
        "lang": "%s",
        "url": "%s",
    },
"""[1:] % (name, description, stars, forks, lang, url)


def gen_data_txt(github, out_file_path, sort_by=None):
    repos = github.get_user().get_repos("owner")
    if sort_by is not None:
        if sort_by == "stars":
            repos = sorted(repos, key=lambda x: x.stargazers_count, reverse=True)
        elif sort_by == "name":
            repos = sorted(repos, key=lambda x: x.name)

    with open(out_file_path, 'w') as f:
        f.write("// All\n")
        for repo in repos:
            f.write("%s, %d, %d\n" % (repo.name, repo.stargazers_count, repo.forks_count))


def gen_data_js(github, in_file_path, out_file_path):
    if not os.path.exists(in_file_path):
        return

    user = github.get_user()
    repos = user.get_repos("owner")
    repos = {repo.name: repo for repo in repos}  # Convert to a dict

    with open(in_file_path, "r") as txt, open(out_file_path, 'wb') as js:
        def write(content):
            js.write(content.encode('utf-8'))

        write(str_user(user.avatar_url, user.name, user.url) + "\n")

        items_str = ""
        for line in txt:
            line = line.strip()
            if line.startswith("//"):
                category_name = line[2:].lstrip()
                items_str += str_category_item(category_name)

            elif len(line) > 0:
                repo_name = line.split(",")[0].rstrip()
                if repo_name in repos:
                    repo = repos[repo_name]
                    items_str += str_repo_item(
                        repo.name, repo.description,
                        repo.stargazers_count, repo.forks_count, repo.language,
                        repo.url
                    )

        write(str_items(items_str))


def main():
    def print_usage():
        print("usage: %s --token=GITHUB_TOKEN \n\t" % __file__ +
              "(--txt_out=TXT_OUT [--sort_by=stars|name]) | \n\t" +
              "(--txt_in=TXT_IN --js_out=JS_OUT)")

    opts, args = getopt.getopt(
        sys.argv[1:], "", ["token=", "txt_out=", "txt_in=", "js_out=", "sort_by="])
    opts = {opt[0][2:]: opt[1] for opt in opts}
    if "token" not in opts:
        print_usage()
        return

    if "txt_out" in opts:
        github = Github(opts["token"])
        sort_by = "stars"
        if "sort_by" in opts:
            sort_by = opts["sort_by"]

        out_file_path = opts["txt_out"]
        print("Generating %s now..." % out_file_path)
        gen_data_txt(github, out_file_path, sort_by)
        print("Finished.")

    elif "txt_in" in opts and "js_out" in opts:
        github = Github(opts["token"])

        out_file_path = opts["js_out"]
        print("Generating %s now..." % out_file_path)
        gen_data_js(github, opts["txt_in"], opts["js_out"])
        print("Finished.")

    else:
        print_usage()


if __name__ == '__main__':
    main()
