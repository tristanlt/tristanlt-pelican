Docker #2 : Plone
#################
:date: 2014-06-07 06:01
:author: tristanlt
:tags: Debian, Docker
:slug: docker-2-plone

|image0|    This recipe is about Plone deployement for developement and
production with Docker and Buildout. I will write two DockerFile, first
one provide a great python environnement and second one which deploy a
Plone instance with iuem.sequestre. iuem.sequestre is a numeric vault to
store secrets. It's a Plone addon.

Python Docker Image Layer
-------------------------

First, I writes a Docker file to create an image based on Debian Wheezy.
Python needs some dependencies to builds (ie gcc...), in our DockerFile
we need to install this dependencies.

I create a new directory and create a new DockerFile

::

    mkdir tristanlt-python27 
    cd tristanlt-python27
    vim DockerFile

DockerFile
~~~~~~~~~~

::

    FROM debian:wheezy
    MAINTAINER Tristan LT « me@tristan.lt »

    ENV DEBIAN_FRONTEND noninteractive

    RUN (apt-get update && apt-get upgrade -y -q && apt-get dist-upgrade -y -q && apt-get -y -q autoclean && apt-get -y -q autoremove)
    RUN apt-get install -y -q git-core python build-essential python-distribute openssl libssl-dev
    RUN (mkdir -p /opt/BUILDOUT && cd /opt/BUILDOUT)
    RUN (cd /opt/BUILDOUT && git clone https://github.com/collective/buildout.python.git)
    RUN (cd /opt/BUILDOUT/buildout.python && sed -i '/python[2-3][1-6:8-9]/d' buildout.cfg )
    RUN (cd /opt/BUILDOUT/buildout.python && python bootstrap.py && ./bin/buildout )
    RUN (cd /opt/BUILDOUT/buildout.python )

Build
~~~~~

An now we can build this Docker Image

::

    sudo docker.io build --tag="tristanlt/python27"  --rm=true .

About params : docker create intermediates images for each RUN command.
When you develop an DockerFile, intermediates images may be useful
because docker build process don't rebuilds successful stages for
fastest build sequence. We you are sure, you can tell Docker to not keep
intermediates images with '--rm=true'.

Next, we can check our image :

::

    sudo docker.io images |grep tristanlt/python27
    tristanlt/python27        latest              61d7fa4d7535        2 weeks ago          502.6 MB

We have a fresh image with Python based on Debian Wheezy.

Plone Docker Image Layer
------------------------

I'll create an image layer named tristanlt/sequestre based on
tristanlt/python27 which install some Plone dependencies, clone a GitHub
repository, and finally build our Plone instance.

::

    mkdir tristanlt-sequestre 
    cd tristanlt-sequestre
    vim DockerFile

DockerFile
~~~~~~~~~~

This DockerFile builds an image based on tristanlt/python27 (FROM line),
installs supervisord and builds Plone. In this case, supervisord is a
good idea because Plone must be launch as non-root user. We need to
setup supervisord by injecting a special conf in /etc/supervisor/conf.d.
Next, we ask to Docker to start supervirsord process in place of Plone. 

::

    FROM tristanlt/python27
    MAINTAINER Tristan LT « me@tristan.lt »

    ENV DEBIAN_FRONTEND noninteractive

    RUN (apt-get update && apt-get upgrade -y -q && apt-get dist-upgrade -y -q && apt-get -y -q autoclean && apt-get -y -q autoremove)
    RUN apt-get install -y -q supervisor python-imaging python-lxml python-ldap python-cjson libssl-dev libsasl2-dev libldap2-dev libgif-dev libjpeg62-dev libpng12-dev libfreetype6-dev libxml2-dev libxslt1-dev
    RUN (cd /opt/ && git clone https://github.com/tristanlt/iuem.sequestre.git)
    ADD supervisord.conf /etc/supervisor/conf.d/sequestre.conf
    RUN adduser --system --disabled-password --shell /bin/bash --group --home /home/plone --gecos "Plone system user" plone
    RUN chown -R plone.plone /opt/iuem.sequestre
    RUN su plone -c "cd /opt/iuem.sequestre && /opt/BUILDOUT/buildout.python/python-2.7/bin/python bootstrap.py"
    RUN su plone -c "cd /opt/iuem.sequestre && ./bin/buildout"
    EXPOSE 8080
    CMD ["/usr/bin/supervisord"]

We also need a **supervisord.conf** in the same place than DockerFile
which will added in  **/etc/supervisor/conf.d** as **sequestre.conf**

::

    [supervisord]
    nodaemon=true

    [program:plone]
    command=/opt/iuem.sequestre/bin/instance console
    autostart=true
    autrestart=true
    user=plone

Build
~~~~~

An now we can build this Docker Image

::

    sudo docker.io build --tag="tristanlt/sequestre"  --rm=true .

And check

::

    sudo docker.io images |grep tristanlt/sequestre
    tristanlt/sequestre       latest              67a263ad9784        2 weeks ago         759.3 MB

Run Docker Container
--------------------

Finally, we can create and run our container with :

::

    sudo docker.io run -d --name="vault1" -P tristanlt/sequestre
    3f7a6bf3e7c8f17383e8085a4b8258cf62141c81f10b3405e45326d523adf594

| 
| About options :

-  -d tell to daemonize and not attach a tty
-  --name tell a name to our new container (optional but useful)
-  -P tell to map published container port 8080 to one host port

We can check if your container work with **docker.io ps** commande

::

    sudo docker.io ps
    CONTAINER ID        IMAGE                        COMMAND                CREATED             STATUS              PORTS                     NAMES
    3f7a6bf3e7c8        tristanlt/sequestre:latest   /usr/bin/supervisord   29 seconds ago      Up 29 seconds       0.0.0.0:49153->8080/tcp   vault1

We can get more informations about running containers with **docker.io
inspect** command. For instance, we should want have the host port where
8080 container port is mapped ?

::

    sudo docker.io inspect vault1 |grep HostPort
                         "HostPort": "49153"
                        "HostPort": "49153"

Test Docker Container
---------------------

We can try to access our container 8080 with address
http://127.0.0.1:<hostport>

Voila.

.. |image0| image:: /img/gallery/homepage-docker-logo.png
   :class: img_left
   :width: 121px
   :height: 100px
