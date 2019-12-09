PyPDF Manipuler des fichiers PDF avec Python
############################################
:date: 2013-10-20 09:11
:author: tristanlt
:tags: Python, pdf
:slug: pypdf-manipuler-des-fichiers-pdf-avec-python

.. raw:: html

   <div id="parent-fieldname-description"
   class="documentDescription kssattr-atfieldname-description kssattr-templateId-kss_generic_macros kssattr-macro-description-field-view">

En faisant Bookletizer.py j'ai découvert la bibliothèque python PyPDF
qui permet de manipuler des documents PDF via des scripts. Je vais
décortiquer le script que j'ai créé pour ré-ordonner les pages en mode
booklet.

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

.. code:: 

    # Import du moduleimport pyPdf[...]# ouverture du fichier PDF avec une execption# différente en cas de pbm fichier (fichier # inexistant) ou pbm PDF (le fichier n'est# pas un fichier PDF)try:    inputfile = pyPdf.PdfFileReader(file, "rb"))    inputfile.numPagesexcept IOError:    sys.exit("Input file error")except pyPdf.utils.PdfReadError:    sys.exit("Bad PDF file")[...]# Creation d'un simple fichier PDF vide (0 pages)# qui va recevoir les pages dans l'ordre booklet output = pyPdf.PdfFileWriter()[...]# Ajout d'une page dans le le fichier output#Ici c'est la page n° i de inputfile output.addPage(inputfile.getPage(i))# Pour finir écrivons le fichier outputoutputStream = file(options.outputfilename, "wb")output.write(outputStream)outputStream.close()

Avec cette librairie nous pouvons donc facilement tronquer, assembler,
mélanger ou re-indexer des documents.

.. raw:: html

   </div>

.. raw:: html

   </div>
