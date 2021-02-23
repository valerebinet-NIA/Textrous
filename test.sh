#!/bin/bash
clear
ps ax | grep python
ls -al /var/run/textrous.pid
cat /var/run/textrous.pid
ls -al /var/run/httpd.pid
cat /var/run/httpd.pid
ls -al /var/lock/subsys/textrous 
ls -al /var/lock/subsys/httpd
exit 0
