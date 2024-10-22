# ProjetETSIlyes
Lien du dossier google drive contenant touts les fichiers extraits et utilisés dans le projet :
https://drive.google.com/drive/folders/1MVkSx81zCHLOEI4EFHq4PfyJRqQp2UIv?usp=sharing

Lien du Github repo : 
https://github.com/ilyesox/ProjetETSIlyes.git


1.	Extraction des 48 projets 

a	Script utilisé :
https://github.com/ilyesox/ProjetETSIlyes/blob/39069ac32a741de33fa3f74ab98dc999d1202913/projectsextraction.py

b.	Liste des 48 projets extraits 
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Projects%20collected/Projects%20collected

2.	L’Extraction des Versions des Fournisseurs depuis le Registre Terraform
Le script 
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Providers%20versions%20extraction.py
Le script précèdent va dans le projet ( fichier csv d’un certain projet donné) a la colonne sourcename et cherche le nom du provider dans terraform registry et quand il le trouve il ramène toutes les versions existantes de ce fournisseur voici un exemple : 
Exemple de résultat 
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Exemple%20des%20versions%20extraites%20de%20azurerm

3.	Classement des fournisseurs par utilisation :
Pour savoir quel sont les fournisseurs les plus utilisés dans notre étude on a développé un script qui extrait les données à partir d’un autres fichier Excel qu’on va en parler juste après.
Le script :
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/upgrades%2C%20downgrades%20and%20changes%20per%20project%20(sorted).py
Le résultat :
 https://docs.google.com/spreadsheets/d/1iYwQvXbnBD-K9-J8ohjZuz8hnFLn3t3C/edit?usp=sharing&ouid=105140662728749325776&rtpof=true&sd=true

4.	Et maintenant voici le script pour extraire les données suivantes :
Project,	provider, upgrades, downgrades, total upgrades in the project, total downgrades in the project, total changes in the project, total upgrades of the provider across all projects, total downgrades of the provider across all projects, total changes of the provider across all projects.
Script 
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/project_provider_upgrades_downgrades%20results%20per%20provider.py
Résultat
https://docs.google.com/spreadsheets/d/1-o-08g8sk-17w3aac9H_5V44rGq6MJfL/edit?usp=sharing&ouid=105140662728749325776&rtpof=true&sd=true

5.	Total des changements par projet
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Results/Total%20changes%20per%20project.png
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Results/Total%20downgrades%20per%20project.png
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Results/Total%20upgrades%20per%20project.png
Ces graphes ont été extraits à partir du fichier Excel qui contient le nombre de changements, upgrades et downgrades par projets « upgrades, downgrades and changes per project (sorted).xlsx » : 
https://docs.google.com/spreadsheets/d/1sCJ99WocGYTnxUsPQN2kjaD879bBI6Fx/edit?usp=sharing&ouid=105140662728749325776&rtpof=true&sd=true

Script 
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/upgrades%2C%20downgrades%20and%20changes%20per%20project%20(sorted).py
Résultat
https://docs.google.com/spreadsheets/d/1sCJ99WocGYTnxUsPQN2kjaD879bBI6Fx/edit?usp=sharing&ouid=105140662728749325776&rtpof=true&sd=true

6.	Et maintenant les statistiques des Changements de Versions
À partir du fichier « upgrades, downgrades and changes per project (sorted).xlsx » on a extrait ce graphe ainsi que le tableau de statistique
Résultat
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Results/boxplot%20changes%20with%20maxs.png
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Results/boxplot%20changes%20without%20maxs.png
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Results/tableau%20changes%20statistics.pdf
Script 
https://github.com/ilyesox/ProjetETSIlyes/blob/9c6b05738fcb04b4a1dbabb5f7dffbb025ee895c/Boxplot%20generation.py


7.	Technical Lag 
Avant d’avoir le graphe du Technical Lag 
a	On a extrait 48 fichiers contenant les données nécessaires pour voir le Technical Lag
Les voici
Résultat
https://drive.google.com/drive/folders/1KwSIhaxlAzwsA-mnpkpEscBjMEyaIsp1?usp=sharing

Script 

https://github.com/ilyesox/ProjetETSIlyes/blob/d1b00ff59ef30684b29b7d94a4e6acfe6cba47ca/script%20to%20exctract%20the%20files%20for%20technical%20lag.py

b	À partir des fichiers csv extrait à partir de tous les 48 projets on a réussi à avoir le graphe du Technical Lag 
Résultat 
https://github.com/ilyesox/ProjetETSIlyes/blob/d1b00ff59ef30684b29b7d94a4e6acfe6cba47ca/Results/technical%20lag%20graph.png
En utilisant ce script 
https://github.com/ilyesox/ProjetETSIlyes/blob/d1b00ff59ef30684b29b7d94a4e6acfe6cba47ca/technical%20lag%20script.py

Après ça, on a extrait les graphes Technical Lag de quelques fournisseurs 
Résultats 
https://github.com/ilyesox/ProjetETSIlyes/blob/d1b00ff59ef30684b29b7d94a4e6acfe6cba47ca/Results/technical%20lag%20of%20hashicorp%20aws.png
https://github.com/ilyesox/ProjetETSIlyes/blob/d1b00ff59ef30684b29b7d94a4e6acfe6cba47ca/Results/technical%20lag%20of%20hashicorp%20azurerm.png
https://github.com/ilyesox/ProjetETSIlyes/blob/d1b00ff59ef30684b29b7d94a4e6acfe6cba47ca/Results/technical%20lag%20of%20hashicorp%20google.png
https://github.com/ilyesox/ProjetETSIlyes/blob/d1b00ff59ef30684b29b7d94a4e6acfe6cba47ca/Results/technical%20lag%20of%20hashicorp%20helm.png
https://github.com/ilyesox/ProjetETSIlyes/blob/d1b00ff59ef30684b29b7d94a4e6acfe6cba47ca/Results/technical%20lag%20of%20hashicorp%20kubernetes.png

En utilisant ce script
https://github.com/ilyesox/ProjetETSIlyes/blob/d1b00ff59ef30684b29b7d94a4e6acfe6cba47ca/technical%20lag%20specified%20script.py
