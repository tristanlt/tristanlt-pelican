Docker #3 : Commandes utiles
############################
:date: 2014-06-07 06:31
:author: tristanlt
:tags: Docker
:slug: docker-3-commandes-utiles

|image0|\ Voici quelques commandes très utiles pour démarrer avec
Docker. La commande que j'utilise est docker.io parce que dans Debian et
Ubuntu la commande docker était déjà prise.

Supprimer tous les containers avec leurs volumes (attention)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``sudo docker.io rm -f -v `sudo docker.io ps -a -q```

Supprimer toutes les images (attention)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``sudo docker.io rmi -f `sudo docker.io images -q```

Contruire une image à partir d'un DockerFile sans garder les containers intermédiaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``sudo docker.io build --rm=true --tag="tristanlt/python27" .``

Construire un container avec une image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``sudo docker.io run -d --name="python" -P tristanlt/python27``

Récupérer une image toute faite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``sudo docker.io pull tristanlt/python27``

Lancer une commande personnalisée dans une image (implique la création d'un container)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``sudo docker.io run -i -t tristanlt/python27 /bin/bash``

Créer une nouvelle image à partir d'un container en fonctionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Créer un nouveau tag une image existente

``sudo docker.io commit -m "Added Numpy and Scipy" (id ou nom du container)``
tristanlt/python27:sci

Créer une nouvelle image

| ``sudo docker.io commit -m "Added Numpy and Scipy" (id ou nom du container)``
  manouvelleimage

.. |image0| image:: /img/gallery/homepage-docker-logo.png
   :width: 121px
   :height: 100px
