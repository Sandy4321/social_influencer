import load_data as load
import evaluation as eva
import json
import itertools
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import networkx as nx
import re



##################################################
################### Load data ####################
##################################################
userList = load.top10_users()
userNum = len(userList)
truth = [x + 1 for x in range(userNum)]



##################################################
########## Baseline 1: # Owned projects ##########
##################################################
# Binary version of owned repos 
try:
	repoList = load.getRepos(userList, 'o')
except:
	print('Could not load the repositories of users.')	
else:
	print([len(i) for i in repoList])
	ownedRank = eva.rank_of_list([len(i) for i in repoList])
	print(scipy.stats.spearmanr(truth, ownedRank))
	print('Owned     : rho = %.6f, tau = %.6f, %s' % (eva.spearman(ownedRank, truth), eva.kendall(ownedRank, truth), ownedRank))


# # Weighted version(# commits) of owned repos 
# owned_c = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.commits_of_repos([x for x in range(21631)])
# except:
# 	print('Could not load the number of commits of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			owned_c[i] = owned_c[i] + repo_weight[repo]	
# 	ownedRank_c = eva.rank_of_list(owned_c)
# 	print("Owned(c)  : rho = %.6f, tau = %.6f, %s" % (eva.Spearman(truth, ownedRank_c), eva.Kendall(truth, ownedRank_c), ownedRank_c))


# # Weighted version(# contributors) of owned repos 
# owned_cb = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.contributors_of_repos([x for x in range(21631)])
# except:
# 	print('Could not load the number of contributors of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			owned_cb[i] = owned_cb[i] + repo_weight[repo]	
# 	ownedRank_cb = eva.rank_of_list(owned_cb)
# 	print("Owned(cb) : rho = %.6f, tau = %.6f, %s" % (eva.Spearman(truth, ownedRank_cb), eva.Kendall(truth, ownedRank_cb), ownedRank_cb))


# # Weighted version(# forks) of owned repos 
# owned_f = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.forks_of_repos([x for x in range(21631)])
# 	# print(repo_weight)
# except:
# 	print('Could not load the number of forks of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			owned_f[i] = owned_f[i] + repo_weight[repo]
# 	ownedRank_f = eva.rank_of_list(owned_f)
# 	print("Owned(f)  : rho = %.6f, tau = %.6f, %s" % (eva.Spearman(truth, ownedRank_f), eva.Kendall(truth, ownedRank_f), ownedRank_f))


# # Weighted version(# watches) of owned repos 
# owned_w = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.watches_of_repos([x for x in range(21631)])
# 	# print(repo_weight)
# except:
# 	print('Could not load the number of watches of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			owned_w[i] = owned_w[i] + repo_weight[repo]	
# 	ownedRank_w = eva.rank_of_list(owned_w)
# 	print("Owned(w)  : rho = %.6f, tau = %.6f, %s" % (eva.Spearman(truth, ownedRank_w), eva.Kendall(truth, ownedRank_w), ownedRank_w))


# # Weighted version(# stars) of owned repos 
# owned_s = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.stars_of_repos([x for x in range(21631)])
# 	# print(repo_weight)
# except:
# 	print('Could not load the number of stars of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			owned_s[i] = owned_s[i] + repo_weight[repo]	
# 	ownedRank_s = eva.rank_of_list(owned_s)
# 	print("Owned(s)  : rho = %.6f, tau = %.6f, %s" % (eva.Spearman(truth, ownedRank_s), eva.Kendall(truth, ownedRank_s), ownedRank_s))

# # Weighted version(regression value) of owned repos 
# owned_r = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.regression_of_repos([x for x in range(21631)])
# 	# print(repo_weight)
# except:
# 	print('Could not load the number of stars of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			owned_r[i] = owned_r[i] + repo_weight[repo]	
# 	ownedRank_r = eva.rank_of_list(owned_r)
# 	print("Owned(r)  : rho = %.6f, tau = %.6f, %s" %(eva.Spearman(truth, ownedRank_r), eva.Kendall(truth, ownedRank_r), ownedRank_r))



##################################################
######### Baseline 2: # Written projects #########
##################################################
# # Binary version of written repos 
# try:
# 	repoList = load.written_repos(userList)
# except:
# 	print('Could not load the repositories of users.')	
# else:
# 	# print([len(i) for i in repoList])
# 	writtenRank = eva.rank_of_list([len(i) for i in repoList])
# 	print('Written   : rho = %.6f, tau = %.6f, %s' % (eva.Spearman(truth, writtenRank), eva.Kendall(truth, writtenRank), writtenRank))


# # Weighted version(# commits) of written repos 
# written_c = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.commits_of_repos([x for x in range(21631)])
# except:
# 	print('Could not load the number of commits of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			written_c[i] = written_c[i] + repo_weight[repo]	
# 	writtenRank_c = eva.rank_of_list(written_c)
# 	print("Written(c)  : rho = %.6f, tau = %.6f, %s" %(eva.Spearman(truth, writtenRank_c), eva.Kendall(truth, writtenRank_c), writtenRank_c))


# # Weighted version(# contributors) of written repos 
# written_cb = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.contributors_of_repos([x for x in range(21631)])
# except:
# 	print('Could not load the number of contributors of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			written_cb[i] = written_cb[i] + repo_weight[repo]	
# 	writtenRank_cb = eva.rank_of_list(written_cb)
# 	print("Written(cb)  : rho = %.6f, tau = %.6f, %s" %(eva.Spearman(truth, writtenRank_cb), eva.Kendall(truth, writtenRank_cb), writtenRank_cb))


# # Weighted version(# forks) of written repos 
# written_f = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.forks_of_repos([x for x in range(21631)])
# 	# print(repo_weight)
# except:
# 	print('Could not load the number of forks of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			written_f[i] = written_f[i] + repo_weight[repo]
# 	writtenRank_f = eva.rank_of_list(written_f)
# 	print("Written(f)  : rho = %.6f, tau = %.6f, %s" %(eva.Spearman(truth, writtenRank_f), eva.Kendall(truth, writtenRank_f), writtenRank_f))


# # Weighted version(# watches) of written repos 
# written_w = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.watches_of_repos([x for x in range(21631)])
# 	# print(repo_weight)
# except:
# 	print('Could not load the number of watches of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			written_w[i] = written_w[i] + repo_weight[repo]	
# 	writtenRank_w = eva.rank_of_list(written_w)
# 	print("Written(w)  : rho = %.6f, tau = %.6f, %s" %(eva.Spearman(truth, writtenRank_w), eva.Kendall(truth, writtenRank_w), writtenRank_w))


# # Weighted version(# stars) of written repos 
# written_s = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.stars_of_repos([x for x in range(21631)])
# 	# print(repo_weight)
# except:
# 	print('Could not load the number of stars of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			written_s[i] = written_s[i] + repo_weight[repo]	
# 	writtenRank_s = eva.rank_of_list(written_s)
# 	print("Written(s)  : rho = %.6f, tau = %.6f, %s" %(eva.Spearman(truth, writtenRank_s), eva.Kendall(truth, writtenRank_s), writtenRank_s))

# # Weighted version(regression value) of written repos 
# written_r = [0 for x in range(userNum)]
# try:
# 	repo_weight = load.regression_of_repos([x for x in range(21631)])
# 	# print(repo_weight)
# except:
# 	print('Could not load the number of stars of repositories.')	
# else:	
# 	for i in range(userNum):
# 		for repo in repoList[i]:
# 			written_r[i] = written_r[i] + repo_weight[repo]	
# 	writtenRank_r = eva.rank_of_list(written_r)
# 	print("Written(r)  : rho = %.6f, tau = %.6f, %s" %(eva.Spearman(truth, writtenRank_r), eva.Kendall(truth, writtenRank_r), writtenRank_r))



##################################################
############# Eliminate commit <= 10 #############
##################################################
# repo_weight = [0 for x in range(21631)]
# for i in range(len(repo_commit)):
# 	if repo_commit[i] >= 10:
# 		repo_weight[i] = 1 
#print(repo_weight)

# new_writtenList = [0 for x in range(userNum)]
# for i in range(len(repoList)):
# 	for repo in repoList[i]:
# 		if repo_weight[repo] == 1:
# 			new_writtenList[i] = new_writtenList[i] + 1 
#print(new_writtenList)	
# b2 = eva.rank_of_list(new_writtenList)
# print("New_Written : rho = %s, tau = %s, %s" %(eva.Spearman(truth, b2), eva.Kendall(truth, b2), b2))

# new_user_score = [0 for x in range(userNum)]
# for i in range(userNum):
# 	for repo in repoList[i]:
# 		if repo_weight[repo] == 1:
# 			new_user_score[i] = new_user_score[i] + repo_commit[repo]	
# #print(new_user_score)		
# c2 = eva.rank_of_list(new_user_score)
# print("Written(we) : rho = %s, tau = %s, %s" %(eva.Spearman(truth, c2), eva.Kendall(truth, c2), c2))


##################################################
############# Baseline 3: # Commits ##############
##################################################
#user_commit = load.commits_of_users(userList)
# commitRank = eva.rank_of_list(user_commit)
# print("Commits     : rho = %s, tau = %s, %s" %(eva.Spearman(truth, commitRank), eva.Kendall(truth, commitRank), commitRank))


##################################################
######## Other Baseline : # Collaborators ########
##################################################
collabList = load.collab_of_users(userList)
collabRank = eva.rank_of_list([len(i) for i in collabList])
print("Collaborator: rho = %s, tau = %s, %s" %(eva.spearman(truth, collabRank), eva.kendall(truth, collabRank), collabRank))


##################################################
###### Other Baseline : # Related projects #######
##################################################
# relatedList = load.related_repo_of_users(userList, repoList, collabList)
# relatedRank = eva.rank_of_list([len(i) for i in relatedList])
# print("Related repo: rho = %s, tau = %s, %s" %(eva.Spearman(truth, relatedRank), eva.Kendall(truth, relatedRank), relatedRank))	


######################################################
## Find the number of top 10/20 collaborators  ##
######################################################
# for i in range(0, userNum):	
# 	t = 0
# 	for collab in user_info[i][2]:
# 		if collab in top20:
# 			t = t + 1
# 	print(t)	
	
##################################################
#################### PageRank ####################
##################################################	

# G = nx.Graph()
# G.add_nodes_from([x for x in range(3895)])


# fname = 'Python_dataset/repo_info.json'
# try:
# 	fhand = open(fname, 'r')
# except:
# 	print('Could not read file', fname)
# else:
# 	repos = json.load(fhand)
# 	for repo in repos:
# 		contributors = repo['contributors']
# 		for x, y in itertools.combinations(contributors, 2):
#             # adj[x][y] = 1
#             # adj[y][x] = 1
#             # if (x in users or y in users):
# 			e = (x, y)
# 			G.add_edge(*e)
# 			if 'weight' not in G[x][y]:
# 				if 'stars' not in repo:
# 					estimate_star = 40.244 * len(contributors) - 22.605
# 					if estimate_star < 0.0:
# 						estimate_star = 0.0
# 					G[x][y]['weight'] = estimate_star
# 				else:
# 					G[x][y]['weight'] = repo['stars'] 	
# 			else:
# 				if 'stars' not in repo:
# 					estimate_star = 40.244 * len(contributors) - 22.605
# 					if estimate_star < 0.0:
# 						estimate_star = 0.0
# 					G[x][y]['weight'] += estimate_star
# 				else:
# 					G[x][y]['weight'] += repo['stars'] 	
          
# 	score = list()
# 	pr = nx.pagerank(G, weight='weight')
# 	for user in userList:
# 		score.append(pr[user])
# 	index = 0;	
# 	for s in score:
# 		index+=1 
# 		print(index, ':', s)

# 	Rank = eva.rank_of_list(score)
# 	print('Pagerank     : rho = %.6f, tau = %.6f, %s' % (eva.Spearman(truth, Rank), eva.Kendall(truth, Rank), Rank))
         

            
# finally:
#     fhand.close()



##################################################
#################### FM Model ####################
##################################################
# fm = [307.03, 285.17, 152.46, 58.27, 50.09,  28.19,  30.39, 23.25,  16.6,  16.23, 
# 	   39.91,  22.09,  24.62,  8.86, 11.23, 231.91,  18.34, 37.11, 11.69, 110.19, 
# 	   10.68,  10.97,  63.06, 14.63, 163.7,   95.2, 100.31, 34.28, 47.06, 313.48]

# fm = fm[:30]
# ff = eva.rank_of_list(fm)
# print("FM          : rho = %s, tau = %s, %s" %(eva.Spearman(truth, ff), eva.Kendall(truth, ff), ff))	


##################################################
########### Calulate repo correlation ############
##################################################
# fname = 'Python_dataset/repo_info.json'
# try:
# 	fhand = open(fname, 'r')
# except OSError as e:
# 	print('Could not read file', fname)
# else:
# 	try:
# 		lists = json.load(fhand)
# 	except ValueError as e:
# 		print('Fail to load the file', fname)
# 	else:		
# 		stars = list()
# 		forks = list()
# 		watches = list()
# 		commits = list()
# 		contributors = list()
# 		for dicts in lists:
# 			if 'stars' in dicts:
# 			# if ('stars' in dicts and dicts['stars'] > 50 and dicts['stars'] < 100):	
# 				stars.append(dicts['stars'])
# 				forks.append(dicts['forks'])
# 				watches.append(dicts['watchers'])
# 				commits.append(dicts['commits'])
# 				contributors.append(len(dicts['contributors']))
		
# 		"""Pearson coefficient"""
# 		x = load.regression_of_repos([x for x in range(21631)])
# 		y = load.stars_of_repos([x for x in range(21631)])
# 		# x = contributors
# 		# y = stars
# 		# x = [forks[i]*0.67462966 + watches[i]*11.47998692 + commits[i]*0.1217047 + contributors[i]*5.97638657 - 20.55699082 for i in range(len(stars))]
# 		print(scipy.stats.pearsonr(x, y))

# 		""" Simple linear regression """
# 		# ssxm, ssxym, ssyxm, ssym = np.cov(x, y, bias=1).flat
# 		# slope, intercept, r_value, p_value, std_err_slope = scipy.stats.linregress(x, y)	
# 		# std_err = std_err_slope * np.sqrt(len(x) * ssxm)
# 		# hx = [xi * slope + intercept for xi in x]
# 		# print(ssxm, ssym ,ssxym)
# 		# print(slope, intercept, std_err)
# 		# print(r_value) 	

# 		""" Multiple linear regression """
# 		# x = [[forks[i], watches[i], commits[i], contributors[i]] for i in range(len(forks))]
# 		# x = np.array(x)
# 		# # x = np.array(watches)
# 		# # x = x.reshape(len(x), 1)
# 		# y = np.array(stars)
# 		# y = y.reshape(len(y), 1)
# 		# clf = linear_model.LinearRegression()
# 		# clf.fit(x, y)
# 		# print(clf.coef_)
# 		# print(np.sqrt(clf.residues_ / (len(stars)-2)))
# 		# print(clf.intercept_)
# 		# y_est = clf.predict(x)
# 		# print(y_est)

# 		""" Display the plot """
# 		# inx = np.argsort(x)
# 		# xs = np.array(x)[inx]
# 		# hxs = np.array(hx)[inx]
# 		# ys = np.array(y)[inx] 
# 		# x_max = np.amax(xs)
# 		# y_max = np.amax(ys)
# 		# x_min = np.amin(xs)
# 		# y_min = np.amin(ys)
# 		# axes = plt.gca()
# 		# axes.set_xlim([x_min,x_max])
# 		# axes.set_ylim([y_min,y_max])
# 		# plt.scatter(xs, ys, label = 'Data sets (21516)')
# 		# plt.scatter(xs, hxs, color = 'red', label = 'Estimated values')
# 		# plt.plot(xs, slope*xs + intercept, color = 'red', label = 'Regrssion line', linewidth = 2)
# 		# plt.xlabel('# of contributors')
# 		# plt.ylabel('# of stars')
# 		# plt.title(r'Contributor-star distribution:')
# 		# plt.legend(loc = 'lower right')
# 		# plt.show()  

# 	finally:
# 		fhand.close()	

	


