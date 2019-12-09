Créer un booklet avec PyPDF
###########################
:date: 2013-10-20 09:34
:author: tristanlt
:tags: Python, pdf
:slug: creer-un-booklet-avec-pypdf

.. raw:: html

   <div id="parent-fieldname-description"
   class="documentDescription kssattr-atfieldname-description kssattr-templateId-kss_generic_macros kssattr-macro-description-field-view">

Si il manque bien une fonctionnalité dans les logiciels libres de
visualisation de PDF, c'est l'impression de livret (booklet). Acroread
dispose de cette fonction fort utile lorsque l'on veux économiser du
papier, imprimer un document en mode Booklet permet de diviser la
consommation de papier par 4 et d'avoir un document pratique à utiliser.

.. raw:: html

   </div>

.. raw:: html

   <div id="viewlet-above-content-body">

.. raw:: html

   </div>

.. raw:: html

   <div id="content-core">

.. raw:: html

   <div id="parent-fieldname-text"
   class="plain kssattr-atfieldname-text kssattr-templateId-newsitem_view kssattr-macro-text-field-view">

La dernière fois que j'ai essayé la fonction booklet de Acroread, celui
ci n'en a fait qu'a sa tête, il me retournait les feuilles dans tous les
sens... Galère... J'ai donc développé un script Python nommé
**bookletizer.py** qui s'appuie sur la bibliothèque
`PyPDF <http://pybrary.net/pyPdf/>`__. Ce script permet de reclasser les
pages dans l'ordre ad-hoc pour une impression *en mode 2 page par
feuille avec recto verso sur les bord courts*.

Téléchargez `Bookletizer.py <http://tristan.lt/docs/bookletizer.py>`__

Pour l'utiliser vous devez disposer de python et installer la librairie
python `PyPDF <http://pybrary.net/pyPdf/>`__. Par exemple, si vous êtes
sous Linux Debian ou Ubuntu, installez juste le paquetage
**python-pypdf**

::

    tletou@ankh:~# sudo aptitude install python-pypdf

Vous pouvez également vous servir de easy\_install

::

    tletou@ankh:~# sudo  easy_install PyPDF

Le script reçoit deux paramètres qui sont le fichier d'entrée (-i
PDF\_FILE ) et le fichier de sortie (-o PDF\_FILE).

::

    aquarius ~/ > ./bookletizer.py -i blenderbpy.pdf -o blenderbpy-booklet.pdf ('Adding ', 2, ' blanks pages')Please print this document 2-sheets per page with duplex on shorts edges - bookletizer.py

Téléchargez `Bookletizer.py <http://tristan.lt/docs/bookletizer.py>`__

N'hésitez pas à me rapporter tout problème rencontré lors de son
utilisation.

.. raw:: html

   </div>

.. raw:: html

   </div>
