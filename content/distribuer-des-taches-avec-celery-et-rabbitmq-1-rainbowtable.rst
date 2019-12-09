Distribuer des tâches avec Celery et RabbitMQ #1 (RainbowTable)
###############################################################
:date: 2014-04-01 04:09
:author: tristanlt
:tags: Python, RabbitMQ
:slug: distribuer-des-taches-avec-celery-et-rabbitmq-1-rainbowtable

|Python Logo|\ RabbitMQ est un service de gestion de file d'attente pour
tâche, particulièrement utilisé lorsque l'on souhaite distribuer un
travail sur de multiples unités de travail. Attention, la communication
inter-processus n'étant pas gérée cette façon de faire ne peut pas se
substituer a MPI et consort! Dans le cas présent et a toute fin de test
(gnarf, gnarf, gnarf), nous souhaitons réaliser une `rainbow
table <http://fr.wikipedia.org/wiki/Rainbow_table>`__. Une rainbow table
est une base de données de mot de passe avec son équivalent chiffré
(hash). Pour bien montrer l'avantage du procédé, j'ai choisit une
fonction de hash hyper couteuse en temps CPU :
`bcrypt. <http://fr.wikipedia.org/wiki/Bcrypt>`__

Le billet suivant nécessite d'avoir installé et configuré RabbitMQ
(`voir mon billet
précédent </blog/rien-ne-sert-de-courrir-avec-rabbitmq/>`__)
et d'avoir installé `Celery <http://www.celeryproject.org/>`__.

::

    pip install celery

Le cas (sans Celery)
--------------------

Le script suivant génère 1000 mots de passe aléatoires de 30 caractères
(A-Z, a-z, 0-9). Dans un cas réel on utiliserait un dictionnaire de mots
de passe classiques. Pour chacun des mots de passe, on génère le hash
associé et écrit le couple motdepasse:hash dans un fichier.

::

    #!/usr/bin/env python
    # -*- coding: utf8 -*-

    import bcrypt
    import string
    import random
    import datetime

    n = 1000
    nbcharpass = 30
    workdir='/home/tletou/tmp/'
    # Generation de n passwords aleatoires de 30 carateres
    passwords=[]
    for i in range(n):
        passwords.append("".join([random.choice(string.letters+string.digits) \
                                   for x in range(1, nbcharpass)]))

    # Generation du nom de fichier de sortie
    filename=workdir+"/hashs-"+passwords[0]+"-"+passwords[-1]+".txt"

    file=open(filename,'w')
    t1 = datetime.datetime.now()
    # Pour chacun des mots de passe, generation des hashs bcrypt
    for clearpass in passwords:
        file.write(clearpass+":"+bcrypt.hashpw(clearpass, bcrypt.gensalt())+"\n")
    t2 = datetime.datetime.now()
    file.close()
    print(str((t2-t1).microseconds/float(n))+"us/hash")

| 
| Lorsque l'on tourne ce petit programme Python, la machine calcul sur
  un CPU, c'est long, et une RainbowTable de 1000 hash est complètement
  inexploitable (il en faut beaucoup beaucoup plus). Bref, c'est loin
  d'être optimal.

Utilisation de Celery
---------------------

Notre cas se prête bien au jeu car on peut facilement découper notre
travail pour le subdiviser en moult morceaux (appelés ici chunk) pour le
distribuer.

Notre job Celery se découpe en deux parties : le **worker** et le
**commander**.

Worker
~~~~~~

Le worker va s'accrocher à un broker (queue de message) RabbitMQ (`ou
Redis, ou
autre... <http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html>`__)
de manière à recevoir les taĉhes envoyées par le commander. Il est
constitué d'une partie configuration qui se passe presque de commentaire
(d'ailleur je commente pas) et d'une ou plusieurs commandes affublées du
décorateur **@app.task**.

Ici le fichier s'appel **rainbowwkr.py**

::

    from celery import Celery
    import bcrypt

    app = Celery('rainbow', broker='amqp://10.0.0.10//')
    app.conf.CELERY_TASK_SERIALIZER = 'json'
    app.conf.CELERY_RESULT_BACKEND = 'amqp'
    app.conf.CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.


    @app.task
    def processchunk(chunk, workdir):
        # Generation du nom de fichier de sortie
        filename=workdir+"/hashs-"+chunk[0]+"-"+chunk[-1]+".txt"
        file=open(filename,'w')
        for clearpass in chunk:
            file.write(clearpass+":"+bcrypt.hashpw(clearpass, bcrypt.gensalt())+"\n")
        file.close()
        return(filename)

Ici, notre fonction processchunk reçoit une liste de mot de passe et un
répertoire pour écrire son fichier de sortie. Elle retourne le nom du
fichier de sortie lorsque le sous-job est terminé.

Pour lancer notre worker sur une machine, il faut utiliser la commande
suivante dans le répertoire contenant le fichier Python du worker.

::

    celery worker -A rainbowwkr

A ce point, on peut se placer sur une autre machine ayant accès au
serveur RabbitMQ et lancer un autre worker. Mais même sans cela la magie
de Celery opèrera.

Commander
~~~~~~~~~

Notre script **commander** va : générer la table de mot de passe de
test, découper cette table, envoyer ces morceaux sur la file de message
RabbitMQ.

Notre fichier **rainbowcmd.py**

::

    #!/usr/bin/env python
    # -*- coding: utf8 -*-

    import string
    import random
    import rainbowwkr
    import datetime

    # 1000 mot de passe de 30 caractères
    n = 1000
    nbcharpass = 30
    # Nombre de division (en combien de tache sera divise notre job)
    nbchunk=10
    workdir='/home/tletou/tmp/'

    # Generation de n password aleatoires de 30 carateres
    passwords=[]
    for i in range(n):
        passwords.append("".join([random.choice(string.letters+string.digits) \
                                   for x in range(1, nbcharpass)]))

::

    # Decoupage, embalage et acheminement
    for i in range(nbchunk):
        # Calcul des intervales pour le decoupage du domaine
        start=i*(n//nbchunk)
        end=i*(n//nbchunk)+(n//nbchunk)-1
        # Creation des taches 
        result=rainbowwkr.processchunk.delay(passwords[start:end],workdir)

Maintenant, si nous lançons le commander avec python, les workers vont
s'agiter. Surveillez la charge CPU, vous verrez que celle-ci est
maintenant bien réparti sur les coeurs de la machine ou des machines.

::

    python rainbowcmd.py

Pour l'instant, je n'ai pas traité le "chronomètre" car il n'est
finalement pas si facile que cela de connaitre l'état d'avancement des
tâches. Je vais explorer ces fonctions et cela fera l'occasion d'un
nouveau billet.

Je ne peux partir sans citer IZ : "Dreams really do come true ooh ooooh"
(Over the rainbow).

.. |Python Logo| image:: /img/python.png
   :class: img_left
   :width: 188px
   :height: 100px
