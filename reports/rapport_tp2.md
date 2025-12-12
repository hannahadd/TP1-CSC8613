# TP2 CSC8613 - Ingestion mensuelle, validation et snapshots
HADDAOUI HANNA 

## Exercice 1:
a)

<img width="1192" height="230" alt="image" src="https://github.com/user-attachments/assets/9932e78d-8404-4ad4-8d54-66b90184dcd8" />

b)

<img width="1204" height="698" alt="image" src="https://github.com/user-attachments/assets/7ffa3884-230a-4172-8a9c-650460531c36" />


c)
(base) hanna@MacBook-Air-de-Hanna TP1-CSC8613 % ls data/seeds/month_000
labels.csv		subscriptions.csv	usage_agg_30d.csv
payments_agg_90d.csv	support_agg_90d.csv	users.csv

(base) hanna@MacBook-Air-de-Hanna TP1-CSC8613 % ls data/seeds/month_001
labels.csv		subscriptions.csv	usage_agg_30d.csv
payments_agg_90d.csv	support_agg_90d.csv	users.csv


## Exercice 2:

a) Le schéma relationnel du projet (tables users, subscriptions, usage_agg_30d, payments_agg_90d, support_agg_90d, labels) a été défini dans `db/init/001_schema.sql`. Ces scripts seront exécutés automatiquement à l’init de PostgreSQL.

b) Le fichier .env stocke les variables d’environnement sensibles (identifiants PostgreSQL). Docker Compose les injecte automatiquement dans les conteneurs, ce qui permet de séparer la configuration du code.

c)

<img width="1888" height="520" alt="image" src="https://github.com/user-attachments/assets/3950db90-5e83-448d-9294-dc8548d5687c" />


d)
streamflow=# \dt
               List of relations
 Schema |       Name       | Type  |   Owner    
--------+------------------+-------+------------
 public | labels           | table | streamflow
 public | payments_agg_90d | table | streamflow
 public | subscriptions    | table | streamflow
 public | support_agg_90d  | table | streamflow
 public | usage_agg_30d    | table | streamflow
 public | users            | table | streamflow
(6 rows)

La commande \dt confirme que les six tables définies dans 001_schema.sql ont bien été créées au démarrage du conteneur PostgreSQL. Voici le rôle de chacune :

users : contient les informations principales sur chaque utilisateur (profil, date d’inscription, caractéristiques démographiques).
subscriptions : regroupe les données liées aux abonnements : durée, options activées, type de contrat, facturation…
usage_agg_30d : stocke des métriques d’usage agrégées sur les 30 derniers jours (heures de visionnage, temps moyen de session, nombre d’appareils…).
payments_agg_90d : conserve les agrégats de paiement sur 90 jours, notamment le nombre d’échecs de prélèvement.
support_agg_90d : contient les interactions avec le support client (tickets, temps moyen de résolution) sur 90 jours.
labels : correspond à la table cible du modèle de churn, indiquant si un utilisateur a résilié (churn_label).

Ces six tables constituent la base de données "live" sur laquelle les futures ingestions mensuelles, validations et snapshots vont s’appuyer.

## Exercice 3:
a) Le conteneur prefect joue le rôle d’orchestrateur du pipeline d’ingestion. Il exécute les flows Prefect qui lisent les fichiers CSV, les chargent dans PostgreSQL, appliquent des validations de qualité (Great Expectations) et créent les snapshots. Cela permet de centraliser la logique d’ingestion et de la rejouer facilement dans un environnement contrôlé.

b) La fonction upsert_csv lit un fichier CSV avec pandas, fait quelques conversions de type (dates, booléens), puis charge les données dans une table temporaire dans PostgreSQL. Ensuite, elle insère les données de cette table temporaire vers la table cible avec une clause ON CONFLICT sur la clé primaire : si une ligne existe déjà, elle est mise à jour (SET col = EXCLUDED.col), sinon elle est insérée. On obtient ainsi un “upsert” idempotent : relancer le flow sur les mêmes fichiers ne crée pas de doublons, mais met simplement les données à jour.

c)
streamflow=# SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM subscriptions;

 count 
-------
  7043
(1 row)

 count 
-------
  7043
(1 row)

Après l’ingestion des données du mois month_000, la base de données contient 7 043 utilisateurs.
Le nombre d’entrées dans les tables users et subscriptions est identique (7 043), ce qui indique que chaque client dispose bien d’un abonnement associé à ce stade.

## Exercice 4:
a) La fonction validate_with_ge ajoute une étape de contrôle qualité dans le pipeline : elle lit une table depuis PostgreSQL, applique des règles (expectations) sur la structure (colonnes attendues) et sur la cohérence des valeurs. Si une règle échoue, une exception est levée et le flow Prefect s’arrête, ce qui évite de propager des données incorrectes vers les étapes suivantes (snapshots / entraînement).

Les bornes choisies (ex. watch_hours_30d >= 0, avg_session_mins_7d >= 0) vérifient des contraintes “physiques” : ces métriques agrégées ne peuvent pas être négatives. Ces règles permettent de détecter rapidement un export corrompu, une erreur de parsing (types) ou une transformation incorrecte, et donc de protéger le modèle contre des données impossibles qui dégraderaient l’entraînement ou provoqueraient des biais.

b) 
c)
Dans ce pipeline, une étape de validation des données est mise en place à l’aide de Great Expectations afin de garantir la cohérence et la qualité des données avant leur utilisation pour l’entraînement d’un modèle de machine learning.

gdf.expect_table_columns_to_match_set([
    "user_id",
    "watch_hours_30d",
    "avg_session_mins_7d",
    "unique_devices_30d",
    "skips_7d",
    "rebuffer_events_7d",
])

gdf.expect_column_values_to_be_between("watch_hours_30d", min_value=0)
gdf.expect_column_values_to_be_between("avg_session_mins_7d", min_value=0)

Justification des bornes choisies:
Les bornes définies correspondent à des contraintes logiques et métier sur les données d’usage.
Par exemple, le nombre d’heures de visionnage sur 30 jours (watch_hours_30d) ainsi que la durée moyenne d’une session (avg_session_mins_7d) ne peuvent pas être négatifs. Des valeurs inférieures à zéro indiqueraient nécessairement une erreur dans les données (export incorrect, problème de transformation ou corruption du fichier source).

Protection du modèle

Ces règles permettent :
1) d’exclure des valeurs impossibles ou incohérentes ;
2) de détecter rapidement des erreurs d’export ou de parsing des fichiers CSV ;
3) d’éviter la propagation de données erronées vers les étapes de snapshots ou d’entraînement.

En cas d’échec d’une expectation, le flow Prefect est interrompu, ce qui empêche l’entraînement d’un modèle sur des données invalides. Cela contribue à améliorer la robustesse du modèle, à limiter les biais induits par des données incorrectes et à garantir une meilleure reproductibilité du système de machine learning.

# Synthèse:
## Exercice 5:
a)
La fonction snapshot_month(as_of) fige l’état des tables “live” à une date de fin de mois as_of en copiant les données dans des tables *_snapshots. Le champ as_of permet de conserver l’historique mensuel et d’éviter d’écraser les états passés, grâce à une insertion idempotente (ON CONFLICT DO NOTHING).

b) 
(base) hanna@MacBook-Air-de-Hanna TP1-CSC8613 % docker compose exec -T postgres psql -U streamflow -d streamflow -c \  
"SELECT COUNT(*) FROM subscriptions_profile_snapshots WHERE as_of = '2024-01-31';"

docker compose exec -T postgres psql -U streamflow -d streamflow -c \
"SELECT COUNT(*) FROM subscriptions_profile_snapshots WHERE as_of = '2024-02-29';"

 count 
-------
  7043
(1 row)

 count 
-------
  7043
(1 row)

On obtient le même nombre de lignes (7043) pour les deux dates. Cela signifie que le snapshot mensuel enregistre un état “figé” des abonnements à chaque date as_of, et que le nombre d’utilisateurs présents dans subscriptions est resté stable entre month_000 et month_001 (ou qu’il n’y a pas eu de nouveaux abonnés dans ces données). Les snapshots restent distincts grâce à la clé primaire (user_id, as_of).

c)
schéma 
CSV (month_000 / month_001)
        |
        v
   Prefect Flow
        |
        |-- Upsert PostgreSQL (tables live)
        |-- Validation Great Expectations
        |-- Snapshots temporels (tables *_snapshots, as_of)
        |
        v
   Données prêtes pour l'entraînement ML

*Pourquoi ne pas entraîner un modèle directement sur les tables live ?*
Les tables live représentent l’état courant des données, susceptible d’évoluer à tout moment (nouveaux utilisateurs, mises à jour, corrections). Entraîner un modèle directement sur ces tables pose plusieurs problèmes majeurs :
d’une part, les données peuvent changer entre deux entraînements, ce qui rend les résultats non reproductibles ; d’autre part, cela introduit un risque de data leakage, car le modèle pourrait indirectement exploiter des informations futures par rapport à la période qu’il est censé prédire.
Travailler sur des données figées à un instant donné permet de maîtriser précisément le contexte temporel de l’entraînement et de garantir la cohérence des résultats.


*Pourquoi les snapshots sont essentiels (data leakage & reproductibilité) ?*
Les snapshots permettent de figer l’état des données à une date donnée (as_of). Chaque snapshot représente une photographie fidèle du système à la fin d’un mois, indépendamment des évolutions ultérieures.
Cela joue un rôle clé pour :
éviter la data leakage, en s’assurant que seules les données disponibles à la date considérée sont utilisées ;
garantir la reproductibilité temporelle, car un entraînement relancé plus tard sur le même snapshot produira les mêmes résultats ;
comparer des modèles entraînés sur différentes périodes (analyse de dérive, évolution du comportement des utilisateurs).
Les snapshots constituent donc une brique indispensable dans tout pipeline ML sérieux en production.

Réflexion personnelle
La partie la plus délicate de ce TP a été la mise en place correcte de l’ingestion avec upsert et snapshots, notamment la gestion des clés primaires composées (user_id, as_of) et la compréhension de l’impact temporel des données.
J’ai également rencontré des difficultés liées à l’exécution du flow Prefect dans le conteneur (chemins des fichiers, variables d’environnement), que j’ai corrigées en vérifiant précisément les volumes montés et les commandes exécutées dans Docker Compose.
Ce TP m’a permis de mieux comprendre les enjeux réels d’un pipeline de données en Machine Learning, au-delà du simple chargement de fichiers, en intégrant des notions fondamentales comme la validation des données, la traçabilité et la reproductibilité.

d) fait 
