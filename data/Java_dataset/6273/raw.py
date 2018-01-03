import os
import re
import json

# fname = 'raw/userid.txt'
# try:
# 	fhand = open(fname, 'r')
# except:
# 	print('Could not open file', fname)

# userlist = dict()
# for line in fhand:
# 	line = line.rstrip()
# 	line = re.findall('(^.*?)\(', line)[0]
# 	userlist[line] = ''
# print(len(userlist))
# fhand.close()			
	
# fhand = open('raw/javaTop30.txt', 'r')
# for name in fhand:
# 	name = name.rstrip()
# 	if not name in userlist:
# 		print(name)	
# with open('userList.json', 'w') as outfile:
# 	json.dump(userlist, outfile, indent=4, sort_keys=True, separators= (',', ':'))
# outfile.closed
# print('Saved')
# print(fname, len(userlist))			
# fhand.close()

# outfile = open('repoList.txt', 'w')
# path = 'raw/repos_list'
# dirs = os.listdir(path)
# for user in dirs:
# 	if not user in userlist:
# 		print('Not found user', user) 
# 	else:
# 		find_name = re.findall('(^.*?)\(', user)
# 		user_name = find_name[0]
# 		fhand = open(path + '/' + user, 'r')
# 		for line in fhand:
# 			repo = line.rstrip()
# 			outfile.write(user_name + '/' + repo + '\n')		
# print(len(dirs))
# print('Saved')

# outfile = open('commitLog.txt', 'w')
# fname = 'raw/contributors_commits.txt'
# try:
# 	fhand = open(fname, 'r')
# except:
# 	print('Could not open file', fname)

# user = ''
# repo = ''
# for line in fhand:
# 	line = line.rstrip()
# 	if not line:
# 		user = ''
# 		repo = ''
# 		continue
# 	if ':' in line:
# 		find_user = re.findall('(^.*?):', line)
# 		find_commit = re.findall(':(.*)', line)
# 		if len(find_user) == 1 and len(find_commit) == 1:
# 			user = find_user[0]
# 			commit = int(find_commit[0])
# 		else:
# 			print('Could not find user', line)	
# 	else:
# 		find_repo = re.findall('\)-(.*)', line)
# 		find_id = re.findall('\((.*?)\)', line)
# 		if len(find_repo) == 1 and len(find_id) == 1:
# 			repo = find_repo[0]
# 			uid = find_id[0]
# 		else:
# 			print('Could not find repo', line)	

# 	if user and repo:
# 		fullrepo = repo + '(' +uid + ')'
# 		newline = user + ' ' + fullrepo + ' ' + str(commit)+ '\n'
# 		outfile.write(newline)
# print('Saved')		

# fname = 'userList.json'
# try:
# 	fhand = open(fname, 'r')
# 	users = json.load(fhand)
# except:
# 	print('Could not open', fname)
# fhand.close()
		
# fname = 'user_info.json'
# try:
# 	fhand = open(fname, 'r')
# 	dicts = json.load(fhand)
# except:
# 	print('Could not open', fname)

# i = 0
# for user in dicts:
# 	i += 1 
# 	if not user in users:
# 		print('could not find user', user)
# 	if not dicts[user]['id'] == users[user]:
# 		print('Invalid id', user)	
# print(i)


# import requests
# from random import randint

# headers = [
#         {"User-Agent" : "Mozilla/5.0 (X11; U; UNICOS lcLinux; en-US) Gecko/20140730 (KHTML, like Gecko, Safari/419.3) Arora/0.8.0"},
#         {"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"},
#         {"User-Agent" : "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16"},
#         {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"},
#         {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"},
#         {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"},
#         {"User-Agent" : "Mozilla/6.0 (X11; U; Linux x86_64; en-US; rv:2.9.0.3) Gecko/2009022510 FreeBSD/ Sunrise/4.0.1/like Safari"},
#         {"User-Agent" : "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"}]


# #Increasing the unauthenticated rate limit for OAuth applications
# payloads = [
# 		{'client_id': 'e5f977a68ace627a1760', 'client_secret': 'aa9e159b082180e875a96d68d84e26324771e5b4'},
# 		{'client_id': 'a69a07f17c4d67a45a3c', 'client_secret': 'da2a32f8b42769fdc4671b4a5c53694d67d8cbb6'}]


# def get_json(url):
# 	try:
# 		response = requests.get(url, headers = headers[randint(0,7)], params = payloads[randint(0,1)])

# 	except requests.exceptions.ConnectionError as e:	
# 		print('We failed to reach a server.', e)
# 		return(False)

# 	except requests.exceptions.Timeout:
# 		print('The request has timed out.')
# 		return(False)

# 	except requests.exceptions.TooManyRedirects:
# 		print('The request exceeds the configured number of maximum redirections.')
# 		return(False)
	
# 	except requests.exceptions.RequestException as e:
# 		print('Other exceptions.', e)
# 		return(False)

# 	else:
# 		try:
# 			response.raise_for_status()
# 		except requests.exceptions.HTTPError as e:
# 			print('The server couldn\'t fulfill the request.', url)
# 			return(False)		
# 		else:	
# 			return(response.json())

# outfile = open('new_repos_info.txt', 'w')
# missfile = open('new_miss_repo.txt', 'w')
# missing = 0
# try:
# 	fhand = open('repoList.txt', 'r')
# except:
# 	print('Could not open file')
# index = 1	
# for line in fhand:
# 	if index % 100 == 0:
# 		print(index)

# 	line = line.rstrip()
	
# 	try:
# 		user_url = 'https://api.github.com/repos/' + line
# 		repo_dict = get_json(user_url)
# 		if not repo_dict:
# 			missfile.write(lines)
# 			missing += 1 
# 		else:
# 			string = line +':'+str(repo_dict['stargazers_count'])+','+str(repo_dict['forks_count'])+','+str(repo_dict['subscribers_count'])+'\n'
# 			outfile.write(string)
# 	except:
# 		print('FAIL to load api', user_url)		
# 	index += 1	
# print('Total missing:', missing)



# missing = 0
# repolist = dict()

# fhand = open('repos_info.txt', 'r')
# for line in fhand:
# 	line = re.findall('(^.*?):',line)
# 	repo = line[0]
# 	repolist[repo] = ''
# fhand.close()

# outfile = open('missing_repo.txt', 'w')
# fhand = open('repoList.txt', 'r')
# for line in fhand:
# 	line = line.rstrip()
# 	if not line in repolist:
# 		missing += 1
# 		outfile.write(line+'\n')
# fhand.close()
# print(missing)














