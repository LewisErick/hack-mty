#!/bin/bash

PROJECT_DIR=/home/vagrant/site
USER_HOME=/home/vagrant

echo "Environment installation is beginning. This may take a few minutes.."

##
#	Install core components
##

#echo "Ubuntu Repository for MongoDB 3.0"
#apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
#echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

echo "Ubuntu Repository for PostgreSQL 9.4"
echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

echo "PostgreSQL 9.4 Import the repository signing key"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Install python 3.5
echo "Updating package repositories.."
add-apt-repository -y ppa:fkrull/deadsnakes
apt-get update
echo "Installing python 3.5 ..."
apt-get -y install python3.5

echo "Installing required packages.."
apt-get -y install git

echo "Installing and upgrading pip.."
apt-get -y install python-setuptools
easy_install -U pip

echo "Installing required packages for NFS file sharing for vagrant.."
apt-get -y install nfs-common

echo "Installing required packages for postgres.."
apt-get -y install postgresql-9.4 postgresql-client-9.4 postgresql-contrib-9.4 postgresql-server-dev-9.4

echo "Installing required packages for python package 'psycopg2'.."
apt-get -y install python-dev python3.5-dev libpq-dev

echo "Installing virtualenvwrapper from pip.."
pip install virtualenvwrapper

echo "Installing tree"
apt-get install -y tree

echo "Libraries for python Pillow"
apt-get install -y libtiff5-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk libjpeg8 libjpeg62-dev libfreetype6 libjpeg-dev zlib1g-dev

##
#	Setup the database
##

echo "Configuring postgres for ColorExperts..."
sudo -u postgres psql -c "create user color_usr with password 'color_pwd';"
sudo -u postgres psql -c "create database color_dev;"
sudo -u postgres psql -c "grant all privileges on database color_dev to color_usr;"
sudo -u postgres psql -d color_dev -c "CREATE EXTENSION IF NOT EXISTS hstore;"

##
#	Setup virtualenvwrapper
##
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ${USER_HOME}/.bashrc

##
#	Setup virtualenv
##
echo "Install the virtual environment.."
sudo su - vagrant /bin/bash -c "source /usr/local/bin/virtualenvwrapper.sh;cd ${PROJECT_DIR};mkvirtualenv --python=`which python3.5` site; deactivate;"

##
#	Setup is complete.
##
echo ""
echo "The environment has been installed."
echo ""
echo "You can start the machine by running: vagrant up"
echo "You can ssh to the machine by running: vagrant ssh"
echo "You can stop the machine by running: vagrant halt"
echo "You can delete the machine by running: vagrant destroy"
echo ""
exit 0
