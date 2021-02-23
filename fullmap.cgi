#!/usr/bin/python2
# -*- coding: UTF-8 -*-

# enable debugging
import cgi
import cgitb
import socket
import re
import zlib
import os # get environment settings
cgitb.enable(display = 0, logdir = "./tmp")

print "Content-Type: text/html\n"

def getLink(words, genes):
        return '<a style="color:blue" href="https://textrous.irp.nia.nih.gov/clientph.cgi?genes=' + genes + '&words=' + words + '">' + words + '</a>'

def main():
	form = cgi.FieldStorage()
	try:
                genes = form['genes'].value
                genes = cgi.escape(genes, True)
        except:
                genes = "asdf"

	HOST = os.environ['TEXTROUS_HOST'] # The remote host
	PORT = os.environ['TEXTROUS_PORT'] # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, int(PORT)))
	s.sendall("4" + genes)
	data = s.recv(1048576)
	s.close()
	data = zlib.decompress(str(data)).split()
	num = data[0]

	print '<!DOCTYPE html>'
	print '<link rel="stylesheet" type="text/css" href="https://textrous.irp.nia.nih.gov/th.css"/>'
	data = data[1:]
	data = " ".join(data)
        allWords = re.findall(">([a-z-']+)<", data)
        for word in allWords:
		if word in genes.lower().split(): continue
                data = re.sub(">" + word + "<", ">" + getLink(word, genes) + "<", data)
        print data
	print "</html>"

if __name__ == "__main__":
	main()
