# encoding = 'utf-8'
import requests


user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)' 
	          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')
header = {'User-Agent' : user_agent}

#Increasing the unauthenticated rate limit for OAuth applications
payload = {'client_id': 'e5f977a68ace627a1760', 'client_secret': 'aa9e159b082180e875a96d68d84e26324771e5b4'}

def get_json(url):

	# check if the request exceeds rate limit 
	r = requests.get('https://api.github.com/rate_limit', headers = header, params = payload)
	if r.headers['X-RateLimit-Remaining'] == 0:
		print('Exceeds rate limit.')
		return (False)	
	
	try:
		response = requests.get(url, headers = header, params = payload)

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
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			print('Bad request:', url, response.headers['Status'])
			return(False)		
		else:	
			return(response.json())

dataset_path = '/Users/DerekChiang/Documents/Github repo/social_influencer/Java_dataset/6273/'
fname = dataset_path + 'top30-award.txt'
# try:
# 	fhand = open(fname, 'r')
# except:
# 	print('Could not open file', fname)
# else:	
# 	top30 = list()
# 	followers = list()
# 	api_url = 'https://api.github.com/users/'
# 	for line in fhand:
# 		user = line.rstrip()
# 		top30.append(user)

# 		user_url = api_url + user 
# 		user_dict = get_json(user_url)
# 		followers.append(user_dict['followers'])
# 	# for n in zip(top30, followers):
# 	# 	print(n)	
# 	indices = list(range(len(top30)))
# 	indices.sort(key = lambda x: followers[x], reverse = True)

# 	with open(dataset_path + 'top30-follower.txt', 'w') as outfile:
# 		for i in indices:
# 			outfile.write(top30[i] + '\n')
# 			print(followers[i])
# 	print('Saved')		




