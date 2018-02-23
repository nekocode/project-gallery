#!/usr/bin/env python
# -*- coding: utf-8 -*-
from github import Github
import os.path
import getopt
import sys


def str_ui(name, url):
    return """
var UI_DATA = {
    "title": "%s",
    "github": "%s",
    "description": "Here are the projects I have open sourced.",
    "footer": "%s"
}
"""[1:] % (name, url, name)


def str_wrap_list(list_str):
    return """
var LIST_DATA = [
%s
]
"""[1:] % list_str


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


def gen_ui_data_js(github, out_file_path):
    user = github.get_user()

    with open(out_file_path, 'w') as f:
        f.write(str_ui(user.name, user.html_url))


def gen_items_data_txt(github, out_file_path, sort_by=None):
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


def gen_items_data_js(github, in_file_path, out_file_path):
    if not os.path.exists(in_file_path):
        return

    user = github.get_user()
    repos = user.get_repos("owner")
    repos = {repo.name: repo for repo in repos}  # Convert to a dict

    with open(in_file_path, "r") as txt, open(out_file_path, 'wb') as js:
        def write(content):
            js.write(content.encode('utf-8'))

        # write(str_user(user.avatar_url, user.name, user.html_url) + "\n")

        list_str = ""
        for line in txt:
            line = line.strip()
            if line.startswith("//"):
                category_name = line[2:].lstrip()
                list_str += str_category_item(category_name)

            elif len(line) > 0:
                repo_name = line.split(",")[0].rstrip()
                if repo_name in repos:
                    repo = repos[repo_name]
                    list_str += str_repo_item(
                        repo.name, repo.description,
                        repo.stargazers_count, repo.forks_count, repo.language,
                        repo.html_url
                    )

        write(str_wrap_list(list_str))


def main():
    def print_usage():
        print("usage: %s --token=GITHUB_TOKEN \n\t" % __file__ +
              "(--list_txt_out=TXT_OUT [--sort_by=stars|name]) | \n\t" +
              "(--list_txt_in=TXT_IN --list_js_out=JS_OUT) | \n\t" +
              "(--ui_js_out=JS_OUT)"
              )

    opts, args = getopt.getopt(
        sys.argv[1:], "", ["token=", "list_txt_out=", "list_txt_in=", "list_js_out=", "sort_by=", "ui_js_out="])
    opts = {opt[0][2:]: opt[1] for opt in opts}
    if "token" not in opts:
        print_usage()
        return

    if "list_txt_out" in opts:
        github = Github(opts["token"])
        sort_by = "stars"
        if "sort_by" in opts:
            sort_by = opts["sort_by"]

        out_file_path = opts["list_txt_out"]
        print("Generating %s now..." % out_file_path)
        gen_items_data_txt(github, out_file_path, sort_by)
        print("Finished.")

    elif "list_txt_in" in opts and "list_js_out" in opts:
        github = Github(opts["token"])

        out_file_path = opts["list_js_out"]
        print("Generating %s now..." % out_file_path)
        gen_items_data_js(github, opts["list_txt_in"], out_file_path)
        print("Finished.")

    elif "ui_js_out" in opts:
        github = Github(opts["token"])

        out_file_path = opts["ui_js_out"]
        print("Generating %s now..." % out_file_path)
        gen_ui_data_js(github, out_file_path)
        print("Finished.")

    else:
        print_usage()


if __name__ == '__main__':
    main()
