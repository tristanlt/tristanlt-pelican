OpenStack haute-dispo #1 Keepalived
###################################
:date: 2015-11-14 14:12
:author: tristanlt
:tags: OpenStack, Ubuntu
:slug: openstack-haute-dispo-1-keepalived

|Logo OpenStack|\ Ce post est le premier d'une série de posts visant à
expliquer l'installation de contrôleurs OpenStack haute-disponibilité.
Le sujet est de maintenir le service sur les APIs de gestion et de
console, et non sur les machines virtuelles hébergées par
l'infrastructure.

|Keepalived3nodes|

Prenons 3 noeuds contrôleurs, sur ces noeuds fonctionneront les API
OpenStack ainsi que les services tiers incontournables au bon
fonctionnement d'OpenStack (RabbitMQ, MariaDB).

-  9lpo192 (172.16.9.192)
-  9lpo134 (172.16.9.134)
-  9lpo135 (172.16.9.135)

Prenons également une adresse flottante qui deviendra celle de nos point
d'accès (endpoints) aux APIs.

-  noocloud (172.16.9.200)

**Keepalived** est un service qui va garantir l'accessibilité de
l'adresse virtuelle (VIP) *noocloud* sur l'un des noeuds du cluster
keepalived. C'est l'une des fonctionnalitée de Keepalived.

*Sur chacun des noeuds.*

Il faut déja modifier du comportement du noyau via le fichier
*/etc/sysctl.conf*, cette option permet aux services de se fixer en
écoute (bind) sur une adresse inexistante sur le serveur (au démarrage
du service).

.. raw:: html

   <div>

::

    echo "net.ipv4.ip_nonlocal_bind=1" >> /etc/sysctl.conf
    sysctl -p

.. raw:: html

   </div>

Nous pouvons maintenant installer Keepalived

::

    aptitude install keepalived

Le fichier de configuration (**/etc/keepalived/keepalived.conf**) est
absent du paquet, il faut donc le créer soit même.

Voici celui pour 9lpo192 qui sera considéré comme master :

::

    global_defs {
       notification_email {
         xxx@youdomain.com
       }
       notification_email_from noocloud-root@yourdomain.com
       smtp_server smtp.yourdomain.com
       smtp_connect_timeout 30
    }

    vrrp_instance nooip {
        state MASTER
        interface eth0
        virtual_router_id 200
        priority 200
        advert_int 1
        authentication {
            auth_type PASS
            auth_pass Laevei0kifahkeejaiqu
        }
        virtual_ipaddress {
            172.16.9.200/24
        }
    }

Sur les autres noeuds, le même fichier doit être créé, à l'exclusion des
directives **priority** et **state** qui peuvent être différentes.

Sur **9lpo134**

::

    ...
    state BACKUP
    ...
    priority 100

Sur **9lpo135**

::

    ...
    state BACKUP
    ...
    priority 50

Ainsi, l'adresse IP *noocloud* ira: de préférence sur 9lpo192, en cas de
panne 9lpo134, puis sur 9lpo135

On (re)démarre maintenant keepalived *sur tous les noeuds du cluster*,
puis on vérifie que l'adresse a bien été affectée.

::

    service keepalived start
    ip -4 addr list eth0

Sur 9lpo192, on obtient bien notre VIP.

::

    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
        inet 172.16.9.192/25 brd 172.16.9.255 scope global eth0
           valid_lft forever preferred_lft forever
        inet 172.16.9.200/24 scope global eth0
           valid_lft forever preferred_lft forever

Pour tester la suite, il faut tuer le master (ne pas y aller trop fort,
un *halt* suffit), puis vérifier que l'adresse a bien changée de main...

Maintenant, que nous avons une adresse résiliente pour nos endpoints,
ils nous faut des services résilients ou bien répartir la charge...

.. |Logo OpenStack| image:: /img/openstack-logo5.png
   :width: 100px
   :height: 100px
.. |Keepalived3nodes| image:: /img/keepalived.png
   :width: 350px
   :height: 283px
