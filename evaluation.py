# coding=utf-8
import numpy as np

def spearman(x, y):
	"""
    Calculates a Spearman rank-order correlation coefficient.

    Parameters
    ----------
    x, y : input lists 
           All the ranks in the lists should be distinct integers.

    Returns
    -------
    rho : float 

    """

	# Check inputs
	if (not x or len(x) == 1 or len(x) != len(y)):
		raise ValueError('Invalid input lists.')


	n = len(x)
	diff = 0.0
	for i in range(n):
		diff += (x[i] - y[i])**2	

	return(1.0 - 6.0 * diff / (n * (n**2 - 1.0)))



def kendall(x, y):
	"""
    Calculates a Kendall rank-order correlation coefficient.

    Parameters
    ----------
    x, y : input lists 
           All the ranks in the lists should be distinct integers.

    Returns
    -------
    tau : float 

    """

	# Check inputs
	if (not x or len(x) == 1 or len(x) != len(y)):
		raise ValueError('Invalid input lists.')

	n = len(x)	 
	concordant = discordant = 0

	sorted_order = np.argsort(x)  
	new_x = np.array(x)[sorted_order] 
	new_y = np.array(y)[sorted_order] 

	for i in range(n - 1):
		count = 0
		for j in range(i + 1, n):
			if new_y[j] > new_y[i]:
				count += 1 
		concordant += count
		discordant += n - (i + 1) - count

	return((concordant - discordant) / (0.5 * n * (n - 1)))	



def rank_of_list(lst):
	
	# Check inputs
	if not lst:
		raise ValueError('Empty input list.')

	rankList = [0 for x in range(len(lst))]
	indices = list(range(len(lst)))

	# sort the position of elements
	indices.sort(key = lambda x: lst[x], reverse = True)   

	n = 1
	for i in indices:
		rankList[i] = n
		n = n + 1
	return(rankList)	



