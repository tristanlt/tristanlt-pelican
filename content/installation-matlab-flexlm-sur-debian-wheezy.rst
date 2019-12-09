Installation Matlab Flexlm sur Debian Wheezy
############################################
:date: 2014-01-22 10:13
:author: tristanlt
:tags: Debian, Flexlm
:slug: installation-matlab-flexlm-sur-debian-wheezy

.. raw:: html

   <div id="parent-fieldname-description"
   class="documentDescription kssattr-atfieldname-description kssattr-templateId-kss_generic_macros kssattr-macro-description-field-view">

|Debian Logo|\ Petite surprise lors de la mise en place d'un serveur de
licence Flexlm, sur une Debian Wheezy. En intéractif, le serveur de
licence se lance, lors du processus de démarrage, le serveur reste
inflexible! Ne 

.. raw:: html

   </div>

.. raw:: html

   <div
   class="documentDescription kssattr-atfieldname-description kssattr-templateId-kss_generic_macros kssattr-macro-description-field-view">

Un problème rencontré lors de l'installation du serveur Flexlm de Matlab
sur Debian Wheezy.

.. raw:: html

   </div>

.. raw:: html

   <div
   class="documentDescription kssattr-atfieldname-description kssattr-templateId-kss_generic_macros kssattr-macro-description-field-view">

.. raw:: html

   </div>

.. raw:: html

   <div
   class="documentDescription kssattr-atfieldname-description kssattr-templateId-kss_generic_macros kssattr-macro-description-field-view">

.. raw:: html

   </div>

.. raw:: html

   <div
   class="documentDescription kssattr-atfieldname-description kssattr-templateId-kss_generic_macros kssattr-macro-description-field-view">

Le système est une Debian Wheezy (testing rc1) 3.2.0-4-amd64.

.. raw:: html

   </div>

.. raw:: html

   <div id="content-core">

.. raw:: html

   <div id="parent-fieldname-text-a80639a9c98244cea2650c61ba239686"
   class="kssattr-atfieldname-text kssattr-templateId-widgets/rich kssattr-macro-rich-field-view kssattr-target-parent-fieldname-text-a80639a9c98244cea2650c61ba239686">

| J'ai fait l'installation du serveur de licence Matlab (flexlm) en
  suivant les indications fournie par Mathworks, le serveur fonctionnait
  lorsqu'il était lancé "à la main" par l'utilisateur non-privilégié
  mais pas lorsqu'il était lancé par la commande "/etc/init.d/flexlm
  start".
| J'avais les logs suivants :

::

    Apr 29 16:22:24 leserver kernel: [ 3371.877900] type=1702 audit(1367245344.001:56): op=follow_link action=denied pid=481 comm="lmboot_TMW" path="/var/tmp/lm_TMW.vd1" dev="sdb6" ino=391685 

| 
| Ceux ci sont relatifs a une nouvelle protection sur le noyau Linux
  (enable par défaut) : https://patchwork.kernel.org/patch/1667851/
| En gros, cette protection interdit l’exécution d'un binaire via un
  lien qui est placé dans un répertoire temporaire.

::

    root@leserver:~# ls -ld /var/tmp 
    drwxrwxrwt 2 root root 4096 Apr 30 11:13 /var/tmp 
    root@leserver:~# ls /var/tmp/lm_TMW.vd1 -l 
    lrwxrwxrwx 1 flexnet lpo 54 Apr 30 11:12 /var/tmp/lm_TMW.vd1 ->  /export/home1/matlab/MATLAB_R2012b.app/etc/glnxa64/MLM 

| 
| Cette protection peux être désactivée temporairement via :

::

    echo 0 > /proc/sys/fs/protected_symlinks 
    echo 0 > /proc/sys/fs/protected_hardlinks 

| 
| Ou durablement en créant un fichier :
  /etc/sysctl.d/disablesymhardprotect.conf (par exemple)
| Contenant :

::

    fs.protected_symlinks=0 
    fs.protected_hardlinks=0 

| 
| La solution la plus durable serait de modifier la méthode de lancement
  de flexnet pour prendre en compte cette nouvelle sécurité qui
  impactera tout les systèmes Linux d'ici quelques temps.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. |Debian Logo| image:: /img/gallery/debian.jpeg
   :width: 76px
   :height: 100px
