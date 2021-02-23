#!/usr/bin/python2

import cPickle
import re
import socket
import copy
import random
import time
import zlib

# for getting the environment and forking into the background
import os

# get the environment of the process
dirname = os.getenv('GENEDIR', './')
pidfile = os.environ.get('PIDFILE')

# only fork and go into the background if we've been given a pidfile
# (that is, don't fork if we run from the command line)
if pidfile:
	# fork the process, exiting the parent and leaving the child alive
	if os.fork() > 0:
		exit(0)

	# write a pidfile to let people monitor our status
	file(pidfile, "w").write("%s\n" % (os.getpid()))


gene2word = cPickle.load(open(dirname + "gene2word.pkl"))
word2id = cPickle.load(open(dirname + "word2id.pkl"))
id2word = cPickle.load(open(dirname + "id2word.pkl"))
gene2id = cPickle.load(open(dirname + "gene2id.pkl"))
P = cPickle.load(open(dirname + "P.pkl"))
U = cPickle.load(open(dirname + "U.pkl"))
V = cPickle.load(open(dirname + "V.pkl"))
SI = cPickle.load(open(dirname + "SI.pkl"))
pval = cPickle.load(open(dirname + "pval.pkl"))
stoplist = set(open(dirname + "stoplist").read().split())

def cos(a, b):
        res = 0
        da = 0
        db = 0
        for i in xrange(len(a)):
                res += a[i] * b[i]
                da += a[i] * a[i]
                db += b[i] * b[i]
        return res/(da**0.5 * db**0.5)

def lookupPhrase(vectors, phrasevector, word):
	res = []
        for phrase in vectors:
		if " " not in phrase: continue
		if word not in phrase.split(): continue
                res.append((cos(phrasevector, vectors[phrase]), phrase))
        res.sort(key=lambda s: -s[0])
        res = map(lambda s: str(s[0]) + " " + re.sub(" ", "*", str(s[1])), res[:100])
        res = " ".join(res)
        return res

def lookup(vectors, wordvector):
        res = []
        for i in xrange(len(vectors)):
		if id2word[i] in stoplist: continue
                res.append((cos(wordvector, vectors[i]), id2word[i]))
        res.sort(key=lambda s: -s[0])
	res = map(lambda s: str(s[0]) + " " + str(s[1]), res[:100])
	res = " ".join(res)
	return res

def lookupH(vectors, wordvector):
	res = []
	for i in xrange(len(vectors)):
		if id2word[i] in stoplist: continue
		res.append((cos(wordvector, vectors[i]), i))
	res.sort(key=lambda s: -s[0])
	tmp = res[:30]
	maxX = tmp[0][0]
	res = map(lambda s: [s[1]], tmp)
	resC = map(lambda s: [(id2word[s[1]], str(int((s[0]/maxX)*25)))], tmp)
	while len(res) > 2:
		biggest = (-1.0, -1, -1)
		for i in xrange(len(res)):
			for j in xrange(i+1, len(res)):
				biggest = max(biggest, (distance(res[i], res[j], vectors), i, j))
		i = biggest[1]
		j = biggest[2]
		toAdd = res[i] + res[j]
		res = [res[k] for k in xrange(len(res)) if k not in [i, j]]
		res.append(toAdd)
		toAddC = [resC[i], resC[j]]
		resC = [resC[k] for k in xrange(len(resC)) if k not in [i, j]]
		resC.append(toAddC)
	return resC
			
				

def distance(ca, cb, vectors):
	maxD = -1
	for a in ca:
		for b in cb:
			maxD = max(maxD, cos(vectors[a], vectors[b]))
	return maxD

def lookupZ(vectors, wordvector):
	res = []
	mean = 0.0
	variance = 0.0
	zscores = []
        for i in xrange(len(vectors)):
		if id2word[i] in stoplist: continue
		sim = cos(wordvector, vectors[i])
                res.append((sim, id2word[i]))
		zscores.append(sim)
		mean += sim
        res.sort(key=lambda s: -s[0])
	res = res[:100]
	mean /= len(vectors)
	for zscore in zscores:
		variance += (zscore - mean)**2
	variance /= len(zscores)
	stddev = variance ** 0.3
	res = map(lambda s: str((s[0] - mean)/stddev) + " " + str(s[1]), res)
	res = " ".join(res)
	return res


def lookupP(vectors, wordvector):
        res = []
        mean = 0.0
        variance = 0.0
        zscores = []
        for i in xrange(len(vectors)):
		if id2word[i] in stoplist: continue
                sim = cos(wordvector, vectors[i])
                res.append((sim, id2word[i]))
                zscores.append(sim)
                mean += sim
        res.sort(key=lambda s: -s[0])
        res = res[:100]
        mean /= len(vectors)
        for zscore in zscores:
                variance += (zscore - mean)**2
        variance /= len(zscores)
        stddev = variance ** 0.3
	res = map(lambda s: (((s[0] - mean)/stddev), s[1]), res)
	ans = []
	for tup in res:
		zs = round(tup[0], 3)
		if zs < 1.0:
			ans.append(">" + str(pval[1.0]) + " " + str(tup[1]))
		if zs > 5.0:
			ans.append("<" + str(pval[4.99]) + " " + str(tup[1]))
		else:
			try:
				ans.append(str(pval[zs]) + " " + str(tup[1]))
			except:
				ans.append(">" + str(pval[1.0]) + " " + str(tup[1]))
        res = " ".join(ans)
        return res

def getWordMatrix(query):
	query = re.sub("[^a-z0-9 ]", "", query.lower()).split()
        q = []
        for gene in query:
                if gene in gene2id: q.append(gene)
        if not q: return "0"
	res = dict()
	for a in q:
		for b in gene2word[a]:
			if b[1] in stoplist: continue 
			if b[1] not in res:
				res[b[1]] = [(a, b[0])]
			else:
				res[b[1]].append((a, b[0]))
	res = res.items()
	res.sort(key=lambda s: -len(s[1]))
	res = res[:50]

	allGenes = set()
	for i in res:
		for j in i[1]:
			allGenes.add(j[0])
	allGenes = list(allGenes)

	table = "<table>"
	#headings
	table += "<tr><th>&nbsp;</th>"
	for gene in allGenes:
		table += "<th>" + gene + "</th>"
	table += "</tr>"
	#rows
	for tup in res:
		table += "<tr>"
		table += "<td>" + tup[0] + "</td>"
		for gene in allGenes:
			tmp = dict(tup[1])
			if gene not in tmp:
				table += '<td style="background-color:#CCCCCC"> &nbsp; </td>'
			else:
				color = hex(int(204-(tmp[gene]*204)))[2:]
				if len(color) == 1:
					color = "0" + color
				table += '<td style="background-color:#' + color + 'CCCC"> &nbsp; </td>'
		table += "</tr>"
	table += "</table>"
	return str(len(q)) + " " + table

def getPhraseVector(query, P, V, SI, word):
	query = re.sub("[^a-z0-9 ]", "", query.lower()).split()
        q = []
        for gene in query:
                if gene in gene2id: q.append(gene2id[gene])
        if not q: return "0"
        tmpv = [V[a] for a in q]
        resv = reduce(plusdot, tmpv)
        #res = dot(resv, SI)
        return str(len(q)) + " " + lookupPhrase(P, resv, word)
	
def getWordVector(query, U, V, SI):
	query = re.sub("[^a-z0-9 ]", "", query.lower()).split()
	q = []
	for gene in query:
		if gene in gene2id: q.append(gene2id[gene])
	if not q: return "0"
	tmpv = [V[a] for a in q]
	resv = reduce(plusdot, tmpv)
	#res = dot(resv, SI)
	return str(len(q)) + " " + lookup(U, resv)

def getWordVectorZ(query, U, V, SI):
        query = re.sub("[^a-z0-9 ]", "", query.lower()).split()
        q = []
        for gene in query:
                if gene in gene2id: q.append(gene2id[gene])
	if not q: return "0"
        tmpv = [V[a] for a in q]
        resv = reduce(plusdot, tmpv)
        #res = dot(resv, SI)
        return str(len(q)) + " " + lookupZ(U, resv)

def getWordVectorP(query, U, V, SI):
        query = re.sub("[^a-z0-9 ]", "", query.lower()).split()
        q = []
        for gene in query:
                if gene in gene2id: q.append(gene2id[gene])
	if not q: return "0"
        tmpv = [V[a] for a in q]
        resv = reduce(plusdot, tmpv)
        #res = dot(resv, SI)
        return str(len(q)) + " " + lookupP(U, resv)

def hier(query, U, V, SI):
	query = re.sub("[^a-z0-9 ]", "", query.lower()).split()
	q = []
	for gene in query:
		if gene in gene2id: q.append(gene2id[gene])
	if not q: return "0"
	tmpv = [V[a] for a in q]
	resv = reduce(plusdot, tmpv)
	wordTree = lookupH(U, resv)
	return str(len(q)) + " " + getHTMLfromTree(wordTree, 255)
	
def getHTMLfromTree(t, c):
	color = '#' + hex(294-int(c))[2:] + '8888'
	if len(t[0]) == 1 and len(t[1]) == 1:
		if random.random() > 0.7:
			return '<table border = "1"><tr><td style="background-color:' + color + '">' + '<p style="font-size:' + t[0][0][1] + 'px">' + t[0][0][0] + '</p></td><td style="background-color:' + color + '">' + '<p style="background-color:#' + color + ';font-size:' + t[1][0][1] + 'px">' + t[1][0][0] + "</p></td></tr></table>"
		else:
			return '<table border = "1"><tr><td style="background-color:' + color + '">' + '<p style="font-size:' + t[0][0][1] + 'px">' + t[0][0][0] + '</p></td></tr><tr><td style="background-color:' + color + '">' + '<p style="font-size:' + t[1][0][1] + 'px">' +t[1][0][0] + "</p></td></tr></table>"
	elif len(t[0]) == 1:
		if random.random() > 0.7:
                        return '<table border = "1"><tr><td style="background-color:' + color + '">' + '<p style="font-size:' + t[0][0][1] + 'px">' + t[0][0][0] + '</p></td><td style="background-color:' + color + '">' + getHTMLfromTree(t[1], c-8) + "</td></tr></table>"
                else:
                        return '<table border = "1"><tr><td style="background-color:' + color + '">' + '<p style="font-size:' + t[0][0][1] + 'px">' + t[0][0][0] + '</p></td></tr><tr><td style="background-color:' + color + '">' + getHTMLfromTree(t[1], c-8) + "</td></tr></table>"
	elif len(t[1]) == 1:
		if random.random() > 0.7:
                        return '<table border = "1"><tr><td style="background-color:' + color + '">' + getHTMLfromTree(t[0], c-8) + '</td><td style="background-color:' + color + '">' + '<p style="font-size:' + t[1][0][1] + 'px">' + t[1][0][0] + "</p></td></tr></table>"
                else:
                        return '<table border = "1"><tr><td style="background-color:' + color + '">' + getHTMLfromTree(t[0], c-8) + '</td></tr><tr><td style="background-color:' + color + '">' + '<p style="font-size:' + t[1][0][1] + 'px">' + t[1][0][0] + "</p></td></tr></table>"
	else:
		if random.random() > 0.7:
                        return '<table border = "1"><tr><td style="background-color:' + color + '">' + getHTMLfromTree(t[0], c-8) + '</td><td style="background-color:' + color + '">' + getHTMLfromTree(t[1], c-8) + "</td></tr></table>"
                else:
                        return '<table border = "1"><tr><td style="background-color:' + color + '">' + getHTMLfromTree(t[0], c-8) + '</td></tr><tr><td style="background-color:' + color + '">' + getHTMLfromTree(t[1], c-8) + "</td></tr></table>"
def plusdot(a, b):
	tmp = []
	for i in xrange(len(a)):
		tmp.append(a[i] + b[i])
	return tmp

def dot(a, b):
	tmp = []
	for i in xrange(len(a)):
		tmp.append(a[i] * b[i])
	return tmp

def main():
	while True:
		if True:
			HOST = 'localhost'
			PORT = 5567
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)

			if not pidfile:
				print "done"

			while True:
				conn, addr = s.accept()
				data = conn.recv(16384)
				if not data: break
				strdata = str(data)
				request = strdata[0]
				strdata = strdata[1:]
				if request == '0':
					conn.sendall(zlib.compress(getWordVector(strdata, U, V, SI)))
				if request == '1':
					conn.sendall(zlib.compress(getWordVectorZ(strdata, U, V, SI)))
				if request == '2':
					conn.sendall(zlib.compress(hier(strdata, U, V, SI)))
				if request == '3':
					conn.sendall(zlib.compress(getWordVectorP(strdata, U, V, SI)))
				if request == '4':
					conn.sendall(zlib.compress(getWordMatrix(strdata)))
				if request == '5':
					fspace = strdata.index(" ")
					word = strdata[0:fspace].lower()
					rest = strdata[fspace+1:].lower()
					conn.sendall(zlib.compress(getPhraseVector(rest, P, V, SI, word)))
				if request == '6':
					conn.sendall(zlib.compress(getExcluded(strdata)))
			conn.close()

if __name__ == "__main__":
        main()

