def jp(input, d, n):
	tmp = []
	for s in input:
		try:
			tmp.append([helper(s, d)])
		except:
			pass
	input = tmp
	while True:
		hasChanged = False
		res = []
		for l1 in input:
			flag = False
			for l2 in res:
				if check(l1, l2, n):
					flag = True
					hasChanged = True
					l2 += l1
					break
			if not flag:
				res.append(l1)
		if not hasChanged: 
			ans = []
			for cluster in res:
				tmp = []
				for e in cluster:
					tmp.append(e[0])
				ans.append(tmp)
			return ans
		input = res

def check(l1, l2, n):
	for tup1 in l1:
		for tup2 in l2:
			if tup1[0] in tup2[1] and tup2[0] in tup1[1] and len(tup1[1] & tup2[1]) > n:
				return True
	return False

def helper(s, d):
	return (s, d[s])
