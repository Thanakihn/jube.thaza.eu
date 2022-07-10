---
layout:     post
title:      Timelapse (partie 1)
date:       10/07 2022
summary:    Jouer avec des API et rentabiliser une Raspberry qui s'ennuie
categories: tech
thumbnail:  efelant
tags:
 - python
 - raspberry
 - photographie
 - video
custom_css: tech
---
<i> Attention : je dispose de très peu de compétences en codage et j'ai finalement assez peu de culture des différents logiciels qui existent pour réaliser différentes tâches. Ce post relate donc le voyage d'un amateur d'informatique qui essaie de mener un projet personnel. Il y aura donc probablement des erreurs d'interprétation dans les explications les plus théoriques. Vous voilà prévenus, bonne lecture </i>


<right><i>«Je vais profiter de ce blog pour tenir mon journal de bord»   L'auteur, il y a deux mois</i></right>

Bien qu'étant incapable de tenir mes promesses de régularité dans la tenue de ce blog, il est temps d'y proposer un nouvel article. 
Plus technique cette fois-ci. Alors que nous travaillions au labo, mon collègue H. a eu une excellente idée: «Ça serait stylé de faire un timelapse d'une journée au labo».
Je ne pouvais l'approuver. De plus, puisque mon projet de [Jupyter Hub](https://towardsdatascience.com/setup-your-home-jupyterhub-on-a-raspberry-pi-7ad32e20eed) était tombé à l'eau, j'avais une RaspberryPi inutilisée. Pourquoi faire simple alors ? Voilà donc les solutions que j'ai trouvé pour contrôler mon appareil photo avec une *Raspberry Pi Zero 2 (rpi)*. 


# Contrôler un appareil photo avec un ordinateur, une tâche simple ?

## Nikon, Windows et mon amour du logiciel libre

Pour réaliser un timelapse, il suffit de prendre des photos à interval régulier puis à coller ces images les unes aux autres pour faire une vidéo. On peut percevoir ça comme un ralenti (ou plan en *slow motion*) de l'extrême. Il faut donc que l'on commande la prise de photos avec un ordinateur (ici l'ordinateur sera une carte Raspberry Pi).

L'appareil que j'utilise est un Nikon. Je tombe assez rapidement sur la page officiel du logiciel [Camera Control Pro](https://downloadcenter.nikonimglib.com/en/download/sw/217.html). C'est le logiciel qui semble conseillé sur les forums de photographes. Cependant c'est un logiciel propriétaire et payant et qui ne tourne pas sous Linux, encore moins sur un micro-ordinateur comme la rpi.

Pour trouver une alternative, il y a des sites dédiés, par exemple [alternativeto.net](https://alternativeto.net/software/camera-control-pro/). C'est ainsi que je découvre le merveilleux logiciel [entangle](https://entangle-photo.org/). J'active le mode contrôle par ordinateur dans les paramètres de l'appareil photo, je le branche à l'ordinateur, j'ouvre *entangle* et tadaaa:

<figure>
   <img src="{{site.url}}/assets/2022-timelapse/entangle.png" 
      alt="Capture d'écran du programme entangle"/>
<figcaption><center><b> Le programme *entangle* fonctionne du premier coup youhou</b></center></figcaption>
</figure>

Bon, c'est super mais ça ne me dit pas comment faire pour contrôler l'appareil photo avec un code informatique (un script). En lisant la FAQ de *entangle*, on peut se rendre compte que le logiciel est basé sur un logiciel libre, sous licence GNU LPLG : [gPhoto2](http://www.gphoto.org/). C'est toujours le même concept : quoi que vous vouliez faire en informatique, il y a probablement un logiciel libre qui le fait déjà. En plus de trouver cette librairie, je trouve son [interfaçage sur Python](https://pypi.org/project/gphoto2/), ce qui me rend très heureux car au lieu de faire un vrai code je pourrais donc faire un script Python :).

## gPhoto2 sur rpi

Maintenant que nous connaissons les technologies que nous allons utiliser, nous pouvons préparer notre rpi. J'utilise [rpi-imager](https://www.raspberrypi.com/software/) pour installer la version légère de RaspberryPi OS sur une carte micro-sd. J'apprécie de pouvoir me connecter directement en ssh à ma carte donc je paramètre le wifi et les paramètres ssh grâce à cet assistant. Toutes les options sont disponibles dans le programme *rpi-imager*. Notons que par défaut, les paramètres de sécurités sont quelque peu discutable, il faudra donc les durcir avant de quitter mon réseau local. 

Pour ce connecter à la carte, on attend qu'elle s'allume et on trouve son adresse ip grâce à nmap. Par exemple j'utilise la commande :
`nmap -PA 10.0.0.*` qui liste tous les appareils sur mon réseau local. Une fois que l'on connaît son adresse, on peut se connecter à la carte en ssh : `ssh pi@10.0.0.252`. 

Une fois connecté à la carte, nous pouvons installer *gPhoto2* selon les instructions de la [page officielle](https://pypi.org/project/gphoto2/#raspberry-pi), après avoir mis-à-jour le système et installé les dépendances:
```
sudo apt-get update && sudo apt-get upgrade && sudo apt-get autoremove
sudo apt-get install python3
sudo apt-get install python3-pip libgphoto2
sudo pip3 install -v gphoto2 --no-binary :all:
```

Nous avons la bonne surprise de trouver de nombreux exemples pré-installés dans le dossier `/usr/local/lib/python3.9/dist-packages/gphoto2/examples/`. Même pas besoin de lire quoi que ce soit on peut deviner comment ça marche. Comme je manque de place dans la marge, je vais vous épargner les explications mais en me basant sur les exemples de [Jim Eastbrook](https://github.com/jim-easterbrook/python-gphoto2), je monte deux scripts :
- [le premier pour capturer une simple image]({{site.url}}/assets/2022-timelapse/script_captureimage.py)
- [le second pour prendre des images à intervalle régulier puis les compresser dans une archive.]({{site.url}}/assets/2022-timelapse/script_timelapse.py)


Les scripts fonctionnent, c'est super !

<figure>
   <img src="{{site.url}}/assets/2022-timelapse/rpi.jpg" 
      alt="Image capturée grâce à la rpi"/>
<figcaption><center><b> Image capturée grâce à une commande à distance à travers la raspberry pi | T.Blandin</b></center></figcaption>
</figure>

Notons que pour récupérer les fichiers de la carte, il suffit d'utiliser `scp` : `scp pi@10.0.0.252:/tmp/pictures/picture0000.jpg ~/`

## Conclusion de la première partie

On note que l'on pourrait théoriquement utiliser le programme [ffmpeg](https://ffmpeg.org/) afin de directement transformer les image en une vidéo, cependant, je n'arrive pas à faire fonctionner ce programme sur la rpi alors qu'il tourne parfaitement sur mon ordinateur portable. Je soupçonne l'absence de carte vidéo de la rpi de poser un problème. 
 On a bien avancé sur le projet mais il y a un important souci qui persiste : je ne peux pas me connecter à la carte via mon réseau local dans le labo. Ce sera l'objet du prochain article de cette courte série. 
 
 Mes sincères salutations !
 
 


