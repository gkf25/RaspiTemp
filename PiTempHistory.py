#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import datetime
import shutil

path_source = r'/home/gkf/Documents/PiTemp/donnee'
path_dest = r'/home/gkf/Documents/PiTemp/history'
path_svg = r'/tmp/svg_PiTemp'
date = datetime.datetime.now().strftime('%d-%m-%Y')

for ele in os.listdir(path_source):
    with open(os.path.join(path_source, ele), 'r') as fsource:
        liste = [(round(float(ele[:5]),2), ele[-9:-1]) for ele in fsource.readlines()]
        liste_temp = [ele[0] for ele in liste]
        Tmax, Tmin, Tmoy = (max(liste_temp), min(liste_temp), round(sum(liste_temp)/len(liste_temp),2))
        Hmax, Hmin = liste.pop(liste_temp.index(Tmax))[1] , liste.pop(liste_temp.index(Tmin))[1]

    with open(path_dest, 'a') as fdest:
        ligne =  "({:.2f},{}) , {:.2f} , ({:.2f},{}) , {}\n".format(Tmin, Hmin, Tmoy, Tmax, Hmax, date)
        fdest.write(ligne)

    shutil.copy2(os.path.join(path_source, ele), os.path.join(path_svg, ele))
    os.remove(os.path.join(path_source, ele))


