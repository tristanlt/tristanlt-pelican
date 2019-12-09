OpenStack haute-disponibilité #2 HAProxy
########################################
:date: 2015-11-21 13:29
:author: tristanlt
:tags: OpenStack, Ubuntu
:slug: openstack-haute-disponibilite-2-haproxy

|Logo OpenStack|\ Je poursuit donc la série de posts visant à expliquer
l'installation de contrôleurs OpenStack haute-disponibilité. Le sujet
est de maintenir le service sur les APIs de gestion et de console, et
non sur les machines virtuelles hébergées par l'infrastructure.

La `mise en place de
Keepalived </blog/openstack-ha-1/>`__ est expliquée
dans le post précédent. Notre cluster de test est constitué de 3 noeuds
(9lpo192, 9lpo134 et 9lpo135) et d'une adresse flottante qui peut passer
d'une machine à l'autre en cas de défaillance de son hôte.

L'adresse en question va être utilisée par les clients pour accéder aux
APIs de OpenStack (celle ci sera l'adresse des endpoints). 

|Haproxy with OpenStack|

Installation
============

Sur chacun des noeuds, nous installons HAProxy et apache2 (ce dernier va
servir de service de test) :

::

    $ aptitude install haproxy apache2

Apache2, par défaut, sert les fichiers présents dans /var/www/html dont
le fichier /var/www/html/index.html. Afin de vérifier le bon
fonctionnement de la répartition de charge et du failover, nous allons
personnaliser le fichier pour savoir avec qui nous discutons réellement.

Cette commande remplace le contenu du fichier servit par apache2 par le
hostname du noeuds :

::

    $ echo $HOSTNAME > /var/www/html/index.html

Mieux vaut vérifier le bon fonctionnement de nos serveur de test avant
de passer à la suite :

::

    $ curl http://172.16.9.192:80
    9lpo192
    $ curl http://172.16.9.134:80
    9lpo134
    $ curl http://172.16.9.135:80
    9lpo135

Configuration de HAProxy
========================

La configuration de HAProxy est déjà faites lors de l'installation du
paquet. D'autres paramètres intéressant peuvent être modifiés. Nous
allons ajouter une section pour servir notre fichier index.html sur le
port 4242.

Dans le fichier **/etc/haproxy/haproxy.html** il faut ajouter une
section pour notre service de test :

::

    listen testservice 172.16.9.200:4242
            balance source
            option tcpka
            option httpchk
            maxconn 10000
            server 9lpo134 172.16.9.134:80 check inter 2000 rise 2 fall 5
            server 9lpo135 172.16.9.135:80 check inter 2000 rise 2 fall 5
            server 9lpo192 172.16.9.192:80 check inter 2000 rise 2 fall 5

Nous déclarons donc un nouveau service écoutant sur l'\ `adresse
flottante gérée par
Keepalived </blog/openstack-ha-1/>`__, sur le port
4242.

Les options **tcpka** (tcp keepalived packet) et **httpchk** permettent
respectivement; de garder les sessions TCP ouvertes par l'envoi régulier
de paquets et de vérifer la bonne santé des serveurs http par l'envoi de
requètes http (toutes les 120 sec par défaut).

Cette configuration est à faire sur tous les noeuds, sachant que seul
celui qui dispose de l'adresse flottante gérée par Keepalived sera
réellement interrogé.

Sur tous les noeuds :

::

    $ service haproxy restart

Vérification
============

::

    $ curl http://172.16.9.200:4242
    9lpo134

Dans ce cas, c'est le serveur 9lpo134 qui a réellement répondu. **Si
l'on répète ce test 30 fois, nous obtenons toujours une réponse du même
serveur**, c'est l'option HAProxy **balance source** qui induit cela (le
noeud cible est déterminé par l'adresse cliente).

Si l'on modifie l'option HAProxy **balance source** par \ **balance
roundrobin**, chacun des serveurs seront mis à contribution à leurs
tours. Cette option est utilisable sur les APIs OpenStack car celles-si
fonctionnent sans états (`stateless
services <https://en.wikipedia.org/wiki/Stateless_protocol>`__).

Dans le fichier /etc/haproxy/haproxy.conf :

::

    listen testservice 172.16.9.200:4242
            #balance source
            balance roundrobin

Veillez à faire la modification (et le redémarrage du service HAProxy)
sur tous les noeuds afin d'éviter les surprises si la VIP Keepalived
venait à changer d'hôte. (l'idéal étant d'utiliser Puppet ou Chief pour
gérer ces configurations).

::

    $ curl http://172.16.9.200:4242
    9lpo134
    $ curl http://172.16.9.200:4242
    9lpo135
    $ curl http://172.16.9.200:4242
    9lpo192
    $ curl http://172.16.9.200:4242
    9lpo134
    ...

Ok, nous avons maintenant, une adresse IP qui peut changer d'hôte si le
besoin se fait sentir, et un répartiteur de charge qui permet de
distribuer les requettes sur les APIs seront installées sur nos
différents noeuds.

Pour installer les APIs, il nous faut maintenant les prérequis; un
serveur AMPQ et un serveur SQL.

.. |Logo OpenStack| image:: /img/.thumbnails/openstack-logo5.png/openstack-logo5-100x100.png
   :width: 100px
   :height: 100px
.. |Haproxy with OpenStack| image:: /img/haproxy.png
   :width: 482px
   :height: 374px
