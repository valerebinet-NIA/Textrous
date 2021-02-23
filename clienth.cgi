#!/usr/bin/env python2
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

	print '<html>'
	print '<head>'
	print '<link rel="stylesheet" type="text/css" href="https://textrous.irp.nia.nih.gov/t.css"/>'
	print '</head>'
	print '<body>'

	print '<div style="width:1000px;height:100px;position:absolute;left:0;top:0;overflow:hidden;background-color:#617f10">'
        print '<img style="position:absolute;top:5px;left:45px" src="logo2.bmp" height=90px>'
	print '<ul id="main-nav">'
        print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/query.php">Home</a></li>'
        print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/features.php">Features</a></li>'
        print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/tutorial.php">Tutorial</a></li>'
        print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/about.php">About</a></li>'
        print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/contact.php">Contact</a></li>'
        print '</ul>'
        print '</div>'

	if num == "1":
                print '<div style="width:1000px;height:50px;position:absolute;left:0;top:100px;overflow:hidden;background-color:#7A991A"><h1 style="color:#FFFFFF;margin:0;padding:5px;font-family:Verdana,Geneva,sans-serif;position:relative;left:50px">SEARCH</h1><p style="color:#FFFFFF;margin:0;position:absolute;right:10px;top:15px"><a style="text-decoration:none;color:#FFFFFF" href="https://textrous.irp.nia.nih.gov/cliente.cgi?genes=' + genes + '">(' + num + ' gene found.)</a></p><p><form style="position:absolute;left:500px;top:25%" name = "input" action = "client.cgi" method="GET"><input type="text" id="text" name="genes"><input type="submit" id="submit" value="Submit"></form></p></div>'
        else:
                print '<div style="width:1000px;height:50px;position:absolute;left:0;top:100px;overflow:hidden;background-color:#7A991A"><h1 style="color:#FFFFFF;margin:0;padding:5px;font-family:Verdana,Geneva,sans-serif;position:relative;left:50px">SEARCH</h1><p style="color:#FFFFFF;margin:0;position:absolute;right:10px;top:15px"><a style="text-decoration:none;color:#FFFFFF" href="https://textrous.irp.nia.nih.gov/cliente.cgi?genes=' + genes + '">(' + num + ' genes found.)</a></p><p><form style="position:absolute;left:500px;top:25%" name = "input" action = "client.cgi" method="GET"><input type="text" id="text" name="genes"><input type="submit" id="submit" value="Submit"></form></p></div>'
	
	if num == "0":
		print "</html>"
		return
	
	print '<div style="width:1000px;height:30px;position:absolute;left:0px;top:150px;overflow:hidden;">'	
	print '<ul id="sec-nav">'
	print '<li id="sec-navli"><a id="sec-navli" href="client.cgi?genes=' + genes + '">' + 'Table (Cosine)</a></li>'
	print '<li id="sec-navli"><a id="sec-navli" href="clientz.cgi?genes=' + genes + '">' + 'Table (Z-Scores)</a></li>'
	print '<li id="sec-navli"><a id="sec-navli" href="clientp.cgi?genes=' + genes + '">' + 'Table (p-Values)</a></li>'
	print '<li id="sec-navli"><a id="sec-navli" href="clientw.cgi?genes=' + genes + '">' + 'Hierarchical Cloud</a></li>'
	print '<li id="sec-navli"><a id="sec-navli" href="#"><b>Heat Map</b></a></li>'
	print '</ul>'
	print '</div>'

	print '<div style="width:1000px;position:absolute;left:0px;top:180px;bottom:10px;overflow:auto;background-color:#EEEEEE">'	
	data = data[1:]
	data = " ".join(data)
        allWords = re.findall(">([a-z-']+)<", data)
        for word in allWords:
		if word in genes.lower().split(): continue
                data = re.sub(">" + word + "<", ">" + getLink(word, genes) + "<", data)
	data = re.sub("<th>&nbsp;</th>", '<th><a style="text-decoration:none;color:blue" href="fullmap.cgi?genes=' + genes + '">(fullscreen)</a></th>', data)
        print data
	print "</div>"
	print "</html>"

if __name__ == "__main__":
	main()
