#!/usr/bin/env bash

sudo apt-get -qq -y install python3-venv openssh-server figlet

### Esto es para comunicarse con la maldita fiscal sin sudo
sudo apt-get -qq remove modemmanager -y
sudo usermod -a -G dialout $USER

############## SECURITY STUFF #################
#sudo apt-get -qq install fail2ban -y

#cd /etc/fail2ban
#sudo rm jail.local
#sudo sh -c 'echo "[GATOMALO]" >> jail.local'
#sudo sh -c 'echo "ignoreip = 127.0.0.1" >> jail.local'
#sudo sh -c 'echo "bantime  = 3600" >> jail.local'
#sudo sh -c 'echo "maxretry = 3 " >> jail.local'
#sudo sh -c 'echo "port = 5000" >> jail.local'
#sudo sh -c 'echo "logpath = /var/log/auth.log" >> jail.local'

#sudo service fail2ban restart
###############################################

if [ ! -d /gatomalo ] ; then
	sudo mkdir /gatomalo
	sudo chown $USER /gatomalo/ -R
	sudo chown $USER /gatomalo/* -R
	git clone git@github.com:Bluetide/gatomalo-fiscal.git /gatomalo
	cd /gatomalo
	python3 -m venv venv
	source venv/bin/activate
  pip install --upgrade wheel pip
	pip install -r requirement.txt
	sudo ln -s /gatomalo/gatomalo.service /lib/systemd/system/gatomalo.service
	figlet "GATOMALO"
	echo "setup exitoso!"
	echo "Configurar env vars en /gatomalo/gatomalo.service"
	echo "Encender con sudo service gatomalo start"
else
	echo "DIRECTORIO DE GATO MALO YA EXISTE"
fi
