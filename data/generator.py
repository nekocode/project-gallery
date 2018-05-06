#!/usr/bin/env python
# -*- coding: utf-8 -*-
from github import Github
import os.path
import getopt
import sys
import json


def to_repo(github_repo):
    return {
        'type': 'repo',
        'name': github_repo.name,
        'description': github_repo.description,
        'stars': github_repo.stargazers_count,
        'forks': github_repo.forks_count,
        'lang': github_repo.language,
        'url': github_repo.html_url,
    }


def main():
    def print_usage():
        print('usage: %s --token=GITHUB_TOKEN \n\t (--json=JSON_PATH)' % __file__)

    opts, args = getopt.getopt(sys.argv[1:], '', ['token=', 'json='])
    opts = {opt[0][2:]: opt[1] for opt in opts}  # Convert to a dict

    token = opts['token']
    if token is None:
        print_usage()
        return

    json_file = opts['json']
    if json_file is None:
        opts['json'] = 'data.json'

    print('Reading data from github...')
    github_user = Github(token).get_user()
    github_repos = [r for r in github_user.get_repos('owner')]
    github_repos.extend([r for r in github_user.get_repos('member')])
    github_repos = {repo.name: repo for repo in github_repos}  # Convert to a dict

    old_dict = {}
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                old_dict = json.load(f)
                print('Loaded old data from "%s"' % json_file)
        except Exception:
            old_dict = {}

    print('Restructuring data...')
    config = {
        'title': github_user.name,
        'github': github_user.html_url,
        'description': 'Here are the projects I have open sourced.',
        'footer': github_user.name
    }
    repos = []

    # Config
    if 'config' in old_dict:
        old_config = old_dict['config']
        if 'title' in old_config:
            config['title'] = old_config['title']

        config['github'] = github_user.html_url

        if 'description' in old_config:
            config['description'] = old_config['description']

        if 'footer' in old_config:
            config['footer'] = old_config['footer']

    # Repos
    if 'repos' in old_dict:
        old_repos = old_dict['repos']

        for repo in old_repos:
            if 'type' not in repo or 'name' not in repo:
                continue  # Skip this broken repo

            t = repo['type']
            if t == 'category':
                # Category
                repos.append(repo)
                continue

            if t != 'repo':
                continue  # Skip unknown type

            n = repo['name']
            if n not in github_repos:
                continue  # Skip the removed repo

            repos.append(to_repo(github_repos[n]))
            github_repos.pop(n)  # Remove from dict

    github_repos = [repo for repo in github_repos.values()]  # Dict to list

    if len(github_repos) != 0:
        github_repos = sorted(github_repos, key=lambda x: x.stargazers_count, reverse=True)  # Sort by stargazers count

        repos.append({
            'type': 'category',
            'name': 'Uncategorized',
        })
        for repo in github_repos:
            repos.append(to_repo(repo))

    # Write to file
    print('Saving data to "%s"...' % json_file)
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps({
            'config': config,
            'repos': repos
        }, indent=4, sort_keys=True))

    print('Done')

if __name__ == '__main__':
    main()
