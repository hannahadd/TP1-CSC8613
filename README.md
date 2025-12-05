# TP1-CSC8613

## Exercice 1: Installation de Docker et vérification de l’environnement 
a) Capture du hello world

<img width="1114" height="582" alt="image" src="https://github.com/user-attachments/assets/36b4aa75-5c8d-4724-91c8-3e3bdf7f64c7" />

b) Capture de la commande ps -a

<img width="570" height="114" alt="image" src="https://github.com/user-attachments/assets/5063ada3-cc5e-49be-9da2-329d62ff62a0" />


La commande docker ps -a permet d’afficher l’ensemble des conteneurs connus de Docker sur la machine, qu’ils soient actuellement en cours d’exécution ou déjà arrêtés. Chaque ligne du tableau correspond à un conteneur et présente son identifiant, l’image Docker utilisée, la commande qui a été lancée, la date de création, son état (actif ou terminé) ainsi que son nom. On y retrouve par exemple le conteneur hello-world, qui a été créé, exécuté une seule fois, puis est passé à l’état « Exited ».

## Exercice 2: Premiers pas avec Docker : images et conteneurs
a) Une image Docker est un modèle figé : elle contient un système minimal (fichiers, dépendances, configuration) mais ne s’exécute pas en elle-même.
Un conteneur Docker est une instance en cours d’utilisation d’une image : c’est le “processus vivant” créé à partir de cette image, avec son propre système de fichiers et son état d’exécution. On peut lancer plusieurs conteneurs différents à partir d’une même image.

b)  <img width="1122" height="322" alt="image" src="https://github.com/user-attachments/assets/ffeb057e-dde0-488d-abe4-630e87748c90" />
La commande docker run alpine echo "Bonjour depuis un conteneur Alpine" télécharge l’image alpine si elle n’est pas déjà présente, crée un conteneur à partir de cette image, exécute la commande echo à l’intérieur, affiche le message dans la console, puis arrête immédiatement le conteneur une fois la commande terminée.

c) <img width="714" height="403" alt="image" src="https://github.com/user-attachments/assets/5ffe0c5f-cde1-4bb9-8be0-42331d9d4141" />
Le conteneur basé sur l’image alpine apparaît avec l’état Exited car il a uniquement exécuté la commande echo puis s’est terminé. Dans Docker, un conteneur s’arrête dès que le processus principal associé (ici la commande echo) a fini de s’exécuter.


d) <img width="726" height="240" alt="image" src="https://github.com/user-attachments/assets/69fd2e37-86dd-44ca-985e-ab30906a99b6" />

Avec docker run -it alpine sh, je lance un conteneur Alpine en mode interactif et j’ouvre un shell sh à l’intérieur. La commande ls montre un système de fichiers minimal, propre à l’image Alpine. La commande uname -a confirme que le conteneur tourne sur un noyau Linux. Quand je tape exit, je sors du shell et le conteneur s’arrête : je reviens au terminal de ma machine hôte.


## Exercice 3: Construire une première image Docker avec une mini-API FastAPI

Étape 1 — Compléter le fichier app.py

a) <img width="1168" height="410" alt="image" src="https://github.com/user-attachments/assets/730aa584-510d-4b91-94ab-69feb6db9d9e" />


Étape 2 — Compléter le Dockerfile

b) <img width="1342" height="588" alt="image" src="https://github.com/user-attachments/assets/367afb87-7de9-47af-ab46-6e7932af43bf" />


Étape 3 — Construire l'image Docker
c)


## Exercice 4: Exécuter l’API FastAPI dans un conteneur Docker

Étape 1 — Lancer le conteneur
a)

Étape 2 — Tester l’endpoint /health
b)

Étape 3 — Observer les conteneurs en cours d’exécution
c)

Étape 4 — Arrêter le conteneur
d)

## Exercice 5: Démarrer un mini-système multi-conteneurs avec Docker Compose
a)
b)
c)
d)
e)

## Exercice 6:Interagir avec la base de données PostgreSQL dans un conteneur
a)
b)
c)
d)

## Exercice 7: Déboguer des conteneurs Docker : commandes essentielles et bonnes pratiques
a)
b)
c)
d)
e)

## Exercice 8: 

a)
b)
c)
d)
