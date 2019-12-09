Docker #1 : un simple Dockerfile
################################
:date: 2014-04-05 13:08
:author: tristanlt
:tags: Debian, Docker, RabbitMQ
:slug: docker-1-un-simple-dockerfile

|image0|\ Docker permet d'industrialiser la mise en place de conteneurs
applicatifs (basés sur lxc). Le but est la mise en place
d'environnements de développement ou de SaaS (Software as a Service).
L'un des avantages de Docker, est la construction des containers eux
même. Ceux ci sont gérés sous forme de couche. Ansi, un hôte hébergeant
20 containers pour des WebApp Django, n'aura en mémoire qu'une seule
image système d'exploitation et selon les versions de la WebApp
disposera de plusieurs couches.

Dans l'exemple suivant, le service que l'on souhaite obtenir est un
gestionnaire de files de messages AMPQ RabbitMQ. Ce container sera
constitué d'une couche Debian Wheezy (elle même constitués de plusieurs
couches) et d'une couche que nous allons créer pour l'installation de
RabbitMQ, l'assemblage de ces couches donnera naissance à un container
rabbitmq-deb.

Voici donc un billet qui montre comment déployer facilement des RabbitMQ
avec Docker Je reprend simplement un `billet précédent sur
l'installation de
RabbitMQ </blog/rien-ne-sert-de-courrir-avec-rabbitmq/>`__
et refait cette installation dans un conteneur Docker. Le menu est le
suivant :

#. Installation de Docker
#. Ecriture du Dockerfile pour créer le container rabbitmq-deb
#. Manipulation du container

Installation de Docker
----------------------

Plaçons nous sur une fraiche installation de **Debian Wheezy** (pour moi
en VM qemu, amd64) en root. Puis nous allons suivre les `instructions
d'installation proposées sur le site de
Docker <http://docs.docker.io/en/latest/installation/ubuntulinux/>`__
(celles pour Ubuntu, Debian n'étant pas représenté :( )

::

    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
    echo "deb http://get.docker.io/ubuntu docker main" > /etc/apt/sources.list.d/docker.list
    apt-get update
    apt-get install lxc-docker

Ecriture du Dockerfile pour créer le container rabbitmq-deb
-----------------------------------------------------------

L'écriture d'un Dockerfile ressemble un peu à celle d'une recette de
cuisine: incorporer ça, faire ça, incorporer autre chose, faire cette
opération et cette autre opération. Voici les mots clefs de base pour la
création d'un container :

-  *FROM debian:wheezy* : Nous allons partir d'une base de Debian
   Wheezy, celle ci sera automatiquement téléchargé du dépôt
   communautaire de Docker.
-  *MAINTAINER Tristan LT « me@tristan.lt »* : Le nom du résponsable,
   surtout util lorsque l'on souhaite faire partager le container que
   l'on a créé en le poussant (PULL) sur le dépôt communautaire.
-  *RUN* : Faire cette opération
-  *ADD file.conf /pathto/file/oncontainer/file.conf* : Placer un
   fichier du répertoire contenant le fichier Dockerfile vers
   l'arborescence du nouveau container.
-  *EXPOSE 5672* : Du conteneur, nous ne verrons que les ports réseaux
   que nous demanderons explicitement de voir.
-  *ENTRYPOINT ['/usr/sbin/rabbitmq-server']* : Commande à lancer lors
   de l'instanciation du container (l'applicatif).

Voici l'exemple commenté :
~~~~~~~~~~~~~~~~~~~~~~~~~~

Création du répertoire pour notre DockerFile

::

    mkdir Docker-RabbitMQ
    cd Docker-RabbitMQ

Dans ce dossier nous allons avoir deux fichiers :

-  Dockerfile

::

    # This DockerFile setup a fresh RabbitMQ container
    # According to this simple configuration : http://tristan.lt/blog/rien-ne-sert-de-courrir-avec-rabbitmq/
    #
    FROM debian:wheezy
    MAINTAINER Tristan LT « me@tristan.lt »

    # Ne pas poser de questions debconf lors des phases d'installation
    ENV DEBIAN_FRONTEND noninteractive

    RUN (apt-get update && apt-get upgrade -y -q && apt-get dist-upgrade -y -q && apt-get -y -q autoclean && apt-get -y -q autoremove)
    RUN apt-get install -y -q rabbitmq-server
    ADD rabbitmq-env.conf /etc/rabbitmq/rabbitmq-env.conf

    EXPOSE 5672
    ENTRYPOINT  ["/usr/sbin/rabbitmq-server"]

-  rabbitmq-env.conf

::

    RABBITMQ_NODENAME='mq'
    RABBITMQ_CONFIG_FILE='/etc/rabbitmq/altconfig'

Création du container rabbitmq-deb
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nous allons utiliser la commande *docker build* afin de générer notre
nouveau conteneur. Avec en paramêtre *-t*, le nom du conteneur que nous
allons créer, et en entrée le répertoire dans lequel se trouve notre
Dockerfile (ici '.' ).

::

    root@klatch:~/Docker-RabbitMQ# ls 
    Dockerfile  rabbitmq-env.conf
    root@klatch:~/Docker-RabbitMQ# docker build -t rabbitmq-deb .
    ploading context 4.096 kB
    Uploading context 
    Step 0 : FROM debian:wheezy
     ---> a60f67605f28
    Step 1 : MAINTAINER Tristan LT « me@tristan.lt »
     ---> Using cache
    [...SNIP...]

Dans les grandes lignes, si l'hôte n'a jamais utilisé aucune des
sous-couches qui composent le container de base *debian:wheezy*, Docker
va télécharger celles-ci. Ensuite, Docker va instancier pour jouer notre
recette de cuisine Dockerfile. Pour finir, il va compiler toutes ces
différences pour créer une image de container qui n'est que la
différence avec l'image de base (debian:wheezy).

On peux contrôler la création de notre image de container en consultant
les images présentes sur la machine :

::

    root@klatch:~/Docker-RabbitMQ# docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
    rabbitmq-deb        latest              8ce8ba6dc683        9 minutes ago       207.8 MB
    <none>              <none>              5de48d3bdd31        16 hours ago        227.1 MB
    debian              unstable            b8e614427a50        3 days ago          125.3 MB
    debian              sid                 10c5dfd76853        3 days ago          125.3 MB
    debian              wheezy              a60f67605f28        4 days ago          118 MB
    [...SNIP...]

Manipulation du container
-------------------------

C'est bien beau de faire des containeurs, mais c'est aussi bien lorsque
cela sert à quelque chose. Nous allons donc démarrer ce beau conteneur.
Dans la commande suivante, le flag *-d* designe un démarrage en mode
démon, le *-p :5671* ouvrira les accès au container sur ce port (fermé
par défaut).

::

    docker run -d -p :5672 rabbitmq-deb

Et voila, votre conteneur est lancé ! On peux vérifier cela avec la
commande *docker ps* qui liste les conteneurs en vie.

::

    root@klatch:~# docker ps
    CONTAINER ID        IMAGE                 COMMAND                CREATED             STATUS              PORTS                 NAMES
    d5e4035a4d81        rabbitmq-deb:latest   /usr/sbin/rabbitmq-s   2 minutes ago       Up 2 minutes        15672/tcp, 5672/tcp   dreamy_nobel

Ensuite, les manipulations possibles (stop, status...) se feront avec le
container ID. Par exemple, pour récupérer l'adresse IP de notre
conteneur (`elle peut être fixée au moment du
run <http://docs.docker.io/en/latest/reference/commandline/cli/#run>`__
sinon), on peux utiliser la commande *docker inspect container\_id*

::

    root@klatch:~# docker inspect d5e4035a4d81 
    [{
        "ID": "d5e4035a4d8152c8d4018381d05dee8650fca755a777f693644245581367b521",
        "Created": "2014-04-06T06:33:44.939623026Z",
        "Path": "/usr/sbin/rabbitmq-server",
    [...SNIP...]
       "NetworkSettings": {
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16,
            "Gateway": "172.17.42.1",
            "Bridge": "docker0",
            "PortMapping": null,
            "Ports": {
                "15672/tcp": null,
                "5672/tcp": null
            }
    [...SNIP...]

Pour le reste, il faudra se tourner vers la commande *docker help* et
vers la `documentation Docker <http://docs.docker.io/en/latest/>`__.

Nous avons donc un conteneur qui répond sur le port 5672 de l'adresse
172.17.0.2 pour nous connecter à RabbitMQ. Cet exemple très simple
permet de comprendre ce que Docker peux apporter à certains déploiement
d'applications.

end

.. |image0| image:: /img/gallery/homepage-docker-logo.png
   :class: img_left
   :width: 121px
   :height: 100px
