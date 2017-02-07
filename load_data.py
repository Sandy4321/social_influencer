# coding=utf-8
import json

userNum = 3895
repoNum = 21631
top30 = [2147, 2575, 1941, 2766, 1282, 3080, 2018, 3690, 2564,  451, 
	     1010, 1468,  664, 1305, 1457, 3583, 3355, 2008,  829, 2542,
	     2827,  584, 1057, 1546, 3574, 2767, 3401, 1389,  105,  580]

datasets = [{'userNum' : 3895, 'repoNum' : 21631, 'language' : 'Python'}]


def all_users():
	return([x for x in range(userNum)])

def top10_users():
	return(top30[:10])

def top11to20_users():
	return(top30[10:20])

def top20_users():	
	return(top30[:20])      

def top21to30_users():
	return(top30[20:30])
	   
def top30_users():
	return(top30)          

##################################################
######### Get the repositories of users ##########
##################################################
def getRepos(userList, mode = 'o'):
	if not userList:
		print('It\'s an empty user list.')
		raise TypeError

	for index in userList:
		if index >= userNum:
			print('The user index: %d is out of range.' % (index))
			raise IndexError	

	N = len(userList)
	repoList = list()
	fname = 'Python_dataset/user_info.json'	
	try:
		fhand = open(fname, 'r')
		lists = json.load(fhand)
	except:
		print('Could not read file', fname)
		raise OSError
	else:	
		if mode == 'o':
			for index in userList:
				repoList.append(lists[index]['owned_repo'])	
		elif mode == 'w':
			for index in userList:
				repoList.append(lists[index]['written_repo'])	
		else:
			print('Invalid mode.')		
	finally:
		fhand.close()
		return(repoList)		


##################################################
######## Find the collaborators of users #########
##################################################
def collab_of_users(userList):
	if not userList:
		print('It\'s an empty user list.')
		raise TypeError

	for index in userList:
		if index >= userNum:
			print('The user index: %d is out of range.' % (index))
			raise IndexError

	try: 
		repoList = getRepos(userList, 'w')
	except:
		print('Could not find the repolist of users', userList)
	else:			
		N = len(userList)
		collabList = [set() for x in range(N)]
		fname = 'Python_dataset/commitLogs.txt'	
	
		try:
			fhand = open(fname, 'r')
		except:
			print('Could not read file', fname)
			raise OSError
		else:
			for line in fhand:
				x = line.split()
				user = int(x[0])
				repo = int(x[1])
				for i in range(N):
					if (repo in repoList[i] and user != userList[i]):
						collabList[i].add(user)
		finally:			
			fhand.close()
			return(collabList)


##############################################
### Find the related repositories of users ###
##############################################
def related_repo_of_users(userList, repoList, collabList):
	if len(userList) == 0 or len(repoList) == 0 or len(collabList) == 0:
		print("The list is empty.")

	relatedList = [set() for u in range(len(userList))]
	if all(len(relatedList) == len(x) for x in (userList, repoList, collabList)):
		file = open("Python_dataset/commitLogs.txt", "r")
		for line in file.readlines():
			x = line.split()
			user = int(x[0])
			repo = int(x[1])
			for i in range(len(userList)):
				if (user in collabList[i] and repo not in repoList[i]):
					relatedList[i].add(repo)
		file.close()
	else:	
		print("The lists have different length.")
	return(relatedList)


###########################################
### Load the number of commits of users ###
###########################################
def commits_of_users(userList):
	if not userList:
		print('It\'s an empty user list.')
		raise TypeError
	for index in userList:
		if index >= userNum:
			print('The user index: %d is out of range.' % (index))
			raise IndexError		

	N = len(userList)
	commitList = list()
	fname = 'Python_dataset/user_info.json'	
	try:
		fhand = open(fname, 'r')
		lists = json.load(fhand)
	except:
		print('Could not read file', fname)
		raise OSError
	else:
		for index in userList:
			commitList.append(lists[index]['commits'])		
	finally:
		fhand.close()
		return(commitList)	


##################################################
### Load the number of commits of repositories ###
##################################################
def commits_of_repos(repoList):
	if not repoList:
		print('It\'s an empty repo list.')
		raise TypeError

	N = len(repoList)
	commitList = list()
	fname = 'Python_dataset/repo_info.json'	
	try:
		fhand = open(fname, 'r')
		lists = json.load(fhand)
	except:
		print('Could not read file', fname)
		raise OSError
	else:
		for r_index in repoList:
			if r_index >= repoNum:
				print('The repo index: %d is out of range.' % (r_index))
			else:
				commitList.append(lists[r_index]['commits'])		
	finally:
		fhand.close()
		return(commitList)	


##################################################
#### Load the number of contributors of repos ####
##################################################
def contributors_of_repos(repoList):
	if not repoList:
		print('It\'s an empty repo list.')
		raise TypeError

	N = len(repoList)
	contributorList = list()
	fname = 'Python_dataset/repo_info.json'	
	try:
		fhand = open(fname, 'r')
		lists = json.load(fhand)
	except OSError as e:
		print('Could not read file', fname)
		raise OSError
	else:
		for r_index in repoList:
			if r_index >= repoNum:
				print('The repo index: %d is out of range.' % (r_index))
			else:
				contributorList.append(len(lists[r_index]['contributors']))		
	finally:
		fhand.close()
		return(contributorList)	


##################################################
#### Load the number of forks of repositories ####
##################################################
def forks_of_repos(repoList):
	if not repoList:
		print('It\'s an empty repo list.')
	else:
		N = len(repoList)
		forkList = list()

	fname = 'Python_dataset/repo_info.json'	
	try:
		fhand = open(fname, 'r')
	except OSError as e:
		print('Could not read file', fname)	
	else:
		try:
			lists = json.load(fhand)
		except ValueError as e:
			print('Fail to load the file', fname)	
		else:
			for r_index in repoList:
				if r_index >= repoNum:
					print('The repo index is out of range.')
				elif 'forks' not in lists[r_index]:
					estimate_fork = 7.989 * float(len(lists[r_index]['contributors'])) - 5.09
					if estimate_fork < 0.0:
						estimate_fork = 0.0
					forkList.append(estimate_fork)	
				else:
					forkList.append(lists[r_index]['forks'])		
	finally:
		fhand.close()
		return(forkList)		


##################################################
### Load the number of watches of repositories ###
##################################################
def watches_of_repos(repoList):
	if repoList is None:
		print('It\'s an empty repo list.')
		raise TypeError
	else:
		N = len(repoList)
		watchList = list()

	fname = 'Python_dataset/repo_info.json'	
	try:
		fhand = open(fname, 'r')
	except OSError as e:
		print('Could not read file', fname)
		raise OSError	
	else:
		try:
			lists = json.load(fhand)
		except ValueError as e:
			print('Fail to load the file', fname)	
			raise ValueError
		else:
			for r_index in repoList:
				if r_index >= repoNum:
					print('The repo index is out of range.')
					raise ValueError
				elif 'watchers' not in lists[r_index]:
					estimate_watch = 2.347 * float(len(lists[r_index]['contributors'])) - 0.097
					if estimate_watch < 0.0:
						estimate_watch = 0.0
					watchList.append(estimate_watch)	
				else:
					watchList.append(lists[r_index]['watchers'])		
	finally:
		fhand.close()
		return(watchList)


##################################################
#### Load the number of stars of repositories ####
##################################################
def stars_of_repos(repoList):
	if repoList is None:
		print('It\'s an empty repo list.')
		raise TypeError
	else:
		N = len(repoList)
		starList = list()

	fname = 'Python_dataset/repo_info.json'	
	try:
		fhand = open(fname, 'r')
	except OSError as e:
		print('Could not read file', fname)
		raise OSError	
	else:
		try:
			lists = json.load(fhand)
		except ValueError as e:
			print('Fail to load the file', fname)	
			raise ValueError
		else:
			for r_index in repoList:
				if r_index >= repoNum:
					print('The repo index is out of range.')
					raise ValueError
				elif 'stars' not in lists[r_index]:
					estimate_star = 40.244 * float(len(lists[r_index]['contributors'])) - 22.605
					if estimate_star < 0.0:
						estimate_star = 0.0
					starList.append(estimate_star)	
				else:
					starList.append(lists[r_index]['stars'])		
	finally:
		fhand.close()
		return(starList)


##################################################
##### Load the multiple regression of repos ######
##################################################
def regression_of_repos(repoList):
	if repoList is None:
		print('It\'s an empty repo list.')
	else:
		N = len(repoList)
		regressionList = list()

	fname = 'Python_dataset/repo_info.json'	
	try:
		fhand = open(fname, 'r')
	except OSError as e:
		print('Could not read file', fname)	
	else:
		try:
			lists = json.load(fhand)
		except ValueError as e:
			print('Fail to load the file', fname)	
		else:
			for r_index in repoList:
				if r_index >= repoNum:
					print('The repo index is out of range.')
				elif 'forks' not in lists[r_index]:
					estimate_fork = 7.989 * float(len(lists[r_index]['contributors'])) - 5.09
					if estimate_fork < 0.0:
						estimate_fork = 0.0
					estimate_watch = 2.347 * float(len(lists[r_index]['contributors'])) - 0.097
					if estimate_watch < 0.0:
						estimate_watch = 0.0	
					y = estimate_fork * 0.674 + estimate_watch * 11.479 + lists[r_index]['commits'] * 0.121 + float(len(lists[r_index]['contributors'])) *	5.976 - 20.556
					if y < 0.0:
						y = 0.0
					regressionList.append(y)	
				else:
					y = lists[r_index]['forks'] * 0.674 + lists[r_index]['watchers'] * 11.479 + lists[r_index]['commits'] * 0.121 + float(len(lists[r_index]['contributors'])) *	5.976 - 20.556
					if y < 0.0:
						y = 0.0
					regressionList.append(y)		
	finally:
		fhand.close()
		return(regressionList)

