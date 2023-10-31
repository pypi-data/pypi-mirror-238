"""
Configuration du Projet - setup.py.

Ce fichier de configuration définit les métadonnées et les informations nécessaires
à la construction et à l'installation du projet "my_task_manager".

Informations du Projet:
    - Nom: my_task_manager
    - Version: 1.3
    - Description: Un projet de gestion de liste de tâches (To-do List).
    - Auteurs: Alban Pereira, Yuchen Xia, Aurélien Raulo, Salimatou Traore
    - Emails des Auteurs: alban.pereira@telecom-paris.fr, yuchen.xia@telecom-paris.fr,
      aurelien.raulo@telecom-paris.fr, salimatou.traore@telecom-paris.fr
    - Packages: Recherche de tous les packages nécessaires pour le projet.
    - Dépendances: datetime, logging

Ce fichier est utilisé pour configurer le projet, y compris le nom, la version, la description,
les auteurs, les dépendances et les packages nécessaires pour l'installation. Il permet également
de spécifier les informations clés nécessaires à la distribution du projet.

Pour installer le projet, utilisez 'pip install .' dans le répertoire racine du projet.
"""


from setuptools import setup, find_packages

# Les données de projet
setup(
    name='my_task_manager',
    version='1.11',
    description='Métadonnées et informations sur la construction de projet To-do List',
    author='Alban Pereira, Yuchen Xia, Aurélien Raulo, Salimatou Traore',
    author_email='alban.pereira@telecom-paris.fr, yuchen.xia@telecom-paris.fr, \
                aurelien.raulo@telecom-paris.fr, salimatou.traore@telecom-paris.fr',
    packages=find_packages(),
    install_requires=[
        'datetime',
        'logging',
    ],
    zip_safe=False,
)

# view at https://pypi.org/project/my-task-manager/
