RPI#2 : 2 boutons
#################
:date: 2013-10-20 08:59
:author: tristanlt
:tags: Electronic, Python, Raspberry
:slug: rpi2-2-boutons

Le montage
----------

Voici le montage, les boutons poussoir sont connectés sur les ports GPIO
#18 (pin 12) et GPIO #23 (pin 16).

 <http://tristan.lt/images/rpi-2-2-boutons/image>`__

Configuration des inputs
------------------------

Nous allons donc utiliser les pin **16 et 12 au sens GPIO.BOARD** ou les
n° GPIO **#18 et #23 au sens GPIO.BCM**. La commande suivante permettant
de placer le pin 16 en mode entrée.

.. code:: 

    GPIO.setup(button_pin1=16, GPIO.IN)

Pull up, down ou pas...
~~~~~~~~~~~~~~~~~~~~~~~

Un port GPIO en entrée peut être configuré pour avec une tolérance, ceci
afin de ne pas réagir aux interférences qu'il est succeptible de
recevoir. Nous avons fait un montage Pull-Down afin de protéger l'entrée
de ce type d'interférences.

Voir :
http://www.coactionos.com/embedded-design/28-using-pull-ups-and-pull-downs.html

Utilisation des Callbacks
~~~~~~~~~~~~~~~~~~~~~~~~~

La méthode la plus simple serait de vérifier toutes les microsecondes la
valeur de notre input comme cela :

.. code:: 

    while True:
        if GPIO.input(button_pin1):
              print('Bouton 1 enfoncé')
        if GPIO.input(button_pin2):
              print('Bouton 2 enfoncé')
     

 

Cette technique fonctionne mais présente 2 désagréments

-  Il faut mettre en place du code pour ne détecter que l'appuie
-  La consommation CPU monte en flêche
-  Plutôt que d'occuper notre CPU a vérifier l'état des boutons, une
   bonne méthode serait de configurer une interruption lors de l'appui
   sur celui-ci.

.. code:: 

    def button_one(channel):
     print('Bouton 1 presse !')

    GPIO.add_event_detect(button_pin1, GPIO.RISING)
    GPIO.add_event_callback(button_pin1, button_one, bouncetime=1000)

Nous commençons par définir une fonction (ici button\_one). Ensuite il
s'agit de branché le signal de l'évennement sur notre fonction.
**GPIO.add\_event\_detect** permet de dire s'il l'événement est
déclenché sur un front montant (appuie) ou descendant (relâchement) d'un
bouton, dans le cas d'un poussoir normalement ouvert.
**GPIO.add\_event\_callback** permet de branché l'événement configuré
pour notre bouton sur la fonction que nous avons établis.

bouncetime
~~~~~~~~~~

L'attribut **bouncetime** permet de gommer les imperfections physiques
des interrupteurs. En effet, à moins d'un interrupteur parfait, lors
d'un appui, le port reçoit un signal qui peux générer plusieurs
événements... Fâcheux, mais l'attribut **bouncetime** permet de ne pas
prendre en compte les nouveaux événements pour le délai définit (en
milisecond). Trop court nous risquons de générer plusieurs événements,
trop long et il faut attendre pour cliquer sur le boutons plusieurs
fois.

Notez que ce de-bounçage aurai pu être réaliser grâce a un condensateur
bien placé (mais où? :) ) .

Le code
-------

.. code:: 

    #!/usr/bin/env python3
    #-*- coding: utf-8 -*- 

    import RPi.GPIO as GPIO,time
    import signal, sys

    DEBUG = 1
    GPIO.setmode(GPIO.BOARD)


    button_pin1 = 16
    GPIO.setup(button_pin1, GPIO.IN)
    button_pin2 = 12
    GPIO.setup(button_pin2, GPIO.IN)

    # Definition d'une fonction qui est appelée lors du ctrl+c
    # celle-ci remet a zero les bus du RPI
    def stop(signal, frame):
     print('SIGINT > Sortons !')
     GPIO.cleanup()
     sys.exit(0)

    def button_one(channel):
     print('Bouton 1 presse !')

    def button_two(channel):
     print('Bouton 2 relache !')


    # Branchement  du signal SIGINT sur notre fonction de sortie
    signal.signal(signal.SIGINT, stop)

    # Branchement d'une fonction de callback sur le front montant créé par l'appuie sur le bouton
    GPIO.add_event_detect(button_pin1, GPIO.RISING)
    GPIO.add_event_callback(button_pin1, button_one, bouncetime=1000)

    # Branchement d'une fonction de callback sur le front descendant créé pare relachement du bouton
    GPIO.add_event_detect(button_pin2, GPIO.FALLING)
    GPIO.add_event_callback(button_pin2, button_two, bouncetime=1000))
    # Pour toujours...
    while True:
     time.sleep(1)

 

GO
--

.. code:: 

    root@raspberrypi:~# python3 button.py 
    Bouton 2 relache !
    Bouton 1 presse !
    Bouton 1 presse !
    Bouton 1 presse !
    Bouton 1 presse !
    Bouton 2 relache !
    Bouton 2 relache !

.. |image0| image:: /img/gallery/image_large.png
   :width: 300px
   :height: 357px
