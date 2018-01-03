#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import os
import json

dirpath = os.getcwd() + '/../data/'
datasets = ['Python_dataset/21631/', 'Python_dataset/55326/', 'Java_dataset/6273/']
data_path = dirpath + datasets[0]


def save_user_info(path):
    """ Save user information into json format. """

    # Load user name and id
    id_dict = json.load(open(path + 'userList.json', 'r'))

    # Initialize user information
    user_info = dict()
    for user, id_num in id_dict.items():
        user_info[user] = {
            "id": id_num,
            "written repos": dict(),
            "owned repos": list(),
            "commits": 0
        }

    # Load user owned repositories
    fhand = open(path + 'repoList.txt', 'r')
    for line in fhand:
        owner = re.findall('(^.*)/', line)[0]
        repo = re.findall('/(.*)', line)[0]

        if owner not in id_dict:
            print('Could not find user', owner)
        else:
            repo_name = repo + '(' + str(id_dict[owner]) + ')'
            user_info[owner]['owned repos'].append(repo_name)

    # Load user written repositories
    fhand = open(path + 'commitLog.txt', 'r')
    for line in fhand:
        log = line.split()
        user = re.findall('(^.*)\(', log[0])[0]
        id_num = int(re.findall('\((.*?)\)', log[0])[0])
        repo = log[1]
        commit = int(log[2])

        if user in user_info and user_info[user]['id'] == id_num:
            user_info[user]['written repos'][repo] = commit
            user_info[user]['commits'] += commit

    # Save information into "user_info.json" file
    with open(path + "user_info.json", 'w') as outfile:
        json.dump(user_info, outfile, indent=4, sort_keys=True, separators=(',', ':'))
    outfile.closed
    print("The user_info.json file is written and saved.")


def save_repo_info(path):
    """ Save repo information into json format. """

    # Load user name and id
    id_dict = json.load(open(path + 'userList.json', 'r'))

    # Initialize a dict to store repository information
    repo_info = dict()
    fhand = open(path + 'repoList.txt', 'r')
    for line in fhand:
        owner = re.findall('(^.*)/', line)[0]
        repo_name = re.findall('/(.*)', line)[0]
        if owner not in id_dict:
            print('Could not find user', owner)
        else:
            repo = {
                'repo_name': repo_name,
                'owner': owner,
                'contributors': list(),
                'commits': 0,
                'id': id_dict[owner]
            }
            repo_full_name = repo_name + '(' + str(id_dict[owner]) + ')'
            repo_info[repo_full_name] = repo

    # Load repo information
    fhand = open(path + 'repos_info.txt', 'r')
    for line in fhand:
        owner = re.findall('(^.*)/', line)
        repo = re.findall('/(.*?):', line)
        star = re.findall(':(.*?),', line)
        fork = re.findall(',(.*?),', line)
        watch = re.findall('^.*,(.*)', line)
        if all(len(x) == 1 for x in (owner, repo, star, fork, watch)):
            if owner[0] not in id_dict:
                print('Could not find user', owner[0])
            else:
                id_string = str(id_dict[owner[0]])
                repo_name = repo[0] + '(' + id_string + ')'
                if repo_name in repo_info:
                    repo_info[repo_name]['stars'] = int(star[0])
                    repo_info[repo_name]['forks'] = int(fork[0])
                    repo_info[repo_name]['watchers'] = int(watch[0])
                else:
                    print('Could not find repo', repo_name)
        else:
            print('Invalid format in repos_info.txt', line)

    # Load contributors and commits of repos
    fhand = open(path + 'commitLog.txt', 'r')
    for line in fhand:
        log = line.split()
        user = re.findall('(^.*)\(', log[0])[0]
        repo = log[1]
        commit = int(log[2])
        if repo in repo_info:
            repo_info[repo]['contributors'].append(user)
            repo_info[repo]['commits'] += commit

    # Save information into "repo_info.json" file
    with open(path + 'repo_info.json', 'w') as outfile:
        json.dump(repo_info, outfile, indent=4, sort_keys=True, separators=(',', ':'))
    outfile.closed
    print("The repo_info.json file is written and saved.")


def main():
    print('The dataset you are saving is', data_path)
    # save_user_info(data_path)
    # save_repo_info(data_path)


if __name__ == '__main__':
    main()
