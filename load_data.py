# coding=utf-8
import json

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



def get_user_info(userList, dataset = datasets[0], mode = 'o'):
	"""
    Get user information from the user_info.json file

    Parameters
    ----------
    userList : input user list(user index)
               The user index should not exceed the total number of users.

    dataset : choose the current dataset           

    mode = 'o' : owned repositories of users
           'w' : written repositories of users
           'c' : # of commits of users           

    Returns
    -------
    returnList : a list

    """
	
	# check inputs
	if not userList:
		raise ValueError('It\'s an empty user list.')

	for index in userList:
		if index >= dataset['userNum']:
			raise IndexError('The user index: %d is out of range.' % (index))	

	# initialization
	N = len(userList)
	returnList = list()

	# open file user_info.json
	fname = 'Python_dataset/user_info.json'	
	try:
		fhand = open(fname, 'r')
		lists = json.load(fhand)
	except:
		raise OSError('Could not read file', fname)
	else:	
		if mode == 'o':
			for index in userList:
				returnList.append(lists[index]['owned_repo'])	
		elif mode == 'w':
			for index in userList:
				returnList.append(lists[index]['written_repo'])	
		elif mode == 'c':
			for index in userList:
				returnList.append(lists[index]['commits'])			
		else:
			raise ValueError('Invalid mode.')		
	finally:
		fhand.close()
		return(returnList)		



def get_collaborators(userList, dataset = datasets[0]):
	"""
    Find the collaborators of users

    Parameters
    ----------
    userList : input user list(user index)
               The user index should not exceed the total number of users.

    dataset : choose the current dataset           


    Returns
    -------
    returnList : a list

    """

	# check inputs
	if not userList:
		raise ValueError('It\'s an empty user list.')

	for index in userList:
		if index >= dataset['userNum']:
			raise IndexError('The user index: %d is out of range.' % (index))


	try: 
		repoList = get_user_info(userList, mode = 'w')
	except:
		print('Could not find the repolist of users', userList)
	else:			
		N = len(userList)
		collabList = [set() for x in range(N)]
		fname = 'Python_dataset/commitLogs.txt'	
	
		try:
			fhand = open(fname, 'r')
		except:
			raise OSError('Could not read file', fname)
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



def get_related_repos(userList, dataset = datasets[0]):
	"""
    Find the related repositories of users

    Parameters
    ----------
    userList : input user list(user index)
               The user index should not exceed the total number of users.

    dataset : choose the current dataset           


    Returns
    -------
    returnList : a list

    """

	# check inputs
	if not userList:
		raise ValueError('It\'s an empty user list.')

	for index in userList:
		if index >= dataset['userNum']:
			raise IndexError('The user index: %d is out of range.' % (index))

	try: 
		repoList = get_user_info(userList, mode = 'w')
		collabList = get_collaborators(userList)
	except:
		print('Could not find the repolist or collabList of users', userList)		
	else:	
		N = len(userList)
		relatedList = [set() for x in range(N)]
		fname = 'Python_dataset/commitLogs.txt'

		try:
			fhand = open(fname, 'r')
		except:
			raise OSError('Could not read file', fname)
		else:
			for line in fhand:
				x = line.split()
				user = int(x[0])
				repo = int(x[1])
				for i in range(N):
					if (user in collabList[i] and repo not in repoList[i]):
						relatedList[i].add(repo)
		finally:			
			fhand.close()
			return(relatedList)



def get_repo_info(repoList, dataset = datasets[0], mode = 'c'):
	"""
    Get repo information from the repo_info.json file

    Parameters
    ----------
    repoList : input repo list(repo index)
               The repo index should not exceed the total number of repos.

    dataset : choose the current dataset           

    mode = 'c' : # of commits of repo
           'cb' : # of contributors of repo
           'f' : # of forks of repo
           'w' : # of watchers of repo
           's' : # of stars of repo   

    Returns
    -------
    returnList : a list

    """
	
	# check inputs
	if not repoList:
		raise ValueError('It\'s an empty repo list.')

	for index in repoList:
		if index >= dataset['repoNum']:
			raise IndexError('The repo index: %d is out of range.' % (index))	

	# initialization
	N = len(repoList)
	returnList = list()

	# open file repo_info.json
	fname = 'Python_dataset/repo_info.json'	
	try:
		fhand = open(fname, 'r')
		lists = json.load(fhand)
	except:
		raise OSError('Could not read file', fname)
	else:	
		if mode == 'c':
			for index in repoList:
				returnList.append(lists[index]['commits'])	
		elif mode == 'cb':
			for index in repoList:
				returnList.append(lists[index]['contributors'])	
		elif mode == 'f':
			for index in repoList:
				if 'forks' not in lists[index]:
					estimate_fork = 7.989 * len(lists[index]['contributors']) - 5.09
					if estimate_fork < 0.0:
						estimate_fork = 0.0
					returnList.append(estimate_fork)
				else:
					returnList.append(lists[index]['forks'])			
		elif mode == 'w':
			for index in repoList:
				if 'watchers' not in lists[index]:
					estimate_watch = 2.347 * len(lists[index]['contributors']) - 0.097
					if estimate_watch < 0.0:
						estimate_watch = 0.0
					returnList.append(estimate_watch)
				else:
					returnList.append(lists[index]['watchers'])	
		elif mode == 's':
			for index in repoList:
				if 'stars' not in lists[index]:
					estimate_star = 40.244 * len(lists[index]['contributors']) - 22.605
					if estimate_star < 0.0:
						estimate_star = 0.0
					returnList.append(estimate_star)	
				else:
					returnList.append(lists[index]['stars'])					
		else:
			raise ValueError('Invalid mode.')		
	finally:
		fhand.close()
		return(returnList)


# ##################################################
# ##### Load the multiple regression of repos ######
# ##################################################
# def regression_of_repos(repoList):
# 	if repoList is None:
# 		print('It\'s an empty repo list.')
# 	else:
# 		N = len(repoList)
# 		regressionList = list()

# 	fname = 'Python_dataset/repo_info.json'	
# 	try:
# 		fhand = open(fname, 'r')
# 	except OSError as e:
# 		print('Could not read file', fname)	
# 	else:
# 		try:
# 			lists = json.load(fhand)
# 		except ValueError as e:
# 			print('Fail to load the file', fname)	
# 		else:
# 			for r_index in repoList:
# 				if r_index >= repoNum:
# 					print('The repo index is out of range.')
# 				elif 'forks' not in lists[r_index]:
# 					estimate_fork = 7.989 * float(len(lists[r_index]['contributors'])) - 5.09
# 					if estimate_fork < 0.0:
# 						estimate_fork = 0.0
# 					estimate_watch = 2.347 * float(len(lists[r_index]['contributors'])) - 0.097
# 					if estimate_watch < 0.0:
# 						estimate_watch = 0.0	
# 					y = estimate_fork * 0.674 + estimate_watch * 11.479 + lists[r_index]['commits'] * 0.121 + float(len(lists[r_index]['contributors'])) *	5.976 - 20.556
# 					if y < 0.0:
# 						y = 0.0
# 					regressionList.append(y)	
# 				else:
# 					y = lists[r_index]['forks'] * 0.674 + lists[r_index]['watchers'] * 11.479 + lists[r_index]['commits'] * 0.121 + float(len(lists[r_index]['contributors'])) *	5.976 - 20.556
# 					if y < 0.0:
# 						y = 0.0
# 					regressionList.append(y)		
# 	finally:
# 		fhand.close()
# 		return(regressionList)

