import pickle
import re
import urllib2
import zlib
import socket

gene2id = pickle.load(open("gene2pubmed_filtered.pkl"))

def getArticle(phrase, genes):
	pmids = []
	for gene in genes:
		try:
			pmids += gene2id[gene]
		except:
			pass
	print pmids
	pmids = list(set(pmids))	
	pmids = "%20".join(pmids)
	query = pmids + "[uid]" + phrase + "[text%20word]"
	url = "http://www.ncbi.nlm.nih.gov/pubmed?term=" + query
	page = urllib2.urlopen(url).read()	
	if "No items found" in page:
		return ""
	else:
		return url

def main():
        while True:
                if True:
                        HOST = 'localhost'
                        PORT = 5568
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.bind((HOST, PORT))
                        s.listen(1)
                        print "done"
                        while True:
                                conn, addr = s.accept()
                                data = conn.recv(16384)
                                if not data: break
                                strdata = str(data)
				strdata = strdata.split("=")
				strdata[0] = strdata[0].split() #genes, strdata[1] is the phrase
				conn.sendall(zlib.compress(getArticle(strdata[1], strdata[0])))
                        conn.close()

if __name__ == '__main__':
	main()
