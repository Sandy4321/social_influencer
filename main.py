#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv
import json
import itertools
import scipy.stats
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn import linear_model
from preprocess.load_data import *
from preprocess.eval import *

dirpath = '/Users/DerekChiang/Desktop/MyRepo/Python/social_influencer/data/'
datasets = ['Python_dataset/21631/',
            'Python_dataset/55326/',
            'Java_dataset/6273/']
data_path = dirpath + datasets[0]


def calcRepoScore(userlist, repo_mode='o', value='b', weight='wo'):
    """ Calculate the scores of users based on their repositories.

    @Parameters
    -----------
    userlist : list
        Input user list.

    repo = 'o' : use owned repositories as the information of users
           'w' : use written repositories as the information of users

    value = 'b': put binary (0 or 1) inside the user-repo matrix
            'p': put commit percentage inside the user-repo matrix

    weight = 'wo': without weight
             'w' : number of watches
             'f' : number of forks
             's' : number of stars
             'cm': number of commits
             'cb': number of contributors

    @Returns
    --------
    scorelist : list
        Output the scores of users.

    """

    # Load user and repo information
    user_dicts = json.load(open(data_path + 'user_info.json', 'r'))
    repo_dicts = json.load(open(data_path + 'repo_info.json', 'r'))

    # Initialization
    userNum = len(userlist)
    scorelist = [0 for x in range(userNum)]

    # Check the type of repository to use as score calculation
    repolist = get_user_info(userlist, data_path, mode=repo_mode)

    # Check the weight of the repo
    for i in range(userNum):
        for repo in repolist[i]:
            if weight == 'wo':
                if value == 'b':
                    scorelist[i] += 1
                elif value == 'p':
                    if repo in user_dicts[userlist[i]]['written repos']:
                        commit_perc = user_dicts[userlist[i]]['written repos'][repo] / repo_dicts[repo]['commits']
                        scorelist[i] += commit_perc

            elif weight == 'w':
                if 'watchers' in repo_dicts[repo]:
                    if value == 'b':
                        scorelist[i] += repo_dicts[repo]['watchers']
                    elif value == 'p':
                        if repo in user_dicts[userlist[i]]['written repos']:
                            commit_perc = user_dicts[userlist[i]]['written repos'][repo] / repo_dicts[repo]['commits']
                            scorelist[i] += commit_perc * repo_dicts[repo]['watchers']

            elif weight == 'f':
                if 'forks' in repo_dicts[repo]:
                    if value == 'b':
                        scorelist[i] += repo_dicts[repo]['forks']
                    elif value == 'p':
                        if repo in user_dicts[userlist[i]]['written repos']:
                            commit_perc = user_dicts[userlist[i]]['written repos'][repo] / repo_dicts[repo]['commits']
                            scorelist[i] += commit_perc * repo_dicts[repo]['forks']

            elif weight == 's':
                if 'stars' in repo_dicts[repo]:
                    if value == 'b':
                        scorelist[i] += repo_dicts[repo]['stars']
                    elif value == 'p':
                        if repo in user_dicts[userlist[i]]['written repos']:
                            commit_perc = user_dicts[userlist[i]]['written repos'][repo] / repo_dicts[repo]['commits']
                            scorelist[i] += commit_perc * repo_dicts[repo]['stars']

            elif weight == 'cm':
                if value == 'b':
                    scorelist[i] += repo_dicts[repo]['commits']
                elif value == 'p':
                    if repo in user_dicts[userlist[i]]['written repos']:
                        commit_perc = user_dicts[userlist[i]]['written repos'][repo] / repo_dicts[repo]['commits']
                        scorelist[i] += commit_perc * repo_dicts[repo]['commits']

            elif weight == 'cb':
                if value == 'b':
                    scorelist[i] += len(repo_dicts[repo]['contributors'])
                elif value == 'p':
                    if repo in user_dicts[userlist[i]]['written repos']:
                        commit_perc = user_dicts[userlist[i]]['written repos'][repo] / repo_dicts[repo]['commits']
                        scorelist[i] += commit_perc * len(repo_dicts[repo]['contributors'])

    return scorelist


def getBaselines(userlist):

    # Initialize a table to save the results
    header = ['', 'spearman', 'kendall']
    table = list()
    table.append(header)

    # Different parameter settings
    values = ['b', 'p']
    weights = ['wo', 'cm', 'cb', 'f', 'w', 's']
    truth = [x + 1 for x in range(len(userlist))]

    # Baseline 1: # of owned repositories
    for v, w in itertools.product(values, weights):
        result = calcRepoScore(userlist, repo_mode='o', value=v, weight=w)
        rank = rank_of_list(result)
        table.append(['Owned(' + w + ')', "{0:.6f}".format(spearman(truth, rank)),
                      "{0:.6f}".format(kendall(truth, rank))])
    table.append(list())  # Append a blank row

    # Baseline 2: # Written repositories
    for v, w in itertools.product(values, weights):
        result = calcRepoScore(userlist, repo_mode='w', value=v, weight=w)
        rank = rank_of_list(result)
        table.append(['Written(' + w + ')', "{0:.6f}".format(spearman(truth, rank)),
                      "{0:.6f}".format(kendall(truth, rank))])
    table.append(list())  # Append a blank row

    # Baseline 3: # of commits
    commit_list = get_user_info(userlist, data_path, mode='c')
    commit_rank = rank_of_list(commit_list)
    table.append(['Commits', "{0:.6f}".format(spearman(truth, commit_rank)),
                  "{0:.6f}".format(kendall(truth, commit_rank))])

    # Baseline 4: # of collaborators
    collab_list = get_collaborators(userlist, data_path)
    collab_rank = rank_of_list([len(i) for i in collab_list])
    table.append(['Collaborators', "{0:.6f}".format(spearman(truth, collab_rank)),
                  "{0:.6f}".format(kendall(truth, collab_rank))])

    # Baseline 5: # of related projects
    relate_list = get_related_repos(userlist, data_path)
    relate_rank = rank_of_list([len(i) for i in relate_list])
    table.append(['Related repos', "{0:.6f}".format(spearman(truth, relate_rank)),
                  "{0:.6f}".format(kendall(truth, relate_rank))])

    return table


if __name__ == "__main__":

    # ----------------------------------------------------------
    # ----------------------------------------------------------
    # ---------- Run baselines 1 to 5 --------------------------
    # ----------------------------------------------------------
    # ----------------------------------------------------------
    users = load_all_users(data_path)
    top30 = load_top30_users(data_path, 'a')

    # Save all the results in a single table
    result_table = list()
    result_01to10 = getBaselines(top30[:10])
    result_11to20 = getBaselines(top30[10:20])
    result_01to20 = getBaselines(top30[:20])
    result_21to30 = getBaselines(top30[20:30])
    result_01to30 = getBaselines(top30)
    for r1, r2, r3, r4, r5 in zip(result_01to10, result_11to20, result_01to20, result_21to30, result_01to30):
        result_table.append(r1 + r2[1:] + r3[1:] + r4[1:] + r5[1:])

    # Output results into a .csv file
    with open('results2.csv', 'w') as outfile:
        csvout = csv.writer(outfile)
        csvout.writerows(result_table)
    print("The results.csv file is written and saved.")

    # ----------------------------------------------------------
    # ----------------------------------------------------------
    # ---------- Run PageRank ----------------------------------
    # ----------------------------------------------------------
    # ----------------------------------------------------------
    # Load all the users and create a graph
    userlist = json.load(open(data_path + 'userList.json', 'r'))
    G = nx.Graph()
    G.add_nodes_from(userlist.keys())

    dicts = json.load(open(data_path + 'repo_info.json', 'r'))
    for repo in dicts:
        contributors = dicts[repo]['contributors']
        for x, y in itertools.combinations(contributors, 2):
            e = (x, y)
            G.add_edge(*e)
            # if 'weight' not in G[x][y]:
            #   G[x][y]['weight'] = repo['stars']
            # else:
            #   G[x][y]['weight'] += repo['stars']

    pr = nx.pagerank(G)

    target_users = [top30[:10], top30[10:20], top30[:20], top30[20:30], top30]
    for user_list in target_users:
        scores = [pr[user] for user in user_list]
        pr_rank = rank_of_list(scores)
        print('Pagerank     : rho = %.6f, tau = %.6f, %s' %
              (spearman(truth, pr_rank), kendall(truth, pr_rank), pr_rank))

    # ----------------------------------------------------------
    # ----------------------------------------------------------
    # ---------- Compute correlation ---------------------------
    # ----------------------------------------------------------
    # ----------------------------------------------------------
    # stars = list()
    # forks = list()
    # watches = list()
    # commits = list()
    # contributors = list()

    # Load repositories information
    # repo_dicts = json.load(open(data_path + 'repo_info.json', 'r'))

    # for repo, dicts in repo_dicts.items():
    #     if 'stars' in dicts:
    #         stars.append(dicts['stars'])
    #         forks.append(dicts['forks'])
    #         watches.append(dicts['watchers'])
    #         commits.append(dicts['commits'])
    #         contributors.append(len(dicts['contributors']))

    # x = stars
    # y = contributors
    # r, pval = scipy.stats.pearsonr(x, y)
    # print("r = %.3f" % r)

    # Simple linear regression
    # ssxm, ssxym, ssyxm, ssym = np.cov(x, y, bias=1).flat
    # slope, intercept, r_value, p_value, std_err_slope = scipy.stats.linregress(x, y)
    # std_err = std_err_slope * np.sqrt(len(x) * ssxm)
    # hx = [xi * slope + intercept for xi in x]
    # print(ssxm, ssym, ssxym)
    # print(slope, intercept, std_err)
    # print(r_value)

    # Multiple linear regression
    # x = [[forks[i], watches[i], commits[i], contributors[i]] for i in range(len(forks))]
    # x = np.array(x)
    # x = np.array(watches)
    # x = x.reshape(len(x), 1)
    # y = np.array(stars)
    # y = y.reshape(len(y), 1)
    # clf = linear_model.LinearRegression().fit(x, y)
    # print(clf.coef_)
    # print(np.sqrt(clf.residues_ / (len(stars)-2)))
    # print(clf.intercept_)
    # y_est = clf.predict(x)
    # print(y_est)

    # """ Display the plot """
    # inx = np.argsort(x)
    # xs = np.array(x)[inx]
    # hxs = np.array(hx)[inx]
    # ys = np.array(y)[inx]
    # x_max = np.amax(xs)
    # y_max = np.amax(ys)
    # x_min = np.amin(xs)
    # y_min = np.amin(ys)
    # axes = plt.gca()
    # axes.set_xlim([x_min,x_max])
    # axes.set_ylim([y_min,y_max])
    # plt.scatter(xs, ys, label = 'Data sets (21516)')
    # plt.scatter(xs, hxs, color = 'red', label = 'Estimated values')
    # plt.plot(xs, slope*xs + intercept, color = 'red', label = 'Regrssion line', linewidth = 2)
    # plt.xlabel('# of contributors')
    # plt.ylabel('# of stars')
    # plt.title(r'Contributor-star distribution:')
    # plt.legend(loc = 'lower right')
    # plt.show()
