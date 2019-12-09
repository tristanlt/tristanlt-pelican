RPI#1 : 2 diodes
################
:date: 2013-10-23 09:10
:author: tristanlt
:tags: Electronic, Python, Raspberry
:slug: rpi1-2-diodes

.. raw:: html

   <div id="parent-fieldname-description"
   class="documentDescription kssattr-atfieldname-description kssattr-templateId-kss_generic_macros kssattr-macro-description-field-view">

Utilisation du GPIO du Raspberry Pi pour faire clignoter deux LEDs en
alternance.

.. raw:: html

   </div>

.. raw:: html

   <div id="viewlet-above-content-body">

.. raw:: html

   </div>

Montage
-------

Nous allons utiliser les pins 16 et 18 de l'interface GPIO. Le montage
est on ne peux plus simple, nous récupérons la masse ( pin 6 : GND ) sur
la breadbox, chacune des diodes est protégée par une résistance de 330
Ohms. La programmation du port GPIO permettra d'envoyer ou non du
courant dans notre circuit.

|RPI 1 Schema|

Programme
---------

Le programme est lui aussi très simple; selon l'état d'un booléen nous
allons, soit allumer vert, éteindre rouge et inverser le booléen, soit
allumer rouge, ,éteindre vert et inverser le booléen, et cela dans une
boucle infinie.

Une sortie sans accroc
~~~~~~~~~~~~~~~~~~~~~~

Pour sortir du programme et donc de la boucle infinie, il faut taper
ctrl+c, cela arrête le prgramme la ou il en est et laisse les états du
GPIO dans l'état. Ce n'est pas une bonne idée pour plusieurs raisons (
voir ; 
http://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi
). Nous allons donc capturer le signal envoyer par ctrl+c pour remettre
a zéro les états GPIO modifiés par notre programme grace à la commande
**GPIO.cleanup()**.

Il suffit de créer une fonction qui quitte proprement, ici la fonction
**stopBlinking** puis à l'aide de la commande signal de "brancher" le
SIGINT (interruption par ctrl+c ou envoi du signal 2).

Configuration des pins GPIOs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Celle la est assez importante et assez déroutante quand comme moi on ne
lit jamais les documentations techniques avant de se lancer. Ici on
aborte la différence entre les adresses GPIO notées #21 ou P21 et les n°
de pins (de connecteur) sur le connecteur GPIO, completements différents
mais utilisables tous les deux.

Dans le programme ci dessous, nous utilisons **GPIO.BOARD** qui
configure le fait que nous allons utiliser les n° de pins pour signaler
quelles interfaces GPIO nous souhaitons piloter. L'autre mode
**GPIO.BCM** utilise les n° d'interface.

Une interface GPIO peut être une entrée et une sortie,  les nôtres
seront des sorties.

.. code:: 

    #!/usr/bin/env python
    import RPi.GPIO as GPIO,time
    import signal, sys

    def stopBlinking(signal, frame):
     GPIO.cleanup()
     sys.exit(0)

    signal.signal(signal.SIGINT, stopBlinking)

    GPIO.setmode(GPIO.BOARD)
    GREEN_LED = 16
    RED_LED = 18
    GPIO.setup(GREEN_LED, GPIO.OUT)
    GPIO.setup(RED_LED, GPIO.OUT)


    print('Press ctrl+c to stop blinking\n')
    switch = True
    while True:
     if switch:
     GPIO.output(GREEN_LED, True)
     GPIO.output(RED_LED, False)
     switch = False
     else:
     GPIO.output(GREEN_LED, False)
     GPIO.output(RED_LED, True)
     switch = True
     time.sleep(.1)

Go
~~

Nous allons maintenant pouvoir lancer notre programme pour admirer le
miracle technologique en route... Placez vous en super-utilisateur et
lancez :

.. code:: 

    python3 swtichRedGreen.py

.. |RPI 1 Schema| image:: /img/gallery/rpi-1-2.png
   :width: 300px
   :height: 554px
