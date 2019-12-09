OpenStack haute-disponibilité #3 RabbitMQ
#########################################
:date: 2015-11-22 14:46
:author: tristanlt
:tags: OpenStack, RabbitMQ
:slug: openstack-haute-disponibilite-3-rabbitmq

|RabbitMQ Logo|\ Les composants des APIs de OpenStack ont recours à un
serveur AMQP pour traiter les demandes de manière asynchrone, un message
est posté sur la file de message et les services qui exécutes réellement
le travail prennent les tickets et exécutent la tâche (tient, ça
ressemble à mon job).

Ce service est extrèmement important, la majorité des tâches sont
exécutées de cette manière (création de VM, destruction, création d'un
réseau...).

Nous allons donc renforcer le serveur AMQP RabbitMQ en le configurant en
mode cluster, par chance, RabbitMQ est nativement prévu pour cela. La
documentation officielle propose un `guide
sympatique <https://www.rabbitmq.com/clustering.html>`__ dont ce billet
n'est qu'une pâle adaptation.

Comme précédement lors de la `configuration de
Keepalived </blog/openstack-ha-1/>`__ et
l'\ `installation de
HAProxy </blog/openstack-haproxy/>`__, nous disposons
de trois noeuds ( 9lpo192, 9lpo134, 9lpo135) qui se connaissent bien
depuis le temps (résolution DNS ou /etc/hosts).

Installation de RabbitMQ
========================

Simplement, sur chacun des noeuds :

::

    aptitude install rabbitmq-server

On peut vérifier que le serveur est seul dans son cluster via :

::

    $ rabbitmqctl cluster_statusCluster status of node rabbit@9lpo192 ...[{nodes,[{disc,[rabbit@9lpo192]}]}, {running_nodes,[rabbit@9lpo192]}, {partitions,[]}]...done.

Histoire de cookies
===================

Pour dialoguer entre eux, les noeuds d'un cluster RabbitMQ doivent
partager quelque chose, un cookie. Moi quand je dois partager un cookie,
ça ne m'ouvre pas au dialogue, mais bon... Sous Linux, ce cookie est
placé dans le fichier */var/lib/rabbitmq/.erlang.cookie.*

Ce cookie est créé lors de l'installation du service rabbitmq-server.
Nous allons prendre le cookie de 9lpo192 :

::

    $ cat /var/lib/rabbitmq/.erlang.cookie
    UEOMRUIRMVISFTILGZW

Puis le diffuser sur tous les noeuds :

::

    $ echo "UEOMRUIRMVISFTILGZWU" > /var/lib/rabbitmq/.erlang.cookie

Mise en place du cluster
========================

Les noeuds disposent du cookie et font tourner leurs propres instances.
Nous allons paramétrer les serveurs RabbitMQ afin de les faire
fonctionner en mode cluster.

Sur **9lpo134** et **9lpo135**, nous allons :

#. Stopper le serveur
#. Ajouter l'hôte au serveur cluster
#. Démarrer le serveur

::

    $ rabbitmqctl stop_app
    $ rabbitmqctl join_cluster rabbit@9lpo192
    $ rabbitmqctl start_app

A la suite de quoi, nous pouvons vérifier que les serveurs RabbitMQ se
sont bien mis en cluster avec la commande (sur n'importe quel hôte) :

::

    $ rabbitmqctl cluster_status
    Cluster status of node rabbit@9lpo134 ...
    [{nodes,[{disc,[rabbit@9lpo134,rabbit@9lpo135,rabbit@9lpo192]}]}]
    ...done.

Par défaut, une file est hébergée sur un seul des hôtes du cluster (mais
accessible de tous). RabbitMQ permet de créer des files hautement
disponibles, ces files sont mise en mirroir sur les noeuds du cluster.

Pour activer les files de message hautement disponible (`Highly
Available Queues <https://www.rabbitmq.com/ha.html>`__), il faut
signaler au cluster que toutes les files seront de type mirroir :

::

    $ rabbitmqctl set_policy ha-all '^(?!amq\.).*' '{"ha-mode": "all"}'

Cette commande place toutes les files de message (amq.\*) dans le
**ha-mode all**, ce mode duplique la file sur chacun des noeuds.

Nous avons maintenant trois serveurs AMPQ qui fonctionnent en mode
cluster. Nous référencerons ces 3 serveurs sur les fichiers de
configuration afin que Oslo (composant OpenStack qui gère les fonctions
communes comme AMPQ) trouve toujours un endroit pour publier ou
consommer un message.

.. |RabbitMQ Logo| image:: /img/rabbitmq_logo_strap.png
   :width: 150px
   :height: 29px
