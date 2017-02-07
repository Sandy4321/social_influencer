# encoding = 'utf-8'

##################################################
### For Python 3.0 or later -- requests module ###
##################################################
import requests


user = 'rg3'
user_url = 'https://api.github.com/users/' + user + '/repos'
user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)' 
	          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')
header = {'User-Agent' : user_agent}

#Increasing the unauthenticated rate limit for OAuth applications
payload = {'client_id': 'e5f977a68ace627a1760', 'client_secret': 'aa9e159b082180e875a96d68d84e26324771e5b4'}

def get_json(url):
	try:
		respnose = requests.get(url, headers = header, params = payload)

	except requests.exceptions.ConnectionError as e:	
		print('We failed to reach a server.', e)
		return(False)

	except requests.exceptions.Timeout:
		print('The request has timed out.')
		return(False)

	except requests.exceptions.TooManyRedirects:
		print('The request exceeds the configured number of maximum redirections.')
		return(False)
	
	except requests.exceptions.RequestException as e:
		print('Other exceptions.', e)
		return(False)

	else:
		try:
			respnose.raise_for_status()
		except requests.exceptions.HTTPError as e:
			print('The server couldn\'t fulfill the request.', e)
			return(False)		
		else:	
			return(respnose.json())


repo_list = get_json(user_url)
if not repo_list:
	print('Please retry.')
else:
	print('User', user, 'has', len(repo_list), 'public repositories.')
	python_repos = list()
	for repo in repo_list:
		if (repo['language'] == 'Python' and repo['fork'] == False):
			python_repos.append(repo['url'])
	print('Written in Python(fork repos are excluded):', len(python_repos))
	for url in python_repos:
		repo = get_json(url)
		if not repo:
			print('Can\'t find the repository.')
		else:	
			print('\nRepository name:', repo['full_name'])
			print('Watch:', repo['subscribers_count'])
			print('Star:', repo['stargazers_count'])	
			print('Fork:', repo['forks_count'])	


