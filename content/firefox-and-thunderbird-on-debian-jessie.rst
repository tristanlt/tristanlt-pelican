Firefox and Thunderbird on Debian Jessie
########################################
:date: 2014-04-23 11:42
:author: tristanlt
:slug: firefox-and-thunderbird-on-debian-jessie

|image0|\ According to Debian rules for free software, Firefox and
Thunderbird aren't supplied with Debian. In place, Debian supplied
Iceweasel and Icedob, which are rebranded versions of Firefox and
Thunderbird without logos and copyrighted names. Here is a way to
retrieve our favorits softwares on our favorit but-a-little-punctilious
linux flavor.

We will create a new apt source which reference a repository maintained
by ubuntuzillateam. Don't be afraid, this is not an Ubuntu-only project,
just a project born in Ubuntu Forum.

First, create a new file **/etc/apt/sources.list.d/ubuntuzilla.list**,
like this (as root) :

::

    echo 'deb http://downloads.sourceforge.net/project/ubuntuzilla/mozilla/apt all main' > /etc/apt/sources.list.d/ubuntuzilla.list

Next, add repository security key, update and remove Debian official
packages:

::

    apt-key adv --recv-keys --keyserver keyserver.ubuntu.com C1289A29

::

    apt update

::

    apt remove iceweasel icedove

Finally, install firefox and thunderbird :

::

    apt install firefox thunderbird

And voila!

.. |image0| image:: /img/gallery/debian.jpeg
   :class: img_left
   :width: 76px
   :height: 100px
