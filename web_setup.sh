#!/bin/bash
# Setup a Ubuntu 12.04 server install for Django
# Needs to be run as root (or with sudo)

# The ubuntu user password
PASSWORD='tiger'

uid=`id -u`
if [ $uid -ne 0 ]
then
  echo 'Must be run as root'
  exit
fi

# Determine if this script is being run on an EC2 image or a local VM
host='apoxz.org'
if [[ ! `hostname` =~ "^domU-" ]]
then
  host=`ifconfig eth0 | awk '$1 == "inet" {split($2,a,":"); print a[2]}'`
fi

apt-get install -y git nginx monit mysql-server python-mysqldb

# Install Django
wget -O Django-1.4.tar.gz "http://www.djangoproject.com/download/1.4/tarball/"
tar xzvf Django-1.4.tar.gz
cd Django-1.4
sudo python setup.py install

# Set up nginx
echo "# the IP(s) on which node server is running
upstream app_apoxz {
    server 127.0.0.1:8000;
}

# the nginx server instance
server {
    listen 0.0.0.0:80;
    server_name $host;
    access_log /var/log/nginx/apoxz.log;

    if (\$host != '$host' ) {
        rewrite  ^/(.*)$  http://$host/\$1  permanent;
    }

    # pass the request to the Django server with the correct headers and much more can be added, see nginx config options
    location / {
      proxy_set_header X-Real-IP \$remote_addr;
      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
      proxy_set_header Host \$http_host;
      proxy_set_header X-NginX-Proxy true;

      proxy_pass http://app_apoxz/;
      proxy_redirect off;
    }

    location /static/ {
      autoindex on;
      alias /var/www/apoxz.org/static/;
    }
}" > /etc/nginx/sites-available/apoxz

ln -s /etc/nginx/sites-available/apoxz /etc/nginx/sites-enabled/apoxz

sed -i -e s/#.server_names_hash_bucket_size/server_names_hash_bucket_size/ /etc/nginx/nginx.conf 

nginx -t

# Set up upstart config
echo '#!upstart
description "APOXZ Django server"
author      "Dave Kelly"

start on runlevel [2345]
stop on runlevel [016]

script
    export HOME="/root"
    export PYTHONPATH=$PYTHONPATH:/var/www/apoxz.org/apoxz/
    echo $$ > /var/run/apoxz.pid
    exec sudo -u ubuntu python /var/www/apoxz.org/apoxz/manage.py runserver >> /var/log/apoxz.sys.log 2>&1
end script

pre-start script
    # Date format same as (new Date()).toISOString() for consistency
    echo "[`date -u +%Y-%m-%dT%T.%3NZ`] (sys) Starting" >> /var/log/apoxz.sys.log
end script

pre-stop script
    rm /var/run/apoxz.pid
    echo "[`date -u +%Y-%m-%dT%T.%3NZ`] (sys) Stopping" >> /var/log/apoxz.sys.log
end script' > /etc/init/apoxz.conf

# Setup git repository
mkdir -p /opt/apoxz.git
chown -R root:ubuntu /opt/apoxz.git/
chmod -R 775 /opt/apoxz.git/
git init --bare /opt/apoxz.git

mkdir -p /var/www/apoxz.org

chown -R root:ubuntu /var/www/apoxz.org
chmod -R 775 /var/www/apoxz.org

echo "#!/bin/sh
GIT_WORK_TREE=/var/www/apoxz.org git checkout -f
echo $PASSWORD | sudo -S service apoxz restart
echo $PASSWORD | sudo -S service nginx restart" > /opt/apoxz.git/hooks/post-receive

chmod +x /opt/apoxz.git/hooks/post-receive

# Set up monit conf
echo '#!monit
set logfile /var/log/monit.log

check process apoxz with pidfile "/var/run/apoxz.pid"
    start program = "/sbin/start apoxz"
    stop program  = "/sbin/stop apoxz"
    if failed port 8000 protocol HTTP
        request /
        with timeout 10 seconds
        then restart' > /etc/monit/conf.d/apoxz.conf

service nginx start

rm -rf Django-1.4.tar.gz Django-1.4

mysql -u root -p -e 'create database apoxz;'

echo 'Completed apoxz web installation.'
