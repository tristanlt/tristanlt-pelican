Rien ne sert de courrir avec RabbitMQ...
########################################
:date: 2014-03-03 09:26
:author: tristanlt
:tags: Debian, Linux, RabbitMQ
:slug: rien-ne-sert-de-courrir-avec-rabbitmq

RabbitMQ est un logiciel client/serveur permettant de passer des
messages de manière asynchrone entre des processus, qu'ils soient
hébergé sur une même machine ou sur des machines différentes. Je m'en
vais tester tout cela sur une Debian Wheezy, puis deux...

Installation du paquetage
~~~~~~~~~~~~~~~~~~~~~~~~~

Magiquement simple

.. code:: 

    root@ankh:~ # aptitude install rabbitmq-server
    [...SNIP...]
    Ajout du groupe « rabbitmq » (GID 106)...
    Fait.
    Ajout de l'utilisateur système « rabbitmq » (UID 104) ...
    Ajout du nouvel utilisateur « rabbitmq » (UID 104) avec pour groupe d'appartenance..
    Le répertoire personnel « /var/lib/rabbitmq » n'a pas été créé.
    [ ok ] Starting message broker: rabbitmq-server.


Quelques configurations utiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L'utilité sera de communiquer des ordres d'un processus tournant sur une
machine a un autre processus tournant sur une autre machine. Il faudra
donc que notre serveur RabbitMQ réponde sur le réseau (et pas sur toutes
les interfaces). Nous allons donc configurer cela grâce au fichier 
**/etc/rabbitmq/rabbitmq-env.conf** qui contient les variables
d'environnement passées au processus serveur RabbitMQ.

Fichier **/etc/rabbitmq/rabbitmq-env.conf**

.. code:: 

    RABBITMQ_NODENAME='mq'
    RABBITMQ_NODE_IP_ADDRESS='10.0.0.10'
    RABBITMQ_CONFIG_FILE='/etc/rabbitmq/altconfig'

Ici je précise également un fichier de configuration que nous pourrons
utiliser pour modifier le comportement par défaut du serveur. Si celui
ci n'existe pas, les configurations par défaut sont utilisées.

Afin de vérifier nos configuration nous allons redémarrer le service
RabbitMQ, demander son statut puis vérifier que celui ci écoute bien sur
l'interface adaptée.

.. code:: 

    root@ankh:~# /etc/init.d/rabbitmq-server stop
    [ ok ] Stopping message broker: rabbitmq-server.
    root@ankh:~# /etc/init.d/rabbitmq-server start
    [ ok ] Starting message broker: rabbitmq-server.
    root@ankh:~# /etc/init.d/rabbitmq-server status
    Status of node mq@ankh ...
    [{pid,4844},
     {running_applications,[{rabbit,"RabbitMQ","2.8.4"},
     {os_mon,"CPO  CXC 138 46","2.2.9"},
     {sasl,"SASL  CXC 138 11","2.2.1"},
     {mnesia,"MNESIA  CXC 138 12","4.7"},
     {stdlib,"ERTS  CXC 138 10","1.18.1"},
     {kernel,"ERTS  CXC 138 10","2.15.1"}]},
     {os,{unix,linux}},
     {erlang_version,"Erlang R15B01 (erts-5.9.1) [...SNIP...]\n"},
     {memory,[{total,25482848},
     [...SNIP...]
     {sockets_used,1}]},
     {processes,[{limit,1048576},{used,117}]},
     {run_queue,0},
     {uptime,5}]
    ...done.
    root@ankh:~# netstat -apn |grep 5672
    tcp        0      0 10.0.0.10:5672          0.0.0.0:*     LISTEN      4844/beam       
    root@ankh:~#

Ok, nous avons maintenant un serveur RabbitMQ prêt a prendre nos
messages.
