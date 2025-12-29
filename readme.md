# 🚦 Urban Flow - Système Intelligent de Gestion du Trafic Urbain

[![ENIM](https://img.shields.io/badge/ENIM-2025--2026-blue)](https://enim.ac.ma/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.3-blue)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-blue)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-Academic-green)](#)

> **Jumeau numérique intelligent pour l'optimisation du trafic urbain avec support V2I et gestion des véhicules d'urgence**

Projet de modélisation réalisé dans le cadre du cursus ISIP (Information Systems and Industrial Programming) à l'École Nationale Supérieure des Mines de Rabat (ENIM).

---

## 📋 Table des Matières

- [🎯 Vue d'ensemble](#-vue-densemble)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture](#️-architecture)
- [🚀 Installation](#-installation)
- [💻 Utilisation](#-utilisation)
- [📊 Résultats](#-résultats)
- [📚 Documentation](#-documentation)
- [👥 Équipe](#-équipe)
- [📄 Licence](#-licence)

---

## 🎯 Vue d'ensemble

**Urban Flow** est un système de jumeau numérique (digital twin) conçu pour optimiser la gestion du trafic urbain en temps réel. Le système combine plusieurs technologies avancées:

- 🧠 **Algorithme Max-Pressure** pour l'optimisation adaptative des feux tricolores
- 🚑 **Module V2I (Vehicle-to-Infrastructure)** pour la priorité des véhicules d'urgence
- 🛡️ **Système Fail-Safe** pour garantir la continuité de service
- 📊 **Dashboard temps réel** avec visualisation interactive
- 🗺️ **Carte Leaflet** pour le suivi en direct du trafic

### Objectifs du Projet

1. **Réduire les temps d'attente** aux intersections de 30-40%
2. **Optimiser le débit** avec une augmentation de 35-40%
3. **Réduire les émissions de CO2** de 15-20%
4. **Garantir la priorité** aux véhicules d'urgence (taux de succès > 98%)

---

## ✨ Fonctionnalités

### 🚦 Gestion Intelligente du Trafic

- ✅ **Algorithme Max-Pressure** adaptatif basé sur la pression des files d'attente
- ✅ **Optimisation dynamique** des cycles de feux en temps réel
- ✅ **Prédiction du trafic** avec historique et tendances
- ✅ **Mode Fail-Safe** automatique en cas de défaillance

### 🚑 Module V2I (Vehicle-to-Infrastructure)

- ✅ **Communication DSRC 5.9 GHz** (300m de portée)
- ✅ **3 niveaux de priorité** (P1 Critique, P2 Haute, P3 Standard)
- ✅ **Vagues vertes automatiques** pour véhicules d'urgence
- ✅ **Réduction de 68%** des temps d'intervention (P1)
- ✅ **Taux de succès 99.2%** pour les requêtes P1

### 📊 Dashboard & Visualisation

- ✅ **Carte interactive** Leaflet avec visualisation temps réel
- ✅ **Graphiques dynamiques** (Chart.js + Recharts)
- ✅ **Métriques en temps réel** (temps d'attente, débit, files, émissions)
- ✅ **Historique des simulations** avec export CSV/JSON
- ✅ **WebSocket** pour mises à jour en direct

### 🛡️ Fiabilité & Sécurité

- ✅ **Triple Modular Redundancy (TMR)** pour contrôleurs
- ✅ **Capteurs redondants** (boucles inductives + caméras)
- ✅ **Alimentation sécurisée** (primaire + UPS + générateur)
- ✅ **Détection automatique** des défaillances (< 100ms)
- ✅ **Dégradation progressive** entre 4 modes opératoires

---

## 🏗️ Architecture

### Stack Technique

#### Backend (Python + Flask)
```
Flask 3.0+          → Framework web
Flask-SocketIO      → Communication temps réel
SQLAlchemy 2.0+     → ORM base de données
PostgreSQL          → Base de données principale
NumPy + Pandas      → Calculs scientifiques
```

#### Frontend (React + TypeScript)
```
React 18.3          → Framework UI
TypeScript 5.5      → Typage statique
Vite 7.3            → Build tool rapide
React-Leaflet 4.2   → Cartes interactives
Chart.js 4.4        → Graphiques
Socket.io-client    → WebSocket
Zustand 4.4         → State management
TailwindCSS 3.4     → Styling
```

### Structure du Projet

```
Projet_Modelisation/
├── backend/                    # Backend Flask
│   ├── src/
│   │   ├── algorithms/         # Algorithmes de trafic
│   │   │   ├── max_pressure.py
│   │   │   ├── v2i_priority.py
│   │   │   ├── fail_safe.py
│   │   │   ├── traffic_predictor.py
│   │   │   └── optimization.py
│   │   ├── api/                # API REST
│   │   ├── models/             # Modèles SQLAlchemy
│   │   ├── simulation/         # Moteur de simulation
│   │   ├── websocket/          # Handlers WebSocket
│   │   └── app.py              # Point d'entrée
│   └── requirements.txt
│
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── components/         # Composants React
│   │   │   ├── Dashboard/      # Dashboard principal
│   │   │   ├── Map/            # Carte Leaflet
│   │   │   └── Layout/         # Layout général
│   │   ├── pages/              # Pages de l'app
│   │   ├── hooks/              # Custom hooks
│   │   ├── stores/             # Zustand stores
│   │   └── services/           # Services API
│   └── package.json
│
├── docs/                       # Documentation
│   ├── rapport/                # Sections du rapport
│   └── guides/                 # Guides utilisateur
│
├── data/                       # Données et résultats
│   └── results/                # Résultats de simulation
│
├── assets/                     # Assets statiques
│   └── graphiques/             # Graphiques générés
│
├── scripts/                    # Scripts utilitaires
│   ├── generate_results.py    # Génération résultats
│   └── v2i_demo.py            # Démo V2I
│
└── README.md                   # Ce fichier
```

---

## 🚀 Installation

### Prérequis

- **Python 3.11+**
- **Node.js 18+** et npm
- **PostgreSQL 14+** (ou SQLite pour dev)
- **Git**

### 1. Cloner le Repository

```bash
git clone https://github.com/Ziiiko10/Projet_Modelisation.git
cd Projet_Modelisation
```

### 2. Installation Backend

```bash
# Créer un environnement virtuel
cd backend
python -m venv venv

# Activer l'environnement
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
cp .env.example .env
# Éditer .env avec vos paramètres

# Initialiser la base de données
python init_postgresql.py
```

### 3. Installation Frontend

```bash
cd frontend
npm install
```

---

## 💻 Utilisation

### Démarrer le Backend

```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Mode développement
python src/app.py

# Ou avec Flask
flask run

# Ou en production avec Gunicorn
gunicorn --worker-class eventlet -w 1 wsgi:app
```

Le backend sera accessible sur: `http://localhost:5000`

### Démarrer le Frontend

```bash
cd frontend
npm run dev
```

Le frontend sera accessible sur: `http://localhost:5173`

### Accéder à l'Application

Ouvrir votre navigateur sur: **http://localhost:5173**

---

## 📊 Résultats

### Métriques de Performance

#### Trafic Normal (500 véh/h)

| Métrique | Feux Fixes | Urban Flow | Amélioration |
|----------|-----------|------------|--------------|
| **Temps d'attente moyen** | 45.2s | 28.4s | **-37.2%** ✅ |
| **Débit horaire** | 820 véh/h | 1145 véh/h | **+39.6%** ✅ |
| **Longueur file d'attente** | 8.3 véh | 4.6 véh | **-44.6%** ✅ |
| **Émissions CO2** | 156.2 kg | 128.7 kg | **-17.6%** ✅ |

#### Module V2I - Véhicules d'Urgence

| Véhicule | Sans V2I | Avec V2I | Réduction | Taux Succès |
|----------|----------|----------|-----------|-------------|
| **P1 (Critique)** | 38.5s | 12.3s | **-68.1%** | 99.2% ✅ |
| **P2 (Haute)** | 38.5s | 17.8s | **-53.8%** | 97.5% ✅ |

#### Haute Densité (1000 véh/h)

| Métrique | Feux Fixes | Urban Flow | Amélioration |
|----------|-----------|------------|--------------|
| **Temps d'attente** | 78.6s | 52.1s | **-33.7%** ✅ |
| **Débit horaire** | 685 véh/h | 920 véh/h | **+34.3%** ✅ |

**🎯 Tous les objectifs atteints et dépassés!**

### Graphiques

Les graphiques de résultats sont disponibles dans `/assets/graphiques/`:
- Comparaison des métriques
- Performance V2I
- Évolution temporelle
- Haute densité

---

## 📚 Documentation

### Documents du Rapport

Tous les documents sont dans `/docs/rapport/`:

1. **Section 3.2.3** - Intégration V2I + Fail-Safe (10 pages)
2. **Section 3.3.3** - Interface de Supervision V2I (8 pages)
3. **Section 3.4.2 & 3.4.3** - Métriques & Analyse (12 pages)

### Guides Utilisateur

Dans `/docs/guides/`:
- Guide de création des diagrammes
- Guide des mockups UI
- Guide complet des résultats

### API Documentation

#### Endpoints Principaux

**Simulation**
```
POST   /api/simulation/start     # Démarrer une simulation
POST   /api/simulation/stop      # Arrêter la simulation
GET    /api/simulation/status    # État de la simulation
```

**Métriques**
```
GET    /api/metrics              # Métriques temps réel
GET    /api/metrics/history      # Historique des métriques
```

**Scénarios**
```
GET    /api/scenarios            # Liste des scénarios
POST   /api/scenarios            # Créer un scénario
GET    /api/scenarios/:id        # Détails d'un scénario
```

**Véhicules**
```
GET    /api/vehicles             # Liste des véhicules
POST   /api/vehicles/priority    # Enregistrer véhicule prioritaire
```

### WebSocket Events

```javascript
// Connexion
socket.on('connect', () => {});

// Mises à jour simulation
socket.on('simulation_update', (data) => {});
socket.on('vehicle_update', (data) => {});
socket.on('metrics_update', (data) => {});
socket.on('traffic_light_update', (data) => {});

// V2I
socket.on('priority_granted', (data) => {});
socket.on('green_wave_activated', (data) => {});
```

---

## 🛠️ Scripts Utilitaires

### Génération des Résultats

```bash
cd scripts
python generate_results_and_plots.py
```

Génère:
- 4 graphiques PNG (300 DPI)
- Fichier CSV de résumé
- Fichier JSON complet

### Démo V2I/Fail-Safe

```bash
cd scripts
python v2i_failsafe_demo.py
```

Exécute 5 scénarios de démonstration:
1. Opération normale avec véhicule d'urgence
2. Résolution de conflits de priorité
3. Mode dégradé (défaillance capteur)
4. Mode sécurisé (défaillance critique)
5. Restauration progressive

---

## 👥 Équipe

**Projet Urban Flow - ENIM 2025-2026**

- **Anouar DAKH** - Chef d'équipe
- **Hamza AMEZZANE** - Développement backend
- **Oussama MAATAQUI** - Développement frontend
- **Abdellah MORJANI** - Algorithmes & optimisation
- **Zakaria BOUGUERGA** - Tests & validation
- **Abderahmane HEDDAS** - Documentation

**Encadrement:**
- **Mme. Maryam GALLAB** - Superviseur académique

---

## 🎓 Contexte Académique

**École:** École Nationale Supérieure des Mines de Rabat (ENIM)  
**Filière:** ISIP (Information Systems and Industrial Programming)  
**Niveau:** 1ère année  
**Année universitaire:** 2025-2026  
**Type de projet:** Projet de modélisation et simulation

---

## 📄 Licence

Ce projet est réalisé dans un cadre académique à l'ENIM.

© 2025 - Équipe Urban Flow - ENIM

---

## 🙏 Remerciements

- **ENIM** pour l'infrastructure et le support
- **Mme. Maryam GALLAB** pour l'encadrement
- **Équipe de développement** pour leur travail acharné
- **Communauté open source** pour les outils utilisés

---

## 📞 Contact

Pour toute question concernant ce projet:

- **Email:** [projet.urbanflow@enim.ac.ma](mailto:projet.urbanflow@enim.ac.ma)
- **GitHub:** [Ziiiko10/Projet_Modelisation](https://github.com/Ziiiko10/Projet_Modelisation)

---

<div align="center">

**⭐ Si ce projet vous intéresse, n'hésitez pas à lui donner une étoile! ⭐**

</div>
