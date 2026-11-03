# ShopFlow — Architecture Résiliente & Distribuée

Ce projet implémente une architecture microservices résiliente basée sur le cas d'usage **ShopFlow**, développée dans le cadre du module d'architecture logicielle. L'objectif est de démontrer la capacité du système à tolérer des pannes (latence, pannes de services tiers) de manière totalement transparente pour l'utilisateur final grâce à des patterns de résilience avancés.

---

## Architecture du Système

Le système est composé de 3 services communiquant en HTTP orchestrés via Docker :
1. **`app` (API Gateway / Orchestrateur - Port 8080)** : Reçoit les requêtes clientes, orchestre les appels vers les sous-services et intègre la logique de résilience (Timeout, Fallback, Cache).
2. **`stock-service` (Service Stock - Port 8082)** : Un service rapide et stable gérant l'inventaire des produits.
3. **`reco-service` (Service Recommandations - Port 8083)** : Un service instable / simulé (flaky) doté d'une API d'administration permettant d'injecter du chaos (latence, pannes).

---

## Patterns de Résilience Implémentés

* **Timeout** : Empêche un blocage indéfini des threads sur le service de recommandations ($0,5\text{s}$ max).
* **Retry** : Permet de retenter les appels en cas d'erreurs réseau transitoires.
* **Circuit Breaker** : Coupe l'accès au service de recommandations s'il enchaîne trop d'échecs, protégeant l'infrastructure.
* **Bulkhead / Cloisonnement** : Limite le nombre de requêtes simultanées pour éviter la saturation du système sous forte charge.
* **Fallback & Cache Résilient** : En cas de panne ou si le circuit est ouvert, le système renvoie la dernière valeur saine mémorisée dans un cache (`"degrade": True`).
* **Dégradation gracieuse** : L'application reste fonctionnelle et livre le stock même si les recommandations sont indisponibles (**0 erreur vue par l'utilisateur**).

---

## 🚀 Guide de Démarrage Rapide (Prérequis : Docker & Docker Compose)

L'intégralité de l'infrastructure se lance en une seule commande grâce à Docker Compose.

### 1. Cloner ou se placer dans le projet
Assure-toi d'être à la racine du dossier contenant le fichier `docker-compose.yml`.

### 2. Lancer les services
Exécute la commande suivante pour construire et démarrer les conteneurs en arrière-plan :

```bash
docker compose up --build -d

### 3. Tester l'application
Une fois les conteneurs démarrés, tu peux tester le bon fonctionnement de l'API en effectuant une requête HTTP (par exemple pour le produit `A1`) :

curl http://localhost:8080/page/A1

Simuler une panne (Chaos Engineering)


curl "http://localhost:8083/admin?down=1"

Pour rétablir le service par la suite :

curl "http://localhost:8083/admin?down=0"