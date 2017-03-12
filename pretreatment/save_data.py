#coding = utf-8
import re
import sys
import json

proj_path = '/Users/DerekChiang/Documents/Github repo/social_influencer/'
datasets = ['Python_dataset/21631/', 'Python_dataset/55326/', 'Java_dataset/6273/']
dataset_path = proj_path + datasets[2]


def save_userInfo(dataset_path):
    """
    Save user information in user_info.json file

    """

    # initialize a dict to save the information of users
    dicts = dict()

    # Load user name and id
    fname = dataset_path + 'userList.json'
    try: 
        fhand = open(fname, 'r')
        id_dict = json.load(fhand) 
    except:
        print('Could not read file', fname)
    else:
        for user, _id in id_dict.items():
            dicts[user] = dict()
            dicts[user]['id'] = _id 
            dicts[user]['written repos'] = dict()   
            dicts[user]['owned repos'] = list() 
            dicts[user]['commits'] = 0
        fhand.close()


    # load user owned repositories
    fname = dataset_path + 'repoList.txt'
    try:
        fhand = open(fname, 'r')
    except:
        print('Could not read file', fname)
    else:   
        for line in fhand:
            line = line.rstrip()
            ownerlist = re.findall('(^.*)/', line)
            repolist = re.findall('/(.*)', line)
            if len(ownerlist) == 1 and len(repolist) == 1:
                owner = ownerlist[0]
                repo = repolist[0]

                if not owner in id_dict:
                    print('Could not find user', owner)
                else:    
                    repo_name = repo + '(' + str(id_dict[owner]) + ')'
                    if owner in dicts:
                       dicts[owner]['owned repos'].append(repo_name)
                    else:
                        print('Could not find owner', owner) 
            else:
                print('Invalid format in repoList.txt', line)   

        fhand.close()


    # load user written repositories
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
            user_id = re.findall('\((.*?)\)', x[0])
            
            user = user_wo_id[0]
            id_num = int(user_id[0])
            repo = x[1]
            commit = int(x[2])

            if user in dicts and dicts[user]['id'] == id_num:
                dicts[user]['written repos'][repo] = commit
                dicts[user]['commits'] += commit
            else:
                print('Wrong user', user)    
        fhand.close()

    fhand.close()    


    # Save file 'user_info.json'  
    with open(dataset_path + 'user_info.json', 'w') as outfile:
        json.dump(dicts, outfile, indent = 4, sort_keys = True, separators = (',', ':'))
    outfile.closed    
    print("The user_info.json file is written and saved.")



def save_repoInfo(dataset_path):
    """
    Save repo information in repo_info.json file

    """

    # initialize a dict to save the information of repos
    dicts = dict()


    # Load user name and id
    fname = dataset_path + 'userList.json'
    try: 
        fhand = open(fname, 'r')
        id_dict = json.load(fhand) 
    except:
        print('Could not read file', fname)
    else:
        fhand.close()


    # load repositories
    fname = dataset_path + 'repoList.txt'
    try:
        fhand = open(fname, 'r')
    except:
        print('Could not read file', fname)
    else:   
        for line in fhand:
            line = line.rstrip()
            ownerlist = re.findall('(^.*)/', line)
            repolist = re.findall('/(.*)', line)

            if len(ownerlist) == 1 and len(repolist) == 1:
                owner = ownerlist[0]
                repo = repolist[0]

                if not owner in id_dict:
                    print('Could not find user', owner)
                else:    
                    repo_info = dict()
                    repo_info['repo_name'] = repo
                    repo_info['owner'] = owner
                    repo_info['contributors'] = list()
                    repo_info['commits'] = 0
                    repo_info['id'] = id_dict[owner]
                    repo_name = repo + '(' + str(id_dict[owner]) + ')'
                    dicts[repo_name] = repo_info    
            else:
                print('Invalid format in repoList.txt', line)   

        fhand.close()


    # load repo info
    fname = dataset_path + 'repos_info.txt'
    try:
        fhand = open(fname, 'r')
    except:
        print('Could not read file', fname)
    else:   
        for line in fhand:
            owner = re.findall('(^.*)/', line)
            repo = re.findall('/(.*?):', line)
            star = re.findall(':(.*?),', line)
            fork = re.findall(',(.*?),', line)
            watch = re.findall('^.*,(.*)', line)
            if all(len(x) == 1 for x in (owner, repo, star, fork, watch)): 
                if not owner[0] in id_dict:
                    print('Could not find user', owner[0])
                else:
                    id_string = str(id_dict[owner[0]])
                    repo_name = repo[0] + '(' + id_string + ')'
                    if repo_name in dicts:
                        dicts[repo_name]['stars'] = int(star[0])
                        dicts[repo_name]['forks'] = int(fork[0])
                        dicts[repo_name]['watchers'] = int(watch[0])
                    else:
                        print('Could not find repo', repo_name)    
            else:
                print('Invalid format in repos_info.txt', line)   

        fhand.close()


    # load contributors and commits of repos
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
            user_id = re.findall('\((.*?)\)', x[0])
            
            user = user_wo_id[0]
            id_num = int(user_id[0])
            repo = x[1]
            commit = int(x[2])

            if repo in dicts:
                dicts[repo]['contributors'].append(user)    
                dicts[repo]['commits'] += commit
            else:
                print('Wrong repo', repo)    
        fhand.close() 

    # Save file 'repo_info.json'    SkinSprite
    with open(dataset_path + 'repo_info.json', 'w') as outfile:
        json.dump(dicts, outfile, indent = 4, sort_keys = True, separators = (',', ':'))
    outfile.closed
    print("The repo_info.json file is written and saved.")


##################################################
################## Main command ##################
##################################################

# save_userInfo(dataset_path)
# save_repoInfo(dataset_path)

