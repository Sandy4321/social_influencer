#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import json

user_re = re.compile("^[^\(]+")


def get_file_content(path):
    """ Store every line of the file in a list and return it. """
    return [line.rstrip() for line in open(path, 'r')]


def load_all_users(path):
    """ Load all users from the specified dataset. """
    return get_file_content(path + "userList.txt")


def load_top30_users(path, rank='s'):
    """ Return the top 30 users from the specified dataset.

    @Parameters
    -----------
    path : string
        The path of the dataset.

    rank : string
        The method to rank the developers on Github.
        's' : # of total repository stars (default)
        'a' : the rank on Git award website
        'f' : # of total followers

    @Returns
    --------
    users : list
        A top 30 user list.

    """

    # Check the rank method
    if rank == 's':
        path += 'top30-stars.txt'
    elif rank == 'a':
        path += 'top30-award.txt'
    elif rank == 'f':
        path += 'top30-followers.txt'

    return get_file_content(path)


def get_user_info(user_list, path, mode='o'):
    """ Get the user information.

    @Parameters
    -----------
    user_list : list
        The input user list.

    path : string
        The path of the dataset.

    mode = string
        The user information you want to return.
        'o' : owned repositories of users (default)
        'w' : written repositories of users
        'c' : # of commits of users

    @Returns
    --------
    info_list : list
        The returned information of users.

    """
    user_dict = json.load(open(path + "user_info.json", 'r'))

    # Check if all the users exist
    for user in user_list:
        if user not in user_dict:
            raise ValueError('Could not find user', user)

    # Check the target information
    target = ""
    if mode == 'o':
        target = "owned repos"
    elif mode == 'w':
        target = "written repos"
    elif mode == 'c':
        target = "commits"

    info_list = [user_dict[user][target] for user in user_list]
    return info_list


def get_repo_info(repo_list, path, mode='c'):
    """ Get repository information.

    @Parameters
    -----------
    repo_list : list
        The input repo list.

    path : string
        The path of the dataset.

    mode : string
        The repository information you want to return.
        'c' : # of commits of repo (default)
        'cb' : # of contributors of repo
        'f' : # of forks of repo
        'w' : # of watchers of repo
        's' : # of stars of repo

    @Returns
    --------
    info_ist : list
        The returned information of repositories.

    """

    repo_dict = json.load(open(path + 'repo_info.json', 'r'))

    # Check if all the repositories exist
    for repo in repo_list:
        if repo not in repo_dict:
            raise ValueError('Could not find repo', repo)

    # Check the target information
    target = ""
    if mode == 'c':
        target = "commits"
    elif mode == 'cb':
        target = "contributors"
    elif mode == 'f':
        target = "forks"
    elif mode == 'w':
        target = "watchers"
    elif mode == 's':
        target = "stars"

    info_list = [repo_dict[repo][target] for repo in repo_list]
    return info_list


def get_collaborators(user_list, path):
    """ Find the collaborators of users.

    @Parameters
    -----------
    user_list : list
        The input user list.

    path : string
        The path of the dataset.

    @Returns
    --------
    collab_list : list
        The collaborators of each user.

    """

    N = len(user_list)
    collab_list = [set() for x in range(N)]

    # Get the written repositories of all users
    written_repo_list = get_user_info(user_list, path, mode='w')

    fhand = open(path + 'commitLog.txt', 'r')
    for line in fhand:
        log = line.split()
        m = re.search(user_re, log[0])

        user = m.group(0)
        repo = log[1]
        for i in range(N):
            if repo in written_repo_list[i] and user != user_list[i]:
                collab_list[i].add(user)

    return(collab_list)


def get_related_repos(user_list, path):
    """ Find the related repositories of users.

    @Parameters
    -----------
    user_list : list
        The input user list.

    path : string
        The path of the dataset.

    @Returns
    --------
    related_repo_list : list
        The related repositories of each user.

    """

    N = len(user_list)
    related_list = [set() for x in range(N)]

    repo_list = get_user_info(user_list, path, mode='w')
    collab_list = get_collaborators(user_list, path)

    fhand = open(path + 'commitLog.txt', 'r')
    for line in fhand:
        log = line.split()
        m = re.search(user_re, log[0])

        user = m.group(0)
        repo = log[1]
        for i in range(N):
            if (user in collab_list[i] and repo not in repo_list[i]):
                related_list[i].add(repo)

    return(related_list)


if __name__ == "__main__":
    s = "A-Circle-Zhang(11173242) ykdl(832666) 1"
    m = re.search(user_re, s)
    print(m.group(0))
