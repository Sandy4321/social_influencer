# coding = utf-8
import re
import json


def top30_users(dataset_path, truth = 's'):
	"""
    Return the top 30 users according to the chosen dataset and ground truth

    Parameters
    ----------
    dataset_path : the path of the chosen dataset 

    truth = 's' : set ground truth as the # of stars (default)
            'a' : set ground truth as the rankings on Git award
            'f' : set ground truth as the # of followers         

    Return
    -------
    top30 : a top 30 user list

    """

    # initialization
	top30 = list()
	
	# check the setting of ground truth
	file = str()
	if truth == 's':
		file = 'top30-stars.txt'
	elif truth == 'a':
		file = 'top30-award.txt'
	elif truth == 'f':
		file = 'top30-followers.txt'	
	else:
		print('Invalid ground truth mode', truth)	

	# return the top 30 user list 
	fname = dataset_path + file
	try:
		fhand = open(fname, 'r')
	except:
		print('Could not load top30 users', fname)
	else:	
		for line in fhand:
			name = line.rstrip()
			top30.append(name)
		fhand.close()
		return(top30)          


def get_userInfo(userList, dataset_path, mode = 'o'):
	"""
    Get user information from the user_info.json file

    Parameters
    ----------
    userList : input user list

    dataset_path : the path of the chosen dataset                

    mode = 'o' : owned repositories of users
           'w' : written repositories of users
           'c' : # of commits of users           

    Return
    -------
    returnList : a list

    """

	# initialization
	N = len(userList)
	returnList = list()

	# open file user_info.json
	fname = dataset_path + 'user_info.json'	
	try:
		fhand = open(fname, 'r')
		user_dict = json.load(fhand)
	except:
		raise OSError('Could not read file', fname)
	else:	
		# check if all the users in userList exist
		for user in userList:
			if not user in user_dict:
				raise ValueError('Could not find user', user)
				break
		else:		
			if mode == 'o':
				for user in userList:
					returnList.append(user_dict[user]['owned repos'])	
			elif mode == 'w':
				for user in userList:
					returnList.append(user_dict[user]['written repos'])	
			elif mode == 'c':
				for user in userList:
					returnList.append(user_dict[user]['commits'])			
			else:
				raise ValueError('Invalid mode.', mode)		
	finally:
		fhand.close()
		return(returnList)		



def get_collaborators(userList, dataset_path):
	"""
    Find the collaborators of users

    Parameters
    ----------
    userList : input user list

    dataset_path : the path of the chosen dataset           

    Return
    -------
    collabList : a list

    """

	try: 
		repoList = get_userInfo(userList, dataset_path, mode = 'w')
	except:
		print('Could not find the repolist of users', userList)
	else:			
		N = len(userList)
		collabList = [set() for x in range(N)]	

		
		fname = dataset_path + 'commitLog.txt'
		try:
			fhand = open(fname, 'r')
		except:
			print('Could not read file', fname)
		else:	
			for line in fhand:
				line = line.rstrip()
				x = line.split()

				user_wo_id = re.findall('(^.*)\(', x[0])
				user = user_wo_id[0]
				repo = x[1]
				for i in range(N):
					if (repo in repoList[i] and user != userList[i]):
						collabList[i].add(user)
		finally:			
			fhand.close()
			return(collabList)


def get_relatedRepos(userList, dataset_path):
	"""
    Find the related repositories of users

    Parameters
    ----------
    userList : input user list

    dataset_path : the path of the chosen dataset               

    Return
    -------
    relatedList : a list

    """

	try: 
		repoList = get_userInfo(userList, dataset_path, mode = 'w')
		collabList = get_collaborators(userList, dataset_path)
	except:
		print('Could not find the repolist or collabList of users', userList)		
	else:	
		N = len(userList)
		relatedList = [set() for x in range(N)]

		fname = dataset_path + 'commitLog.txt'
		try:
			fhand = open(fname, 'r')
		except:
			print('Could not read file', fname)
		else:
			for line in fhand:
				line = line.rstrip()
				x = line.split()

				user_wo_id = re.findall('(^.*)\(', x[0])
				user = user_wo_id[0]
				repo = x[1]
				for i in range(N):
					if (user in collabList[i] and repo not in repoList[i]):
						relatedList[i].add(repo)
		finally:			
			fhand.close()
			return(relatedList)



def get_repoInfo(repoList, dataset_path, mode = 'c'):
	"""
    Get repo information from the repo_info.json file

    Parameters
    ----------
    repoList : input repo list

    dataset_path : the path of the chosen dataset  

    mode = 'c' : # of commits of repo
           'cb' : # of contributors of repo
           'f' : # of forks of repo
           'w' : # of watchers of repo
           's' : # of stars of repo   

    Return
    -------
    returnList : a list

    """

	# initialization
	N = len(repoList)
	returnList = list()

	# open file repo_info.json
	fname = dataset_path + 'repo_info.json'	
	try:
		fhand = open(fname, 'r')
		repo_dict = json.load(fhand)
	except:
		print('Could not read file', fname)
	else:
		for repo in repoList:
			if not repo in repo_dict:
				print('Could not find repo', repo)
				break
		else:		
			if mode == 'c':
				for index in repoList:
					returnList.append(lists[index]['commits'])	
			elif mode == 'cb':
				for index in repoList:
					returnList.append(lists[index]['contributors'])	
			elif mode == 'f':
				for index in repoList:
					returnList.append(lists[index]['forks'])			
			elif mode == 'w':
				for index in repoList:	
					returnList.append(lists[index]['watchers'])	
			elif mode == 's':
				for index in repoList:
					returnList.append(lists[index]['stars'])					
			else:
				raise ValueError('Invalid mode.', mode)		
	finally:
		fhand.close()
		return(returnList)

