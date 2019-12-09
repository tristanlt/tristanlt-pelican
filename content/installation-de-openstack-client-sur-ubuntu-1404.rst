Installation de OpenStack Client sur Ubuntu 14.04
#################################################
:date: 2014-12-20 17:26
:author: tristanlt
:tags: Cloud, OpenStack, Ubuntu
:slug: installation-de-openstack-client-sur-ubuntu-1404

|image0|\ Le client fournit avec Keystone nommée sobrement **keystone**
est en passe d'être déprécié, les utilisateurs de OpenStack sont invités
a se tourner vers OpenStackClient (OSC) qui reprends les bibliothèques
de base des composants OpenStack en offrant une interface en ligne de
commande performante.

Malheureusement, l'installation sur Ubuntu 14.04 semble cassée. Voici
une méthode qui a le mérite de fonctionner.

::

    apt-get install libffi-dev libffi6 libssl-dev python-dev
    pip install pyOpenSSL
    pip install python-openstackclient

Ensuite, pour utiliser l'outil nommé (sobrement ou pas du tout)
**openstack**

::

    export OS_TOKEN=ADMIN123456
    export OS_URL='http://localhost:5000/v3/'
    openstack

Ou avec une authentification

::

    export OS_AUTH_URL=http://localhost:5000/v3/export OS_PROJECT_NAME=myprojectexport OS_USERNAME=myloginexport OS_PASSWORD=mypassopenstack

.. |image0| image:: /img/gallery/openstack-logo5.png
   :width: 100px
   :height: 100px
