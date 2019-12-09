Docker #4 : Build Docker from sources
#####################################
:date: 2014-06-08 12:10
:author: tristanlt
:tags: Docker, Ubuntu
:slug: docker-4-build-docker-from-sources

|image0|\ Docker is still in developpement. I'm experiencing
bug \ `#4068 <https://github.com/dotcloud/docker/issues/4068>`__ which
been corrected on master but not else in Ubuntu 14.04 packages. I will
build Docker from sources with... Docker itself.

Prepare environnement
---------------------

First, we must install Docker and git on our system, link binary named
docker.io to /usr/local/bin/docker. Finally, to avoid uses root or sudo
to each Docker relative commands add your user to docker group.

::

    sudo aptitude install docker.io git
    sudo ln -s /usr/bin/docker.io /usr/local/bin/docker
    sudo usermod -G docker -a tletou

We must logout and login to applied new group membership.

Start building (as normal user)
-------------------------------

These commands clone docker's sources, downloads some base images for
building.

::

    git clone https://github.com/dotcloud/docker.git
    cd docker
    make build

These commands build Docker binary.

::

    make binary

We must see this victory message :

::

    [...]
    ---> Making bundle: binary (in bundles/0.12.0-dev/binary)
    Created binary: /go/src/github.com/dotcloud/docker/bundles/0.12.0-dev/binary/docker-0.12.0-dev

Our new docker command should be in bundles/0.12.0-dev/binary

::

    tletou@aquarius:~/LPO/virt/docker/docker$ ls -l bundles/0.12.0-dev/binary/
    total 17180
    lrwxrwxrwx 1 root root       17 juin   8 15:17 docker -> docker-0.12.0-dev
    -rwxr-xr-x 1 root root 17582674 juin   8 15:17 docker-0.12.0-dev
    -rw-r--r-- 1 root root       52 juin   8 15:17 docker-0.12.0-dev.md5
    -rw-r--r-- 1 root root       84 juin   8 15:17 docker-0.12.0-dev.sha256

Use it
------

We will remove our link to package provided binary from /usr/local/bin
and linking to our new binary.

::

    sudo rm /usr/local/bin/docker
    sudo ln -s $PWD/bundles/0.12.0-dev/binary/docker-0.12.0-dev /usr/local/bin/docker
    # For compatibility with previous scripts and posts
    sudo ln -s $PWD/bundles/0.12.0-dev/binary/docker-0.12.0-dev /usr/local/bin/docker.io

Stop docker service and edit /etc/default/docker.io to point our new
binary

::

    sudo service docker.io stop
    sudo vim /etc/default/docker.io

Uncomment line:

::

    DOCKER="/usr/local/bin/docker"

Start service

::

    sudo service docker.io start
    docker -v 
    Docker version 0.12.0-dev, build 0c611d9

That's all falks.

.. |image0| image:: /img/gallery/homepage-docker-logo.png
   :width: 100px
   :height: 83px
