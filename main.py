# coding = utf-8
import re
import csv
import json
import itertools
import scipy.stats
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn import linear_model
from pretreatment.load_data import *
from pretreatment.evaluation import *

proj_path = '/Users/DerekChiang/Documents/Github repo/social_influencer/'
datasets = ['Python_dataset/21631/', 'Python_dataset/55326/', 'Java_dataset/6273/']
dataset_path = proj_path + datasets[1]


def getBaselines(userList):

	# check input
	if not userList:
		raise TypeError('It\'s an empty user list.')

	userNum = len(userList)
	truth = [x + 1 for x in range(userNum)]	

	# initialize a table to save the results
	header = ['', 'spearman', 'kendall']
	table = list()
	table.append(header)
	

	# load repositories information
	fname = dataset_path + 'repo_info.json'	
	try:
		fhand = open(fname, 'r')
		repo_dicts = json.load(fhand)
	except:
		print('Could not read file', fname)	


	# load user information
	fname = dataset_path + 'user_info.json'	
	try:
		fhand = open(fname, 'r')
		user_dicts = json.load(fhand)
	except:
		print('Could not read file', fname)	


	# Baseline 1: # Owned repositories (binary)
	try:
		repoList = get_userInfo(userList, dataset_path, mode = 'o')
		# print([len(x) for x in repoList])
	except:
		print('Fail to load the repositories of users.')	
	else:
		own = rank_of_list([len(i) for i in repoList])
		table.append(['Owned', "{0:.6f}".format(spearman(truth, own)), "{0:.6f}".format(kendall(truth, own))])
					
	# Baseline 1: # Owned repositories (weighted)
	owned_c = [0 for x in range(userNum)]
	owned_cb = [0 for x in range(userNum)]
	owned_f = [0 for x in range(userNum)]
	owned_w = [0 for x in range(userNum)]
	owned_s = [0 for x in range(userNum)]

	for i in range(len(repoList)):
		for repo in repoList[i]:
			if repo in repo_dicts:
				owned_c[i] += repo_dicts[repo]['commits']
				owned_cb[i] += len(repo_dicts[repo]['contributors'])
				if 'stars' in repo_dicts[repo]:
					owned_f[i] += repo_dicts[repo]['forks']
					owned_w[i] += repo_dicts[repo]['watchers']
					owned_s[i] += repo_dicts[repo]['stars']
			else:
				print('Could not find owned repo', repo)			

	# with open('stars.txt', 'w') as out:
	# 	for x in owned_s:
	# 		out.write(str(x)+'\n')
		
	ownedRank_c = rank_of_list(owned_c)
	ownedRank_cb = rank_of_list(owned_cb)
	ownedRank_f = rank_of_list(owned_f)
	ownedRank_w = rank_of_list(owned_w)
	ownedRank_s = rank_of_list(owned_s)

	table.append(['Owned(c)', "{0:.6f}".format(spearman(truth, ownedRank_c)), "{0:.6f}".format(kendall(truth, ownedRank_c))])
	table.append(['Owned(cb)', "{0:.6f}".format(spearman(truth, ownedRank_cb)), "{0:.6f}".format(kendall(truth, ownedRank_cb))])
	table.append(['Owned(f)', "{0:.6f}".format(spearman(truth, ownedRank_f)), "{0:.6f}".format(kendall(truth, ownedRank_f))])
	table.append(['Owned(w)', "{0:.6f}".format(spearman(truth, ownedRank_w)), "{0:.6f}".format(kendall(truth, ownedRank_w))])
	table.append(['Owned(s)', "{0:.6f}".format(spearman(truth, ownedRank_s)), "{0:.6f}".format(kendall(truth, ownedRank_s))])
	table.append(list()) # as a blank row


	# Baseline 2: # Written repositories (binary)
	try:
		repoList = get_userInfo(userList, dataset_path, mode = 'w')
		# print([len(x) for x in repoList])
	except:
		print('Could not load the repositories of users.')	
	else:
		writtenRank = rank_of_list([len(i) for i in repoList])
		table.append(['Written', "{0:.6f}".format(spearman(truth, writtenRank)), "{0:.6f}".format(kendall(truth, writtenRank))])


	# Baseline 2: # Written repositories (weighted)
	written_c = [0 for x in range(userNum)]
	written_cb = [0 for x in range(userNum)]
	written_f = [0 for x in range(userNum)]
	written_w = [0 for x in range(userNum)]
	written_s = [0 for x in range(userNum)]
	for i in range(len(repoList)):
		for repo in repoList[i]:
			if repo in repo_dicts:
				written_c[i] += repo_dicts[repo]['commits']
				written_cb[i] += len(repo_dicts[repo]['contributors'])
				if 'stars' in repo_dicts[repo]:
					written_f[i] += repo_dicts[repo]['forks']
					written_w[i] += repo_dicts[repo]['watchers']
					written_s[i] += repo_dicts[repo]['stars']
			else:
				print('Could not find written repo', repo)	
	writtenRank_c = rank_of_list(written_c)
	writtenRank_cb = rank_of_list(written_cb)
	writtenRank_f = rank_of_list(written_f)
	writtenRank_w = rank_of_list(written_w)
	writtenRank_s = rank_of_list(written_s)

	table.append(['Written(c)', "{0:.6f}".format(spearman(truth, writtenRank_c)), "{0:.6f}".format(kendall(truth, writtenRank_c))])
	table.append(['Written(cb)', "{0:.6f}".format(spearman(truth, writtenRank_cb)), "{0:.6f}".format(kendall(truth, writtenRank_cb))])
	table.append(['Written(f)', "{0:.6f}".format(spearman(truth, writtenRank_f)), "{0:.6f}".format(kendall(truth, writtenRank_f))])
	table.append(['Written(w)', "{0:.6f}".format(spearman(truth, writtenRank_w)), "{0:.6f}".format(kendall(truth, writtenRank_w))])
	table.append(['Written(s)', "{0:.6f}".format(spearman(truth, writtenRank_s)), "{0:.6f}".format(kendall(truth, writtenRank_s))])
	table.append(list()) # as a blank row



	written_c_s = [0 for x in range(userNum)]
	for i in range(userNum):
		for repo in repoList[i]:
			if 'stars' in repo_dicts[repo]:
				val = user_dicts[userList[i]]['written repos'][repo] / repo_dicts[repo]['commits']
				weight = repo_dicts[repo]['watchers']
				written_c_s[i] += val * weight
			else:
				print(i, repo) 	

	writtenRank_c_s = rank_of_list(written_c_s)
	table.append(['Written(c_s)', "{0:.6f}".format(spearman(truth, writtenRank_c_s)), "{0:.6f}".format(kendall(truth, writtenRank_c_s))])




	# Baseline 3: # Commits
	try:
		user_commit = get_userInfo(userList, dataset_path, mode = 'c')
		# print([x for x in user_commit])
	except:
		print('Could not load the number of commits of users.')	
	else:	
		commitRank = rank_of_list(user_commit)
		table.append(['Commits', "{0:.6f}".format(spearman(truth, commitRank)), "{0:.6f}".format(kendall(truth, commitRank))])


	# Baseline 4: # Collaborators
	try:
		collabList = get_collaborators(userList, dataset_path)
	except:
		print('Could not load the number of collaborators of users.')	
	else:	
		collabRank = rank_of_list([len(i) for i in collabList])
		table.append(['Collaborators', "{0:.6f}".format(spearman(truth, collabRank)), "{0:.6f}".format(kendall(truth, collabRank))])


	# Baseline 5: # Related projects
	try:
		relatedList = get_relatedRepos(userList, dataset_path)
	except:
		print('Could not load the number of related repositories of users.')	
	else:		
		relatedRank = rank_of_list([len(i) for i in relatedList])
		table.append(['Related repos', "{0:.6f}".format(spearman(truth, relatedRank)), "{0:.6f}".format(kendall(truth, relatedRank))])
	

	return table


##################################################
################## Main Command ##################
##################################################

# top30 = top30_users(dataset_path, 'f')

# result_table  = list()
# table1 = getBaselines(top30[:10])
# table2 = getBaselines(top30[10:20])
# table3 = getBaselines(top30[:20])
# table4 = getBaselines(top30[20:30])
# table5 = getBaselines(top30)

# for r1, r2, r3, r4, r5 in zip(table1, table2, table3, table4, table5):
# 	result_table.append(r1 + r2[1:] + r3[1:] + r4[1:] + r5[1:])

# # save the result in a .csv file	
# with open('results.csv', 'w') as outfile:
# 	csvout = csv.writer(outfile)
# 	csvout.writerows(result_table)
# print("The results.csv file is written and saved.")


#################################################
################### PageRank ####################
#################################################	

# names = list()
# # load user name
# fname = dataset_path + 'userList.json'
# try:
# 	fhand = open(fname, 'r')
# 	userlist = json.load(fhand)
# except:
# 	print('Could not read file', fname)
# else:
# 	for name in userlist:
# 		names.append(name)
# 	fhand.close()


# G = nx.Graph()
# G.add_nodes_from(names)



# fname = dataset_path + 'repo_info.json'
# try:
# 	fhand = open(fname, 'r')
# 	dicts = json.load(fhand)
# except:
# 	print('Could not read file', fname)
# else:
# 	for repo in dicts:
# 		contributors = dicts[repo]['contributors']
# 		for x, y in itertools.combinations(contributors, 2):
#             # adj[x][y] = 1
#             # adj[y][x] = 1
#             # if (x in users or y in users):
# 			e = (x, y)
# 			G.add_edge(*e)
# 			# if 'weight' not in G[x][y]:
# 			# 	G[x][y]['weight'] = repo['stars'] 	
# 			# else:
# 			# 	G[x][y]['weight'] += repo['stars'] 	
          
	
# 	pr = nx.pagerank(G)

# 	top30 = top30_users(dataset_path, 'f')
# 	lists = [top30[:10], top30[10:20], top30[:20], top30[20:30], top30]
# 	for users in lists:
# 		truth = [x + 1 for x in range(len(users))]

# 		score = list()
# 		for user in users:
# 			score.append(pr[user])

# 		Rank = rank_of_list(score)
# 		print('Pagerank     : rho = %.6f, tau = %.6f, %s' % (spearman(truth, Rank), kendall(truth, Rank), Rank))
         

            
# finally:
#     fhand.close()

##################################################
########### Calulate repo correlation ############
##################################################
# stars = list()
# forks = list()
# watches = list()
# commits = list()
# contributors = list()

# # load repositories information
# fname = dataset_path + 'repo_info.json'	
# try:
# 	fhand = open(fname, 'r')
# 	repo_dicts = json.load(fhand)
# except:
# 	raise OSError('Could not read file', fname)

# s = 0
# for repo, dicts in repo_dicts.items():	
# 	if 'stars' in dicts:
# 		stars.append(dicts['stars'])
# 		forks.append(dicts['forks'])
# 		watches.append(dicts['watchers'])
# 		commits.append(dicts['commits'])
# 		contributors.append(len(dicts['contributors']))
		
# # 		# """Pearson coefficient"""
# # 		# x = load.regression_of_repos([x for x in range(21631)])
# # 		# y = load.stars_of_repos([x for x in range(21631)])
# x = stars
# y = contributors
# r, pval = scipy.stats.pearsonr(x, y)
# print("r = %.3f" % r)

""" Simple linear regression """
# ssxm, ssxym, ssyxm, ssym = np.cov(x, y, bias=1).flat
# slope, intercept, r_value, p_value, std_err_slope = scipy.stats.linregress(x, y)	
# std_err = std_err_slope * np.sqrt(len(x) * ssxm)
# hx = [xi * slope + intercept for xi in x]
# print(ssxm, ssym ,ssxym)
# print(slope, intercept, std_err)
# print(r_value) 	

# """ Multiple linear regression """
# x = [[forks[i], watches[i], commits[i], contributors[i]] for i in range(len(forks))]
# x = np.array(x)
# # x = np.array(watches)
# # x = x.reshape(len(x), 1)
# y = np.array(stars)
# y = y.reshape(len(y), 1)
# clf = linear_model.LinearRegression()
# clf.fit(x, y)
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

# file = open(dataset_path+'repoList.txt', 'w')
# fhand = open(dataset_path+'repo_info.json', 'r')
# dicts = json.load(fhand)
# i = 0
# for repo in dicts:
# 	if not 'forks' in dicts[repo]:
# 		i +=1
	# file.write(repo[0]+'\n')
# file.close()
# print(i)
# fhand.close()	



# ### new top30
# fname = dataset_path + 'repo_info.json'	
# try:
# 	fhand = open(fname, 'r')
# 	repo_dicts = json.load(fhand)
# except:
# 	print('Could not read file', fname)	


# top30 = top30_users(dataset_path)
# stars = [0 for x in range(30)]
# repoList = get_userInfo(top30, dataset_path, mode = 'o')

# for i in range(len(repoList)):
# 	for repo in repoList[i]:
# 		if repo in repo_dicts:
# 			if 'stars' in repo_dicts[repo]:
# 				stars[i] += repo_dicts[repo]['stars']
# 		else:
# 			print('Could not find owned repo', repo)	

# fhand = open(dataset_path+'top30-stars.txt', 'w')
# indices = list(range(30))
# indices.sort(key = lambda x: stars[x], reverse = True)
# print(indices)
# newtop30 = list()
# for user in indices:
# 	newtop30.append(top30[user])
# 	fhand.write(top30[user]+'\n')
# print(newtop30)




