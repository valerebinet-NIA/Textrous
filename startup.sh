#!/bin/sh
# start the textrous server
pidfile=/var/run/textrous.pid
export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/sbin:/usr/sbin
# change to where every the files live
cd /var/www/textrous/gene2word || exit 2
mv /var/log/httpd/textrous.log /var/log/httpd/textrous.log-$(date +%Y%m%d)
#sudo -s apache python queryWord.py > /var/log/httpd/textrous.log  2>&1 &
sudo -u apache python queryWord.py > /var/log/httpd/textrous.log  2>&1 &
#pgrep -U apache python > /var/run/textrous.pid
#pgrep -U apache python > $pidfile
exit 0
