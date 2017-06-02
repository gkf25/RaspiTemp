#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess


#definition des fonctions 

def eteindre():
    """Fonction permettant l'extinction du raspberry
    il est necessaire d'editer le fichier 'sudoers' à l'aide de la commande:
    sudo visudo
    operator ALL=/sbin/shutdown
    operator ALL=NOPASSWD: /sbin/shutdown"""
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


def mail(message):
	"""Parametre necessaire à l'envoi et la reception de mails pour etre informé de l'alerte  emise"""
    toaddr = "franck.mottas@gmail.com"
    fromaddr = "fmottas@parkeon.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "ALERTE temperature Raspberry!"
    body = message
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "pknfm7311!")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# recuperation de la valeur de la temperature    
with open(r'/sys/class/thermal/thermal_zone0/temp', 'r') as f:
    t = f.readlines()

# formattage de la temperature et de l'heure
temp = round(int(t[0])/1000,2)
date = datetime.datetime.now().strftime("%d-%m-%Y")
heure = datetime.datetime.now().strftime("%H:%M:%S")

# copie des données formatées dans le fichier defini par le path
path_dest =  r'/home/gkf/Documents/PiTemp/donnee'
with open(os.path.join(path_dest,date),'a') as f:
    f.write(str(temp))
    f.write("   ,   ")
    f.write(heure)
    f.write("\n")

# definition des diferents seuils et de leurs actions respective
if temp > 75: 
   avertissement = "La température a dépassée le seuil limite de 75°C, le raspberry va s'éteindre !"
   mail(avertissement)   
   eteindre()   
elif temp > 70:
    avertissement = "Le Raspberry a dépassé la température de 70°C, verifier le systeme !"
    mail(avertissement)
elif temp > 60:
    avertissement = "Le raspberry a depassé la température de 60°C, verifier le systeme !"
    mail(avertissement)

    
