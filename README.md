# TP1-CSC8613
HADDAOUI HANNA MAIA 

## Exercice 1: Installation de Docker et vérification de l’environnement 
a) ☑

b) Capture de la commande ps -a

<img width="570" height="114" alt="image" src="https://github.com/user-attachments/assets/5063ada3-cc5e-49be-9da2-329d62ff62a0" />


La commande docker ps -a afficher tous les conteneurs connus de Docker sur la machine, qu’ils soient en cours d’exécution ou déjà arrêtés. Chaque ligne du tableau correspond à un conteneur et donne son identifiant, l’image Docker utilisée, la commande qui a été lancée, la date de création, son état (si c'est actif ou terminé) et son nom. On y retrouve par exemple le conteneur hello-world, qui a été créé, exécuté une seule fois, puis est passé à l’état « Exited ».

## Exercice 2: Premiers pas avec Docker : images et conteneurs

a) Une image Docker est un modèle figé. L'image contient un système minimal (fichiers, dépendances, configuration) mais ne s’exécute pas en elle-même.
Un conteneur Docker est une instance en cours d’utilisation d’une image : c’est le “processus vivant” créé à partir de cette image, avec son propre système de fichiers et son état d’exécution. On peut lancer plusieurs conteneurs différents à partir d’une même image.

b)  <img width="1122" height="322" alt="image" src="https://github.com/user-attachments/assets/ffeb057e-dde0-488d-abe4-630e87748c90" />

La commande docker run alpine echo "Bonjour depuis un conteneur Alpine" télécharge l’image alpine si elle n’est pas présente, à partir de cette image il crée crée un conteneur, exécute la commande echo à l’intérieur, affiche le message dans la console, et il arrête immédiatement le conteneur une fois que la commande terminée.

c) 

<img width="714" height="403" alt="image" src="https://github.com/user-attachments/assets/5ffe0c5f-cde1-4bb9-8be0-42331d9d4141" />

Le conteneur basé sur l’image alpine apparaît avec l’état Exited car il a uniquement exécuté la commande echo puis s’est terminé. Dans Docker, un conteneur s’arrête dès que le processus principal associé a fini de s’exécuter comme ici avec la commande echo.


d) 

<img width="726" height="240" alt="image" src="https://github.com/user-attachments/assets/69fd2e37-86dd-44ca-985e-ab30906a99b6" />

Avec docker run -it alpine sh, je lance un conteneur Alpine en mode interactif et j’ouvre un shell sh à l’intérieur. La commande ls montre un système de fichiers minimal, propre à l’image Alpine. La commande uname -a confirme que le conteneur tourne sur un noyau Linux. Avec exit, je sors du shell et le conteneur s’arrête, je reviens au terminal de ma machine hôte.


## Exercice 3: Construire une première image Docker avec une mini-API FastAPI

Étape 1 — Compléter le fichier app.py

a) ☑

Étape 2 — Compléter le Dockerfile

b) ☑


Étape 3 — Construire l'image Docker
c) <img width="1498" height="898" alt="image" src="https://github.com/user-attachments/assets/dd1d7a15-b6b5-410a-8371-7de8bebbd3ee" />



## Exercice 4: Exécuter l’API FastAPI dans un conteneur Docker

Étape 1 — Lancer le conteneur
a) 

<img width="572" height="102" alt="Capture d’écran 2025-12-05 à 18 15 23" src="https://github.com/user-attachments/assets/d60a8b64-b239-4dbd-b6d7-439abff773f7" />

L’option -p 8000:8000 demande à Docker de faire un mapping de port entre le port 8000 du conteneur et le port 8000 de la machine hôte. C'est ce qui npous permet d'accéder à l’API qui tourne dans le conteneur via http://localhost:8000 sur ma machine.

Étape 2 — Tester l’endpoint /health
b) 

<img width="449" height="72" alt="image" src="https://github.com/user-attachments/assets/7b618d0a-ad67-40a4-8e60-2de9451123cc" />

<img width="534" height="92" alt="image" src="https://github.com/user-attachments/assets/8c8bd2c0-cde1-4a9a-9a13-18b11d6003b7" />



Étape 3 — Observer les conteneurs en cours d’exécution

c) 
<img width="1854" height="246" alt="image" src="https://github.com/user-attachments/assets/9f5c0b0c-ac24-4476-b552-d124a082a8dc" />

Le conteneur simple-api apparaît dans docker ps avec :
Image : simple-api
Nom : <nom généré par Docker>
Ports : 0.0.0.0:8000->8000/tcp, ce qui indique que le port 8000 du conteneur est exposé sur le port 8000 de la machine hôte.


Étape 4 — Arrêter le conteneur
d)
<img width="572" height="254" alt="Capture d’écran 2025-12-05 à 18 48 26" src="https://github.com/user-attachments/assets/fa4d5d2f-c229-4033-83f3-43d6683f3f23" />

La commande docker stop <id> arrête le conteneur en cours d’exécution.
docker ps affiche seulemment les conteneurs actuellement en cours d’exécution, et docker ps -a liste tous les conteneurs, et aussi ceux qui sont arrêtés (Exited).


## Exercice 5: Démarrer un mini-système multi-conteneurs avec Docker Compose

a) ☑

b) ☑

c)
<img width="1420" height="680" alt="image" src="https://github.com/user-attachments/assets/e908affe-900a-44ef-ae72-e46e895e6440" />

<img width="1438" height="424" alt="image" src="https://github.com/user-attachments/assets/b7b929dd-ef2f-4b71-9406-ce9bfbdaa76b" />

d)
<img width="1436" height="498" alt="image" src="https://github.com/user-attachments/assets/81ca17f8-9e2e-4173-98f1-0ed0ed62db69" />


e)☑
<img width="731" height="64" alt="image" src="https://github.com/user-attachments/assets/0976a4f0-5d78-4997-9c40-77ad76457421" />

La commande docker compose down arrête et supprime tous les conteneurs, le réseau et les ressources associées au fichier docker-compose.yml. docker stop <id> ne concerne qu’un seul conteneur. Il l’arrête, mais ne supprime pas sa définition et ne touche pas aux autres services du projet.

## Exercice 6:Interagir avec la base de données PostgreSQL dans un conteneur

a) La commande docker compose exec db psql -U demo -d demo permet d’ouvrir le client PostgreSQL psql à l’intérieur du conteneur associé au service db défini dans docker-compose.yml, et cela sans redémarrer le conteneur. On se connecte à la base de données demo en utilisant l’utilisateur PostgreSQL demo.

b)

<img width="1442" height="292" alt="image" src="https://github.com/user-attachments/assets/5ea8180c-6db6-430a-9222-4380253e7c84" />

Dans psql, la commande SELECT version(); affiche la version du serveur PostgreSQL (par exemple PostgreSQL 16.x).
La commande SELECT current_database(); renvoie demo, ce qui confirme que je suis bien connecté à la base configurée dans Docker Compose.

c) Dans le réseau Docker Compose, les services peuvent se joindre en utilisant le nom du service comme hostname.
Pour que l’API se connecte à PostgreSQL, elle utiliserait :
hostname : db (nom du service dans docker-compose.yml)
port : 5432
utilisateur : demo
mot de passe : demo
base : demo
Par exemple, une URL de connexion serait :
postgresql://demo:demo@db:5432/demo.


d)  docker compose down arrête les conteneurs et supprime les ressources du projet (conteneurs, réseau), mais conserve les volumes : les données restent sur le disque.
docker compose down -v fait la même chose, mais supprime aussi les volumes associés, donc les données stockées dans PostgreSQL sont définitivement effacées.

## Exercice 7: Déboguer des conteneurs Docker : commandes essentielles et bonnes pratiques
a)

<img width="721" height="132" alt="Capture d’écran 2025-12-08 à 15 09 37" src="https://github.com/user-attachments/assets/1a3bff28-a3c8-44bc-b754-be0ab54e7573" />
<img width="1438" height="360" alt="image" src="https://github.com/user-attachments/assets/d49b5242-8949-4138-b81b-281618c6229a" />


docker compose logs -f api permet de suivre en direct les logs du service api.
Au démarrage, on voit Uvicorn initialiser le serveur FastAPI (messages “Started server process”, “Uvicorn running on …”). Lorsqu’une requête est faite sur /health, une ligne de log supplémentaire apparaît avec la méthode GET /health et le code de réponse HTTP 200.

b)docker compose exec api sh ouvre un shell dans le conteneur du service api.
La commande ls montre le contenu du répertoire de travail /app (par exemple app.py).
python --version affiche la version de Python installée dans le conteneur (ici Python 3.11).
En tapant exit, on ferme le shell et on revient au terminal de la machine hôte.

c) docker compose restart api arrête puis relance uniquement le conteneur du service api, et ne touche pas à la base de données. C’est utile lorsqu’un seul service est bloqué (API qui plante ou mise à jour de configuration par exemple) mais que l’on souhaite garder les autres services (par exemple la bdd) en fonctionnement.

d) Après avoir volontairement renommé la variable app en appi dans app.py, le service api ne démarre plus. Avec docker compose logs -f api, on observe une trace d’erreur indiquant qu’Uvicorn ne trouve pas l’application app (app:app). En lisant le message d’erreur et en le reliant à la configuration de lancement (CMD ["uvicorn", "app:app", ...]), on identifie rapidement la cause : la variable FastAPI doit s’appeler app.

e) docker container prune supprime tous les conteneurs arrêtés. Cela évite d’accumuler des ressources inutiles.
docker image prune supprime les images Docker non utilisées (dangling, non référencées par des conteneurs), ce qui libère de l’espace disque. Nettoyer régulièrement son environnement Docker permet d’éviter que la machine ne soit saturée par des conteneurs et images obsolètes.

## Exercice 8: 

a) Un notebook Jupyter est très pratique pour l’exploration et les prototypes, mais il n’est pas adapté à un déploiement en production.
Tout d'abord, l’exécution n’est pas reproductible : on peut lancer les cellules dans n’importe quel ordre, garder de l’état caché en mémoire, et on ne sait pas exactement dans quelles conditions le modèle a été entraîné ou exécuté. Alors qu'avec Docker on fige un environnement précis (version de Python, bibliothèques, configuration) dans une image, ce qui garantit que le même code se comporte de la même façon sur n’importe quelle machine.
Ensuite, un notebook n’est pas fait pour être un service automatisé car il faut l’ouvrir à la main, lancer les cellules, et il n’expose pas naturellement une API stable. Dans le TP, on a au contraire emballé le modèle (ici une mini-API FastAPI) dans un conteneur qui démarre automatiquement avec docker run ou docker compose up et qui expose une route /health. C’est ce type d’architecture qui est attendu en production pour intégrer un modèle dans un système plus large.

b) Docker Compose devient essentiel dès qu’on manipule plusieurs services (API, base de données...). Il permet de décrire toute l’architecture applicative dans un seul fichier YAML (docker-compose.yml) : services, images, ports, variables d’environnement, dépendances…
Dans le TP, grâce à Docker Compose, on a pu lancer l’API FastAPI et la base PostgreSQL ensemble avec une seule commande docker compose up -d, au lieu de devoir écrire à la main plusieurs commandes docker run compliquées. Compose crée aussi automatiquement un réseau entre les services : l’API peut joindre la base via le hostname db, sans se soucier des adresses IP. 
Enfin, il simplifie la gestion et le débogage, docker compose logs, docker compose exec, docker compose restart api… tout est centralisé pour l’ensemble de la stack.
