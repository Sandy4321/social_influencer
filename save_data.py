# coding=utf-8
import re
import sys
import json
import numpy as np
import load_data as load
import matplotlib.pyplot as plt


##################################################
############ Save user_info.json file ############
##################################################
def save_userInfo():

    # Initialize a list to save the information of users(list of dictionaries)
    lists = list()

    # Load user name and id
    fname = 'Python_dataset/userList_3895.txt'
    try:
        fhand = open(fname, 'r')
    except OSError as e:
        print('Could not read file', fname)
        sys.exit()
    except:
        print('Unexpected error:', sys.exc_info()[0])
        sys.exit()
    else:
        index = 0
        for line in fhand:
            name = re.findall('(.*)\(', line)
            number = re.findall('\((.*)\)', line)  
            if (len(name) == 1 and len(number) == 1):
                user = dict()
                user['index'] = index
                user['name'] = name[0]
                user['id'] = int(number[0])
                user['commits'] = 0
                user['owned_repo'] = list()
                user['written_repo'] = list()
                lists.append(user)   
            else:
                print('Could not find the user name and id.', line)  
            index += 1              
        fhand.close()


    # Load the owned repos of users
    fname = 'Python_dataset/repoList_21631.txt'
    try:
        fhand = open(fname, 'r')
    except OSError as e:
        print('Could not read file', fname)
        sys.exit()
    except:
        print('Unexpected error:', sys.exc_info()[0])
        sys.exit()
    else:
        repo_index = 0
        for line in fhand:
            owner = re.findall('^(.*?)/', line)
            if len(owner) == 1:
                for user in lists:
                    if owner[0] == user['name']:
                        user['owned_repo'].append(repo_index)
                        break 
            else:
                print('Could not find owner:', line)  
            repo_index += 1              
        fhand.close()


    # Load written repos and number of commits of each user   
    fname = 'Python_dataset/commitLogs.txt'    
    try:
        fhand = open(fname, 'r')
    except OSError as e:
        print('Could not read file', fname)
        sys.exit()
    except:
        print('Unexpected error:', sys.exc_info()[0])
        sys.exit()
    else:    
        for line in fhand:
            line = line.rstrip()
            x = line.split()
            user = int(x[0])
            repo = int(x[1])
            commit = int(x[2][:-2])  
            if lists[user]['index'] == user:
                lists[user]['written_repo'].append(repo)
                lists[user]['commits'] += commit
            else:
                print('Wrong user')    
        fhand.close()

    # Save file 'user_info.json'    
    with open('Python_dataset/user_info.json', 'w') as outfile:
        json.dump(lists, outfile, indent = 4, sort_keys = True, separators = (',', ':'))
    outfile.closed    
    print("The user_info.json file is written and saved.")



##################################################
############ Save repo_info.json file ############
##################################################
def save_repoInfo():

    # Initialize a list to save the information of repositories(list of dictionaries)
    lists = list()

    # Load the name of the repos and their owners
    fname = 'Python_dataset/repoList_21631.txt'
    try:
        fhand = open(fname, 'r')
    except OSError as e:
        print('Could not read file', fname)
        sys.exit()
    except:
        print('Unexpected error:', sys.exc_info()[0]) 
        sys.exit()
    else:
        index = 0
        for line in fhand:
            owner = re.findall('(^.*?)/', line)
            name = re.findall('^.*/(.*)', line)   
            if (len(owner) == 1 and len(name) == 1):
                repo = dict()
                repo['index'] = index
                repo['repo_name'] = name[0]
                repo['owner'] = owner[0]
                repo['commits'] = 0
                repo['contributors'] = list()
                lists.append(repo)
            else:
                print('Could not find the repository name and owner', line) 
            index += 1           
        fhand.close()            

    # Load number of commits and contributors(including owner) of each repo  
    fname = 'Python_dataset/commitLogs.txt'    
    try:
        fhand = open(fname, 'r')
    except OSError as e:
        print('Could not read file', fname)
        sys.exit()
    except:
        print('Unexpected error:', sys.exc_info()[0])
        sys.exit()
    else:    
        for line in fhand:
            line = line.rstrip()
            x = line.split()
            user = int(x[0])
            repo = int(x[1])
            commit = int(x[2][:-2])  
            if lists[repo]['index'] == repo:
                lists[repo]['commits'] += commit
                lists[repo]['contributors'].append(user)
        fhand.close()
    

    # Load stars, forks, watchers of repos
    fname = 'Python_dataset/repos_info_21516.txt'
    try: 
        fhand = open(fname, 'r')
    except OSError as e:
        print('Could not read file', fname)
        sys.exit()
    except:
        print('Unexpected error:', sys.exc_info()[0])
        sys.exit()
    else:    
        for line in fhand:
            line = line.rstrip()
            owner = re.findall('(^.*)/', line)
            repo = re.findall('/(.*?):', line)
            star = re.findall(':(.*?),', line)
            fork = re.findall(',(.*?),', line)
            watch = re.findall('^.*,(.*)', line)
            if all(len(x) == 1 for x in (owner, repo, star, fork, watch)):
                for repos in lists:
                    if (owner[0] == repos['owner'] and repo[0] == repos['repo_name']):
                        repos['stars'] = int(star[0])
                        repos['forks'] = int(fork[0])
                        repos['watchers'] = int(watch[0])
                        break    
            else:
                print('Repo:', repo, 'does not conform to the format.')        
        fhand.close()    

    # Save file 'repo_info.json'    
    with open('Python_dataset/repo_info.json', 'w') as outfile:
        json.dump(lists, outfile, indent = 4, sort_keys = True, separators = (',', ':'))
    outfile.closed
    print("The repo_info.json file is written and saved.")



##################################################
####### Save commit distribution of repos ########
##################################################
def repo_commit_distribution():
    
    # Load the number of commits of all repos
    try:    
        repo_commit = load.commits_of_repos([x for x in range(21631)])
    except:
        print('Failed to load the commits of repositories.', sys.exc_info()[0])
        sys.exit()

    # Initialize a dict to save the commit frequency   
    counts = dict() 

    # Count the distribtion of commit frequency
    for commit in repo_commit:
        counts[commit] = counts.get(commit, 0) + 1

    # Save repo_commit_distribution.txt file     
    f = open('Python_dataset/repo_commit_distribution.txt', 'w')
    f.write('[Number of commits]:[Number of repositories with this number of commits]\n') 
    f.write('For example, 50:2 means:\n')
    f.write('    2 repositories have 50 commits.\n')
    for w in sorted(counts):
        f.write(str(w) + ':' + str(counts[w]) + '\n')            
    f.closed
    print('The repo_commit_distribution.txt file is written and saved')

    # Display the commit distribution plot
    x = list(counts.values())   # Number of repositories
    y = list(counts.keys())     # Number of commits  
    inx = np.argsort(x)
    xs = np.array(x)[inx] 
    ys = np.array(y)[inx] 
    axes = plt.gca()
    axes.set_xlim([0,1000])
    axes.set_ylim([0,1000])
    plt.plot(xs, ys)
    plt.xlabel('Number of repositories')
    plt.ylabel('Number of commits')
    plt.title(r'Repository-Commit distribution:')
    plt.show()    



##################################################
################## Main command ##################
##################################################

# repo_commit_distribution()
# save_userInfo()
# save_repoInfo()

