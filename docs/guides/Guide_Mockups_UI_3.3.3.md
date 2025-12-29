# Guide de Création des Mockups UI pour Section 3.3.3

## Vue d'ensemble

Cette section nécessite des mockups (maquettes) de l'interface V2I pour illustrer visuellement le document Word. Ces mockups doivent montrer l'interface telle qu'elle apparaîtrait aux opérateurs du TMC.

---

## 🎨 Outils Recommandés

### Option 1: Figma (Recommandé - Gratuit)
- **Lien**: https://www.figma.com/
- **Avantages**: Professionnel, collaboration en temps réel, bibliothèques de composants
- **Niveau**: Facile à intermédiaire
- **Temps**: 2-3 heures pour tous les mockups

### Option 2: Balsamiq Wireframes
- **Lien**: https://balsamiq.com/wireframes/
- **Avantages**: Style "croquis" professionnel, rapide
- **Niveau**: Très facile
- **Temps**: 1-2 heures

### Option 3: Adobe XD
- **Lien**: https://www.adobe.com/products/xd.html
- **Avantages**: Puissant, prototypage interactif
- **Niveau**: Intermédiaire
- **Temps**: 3-4 heures

### Option 4: Pencil Project (Gratuit, Open Source)
- **Lien**: https://pencil.evolus.vn/
- **Avantages**: 100% gratuit, pas de compte requis
- **Niveau**: Facile
- **Temps**: 2 heures

---

## 📐 Mockups à Créer

### Mockup 1: Vue d'ensemble du Dashboard (PRIORITÉ HAUTE)

**Dimensions**: 1920x1080 pixels (Full HD)

**Éléments à inclure**:

#### En-tête (100px de hauteur)
```
┌─────────────────────────────────────────────────────────────┐
│ 🚨 Module V2I - Supervision Véhicules d'Urgence            │
│ Urban Flow - Centre de Gestion du Trafic          [⚙️] [👤]│
└─────────────────────────────────────────────────────────────┘
```

#### Zone principale (split 70/30)
```
┌──────────────────────────────┬─────────────────────┐
│                              │  REQUÊTES ACTIVES   │
│                              │  ┌─────────────┐    │
│      CARTE INTERACTIVE       │  │ 🚑 AMB_001  │    │
│      (React-Leaflet)         │  │ P1 - 12s    │    │
│                              │  └─────────────┘    │
│  • Véhicules d'urgence       │  ┌─────────────┐    │
│  • Feux tricolores           │  │ 🚒 FIRE_023 │    │
│  • Corridors verts           │  │ P2 - 45s    │    │
│  • Trajectoires prédites     │  └─────────────┘    │
│                              │                     │
└──────────────────────────────┴─────────────────────┘
```

#### Barre de métriques (150px de hauteur)
```
┌─────────────────────────────────────────────────────┐
│  📊 Requêtes: 3  |  ⏱️ Temps: 28s  |  ✓ Succès: 98%  │
│  ⚡ Latence: 45ms                                    │
└─────────────────────────────────────────────────────┘
```

**Couleurs à utiliser**:
- Background principal: #F5F7FA
- Bleu principal (infrastructure): #2E5C8A
- Rouge (P1 critique): #C41E3A
- Orange (P2 haute): #FF9800
- Jaune (P3 standard): #FFC107
- Vert (vague verte): #4CAF50

---

### Mockup 2: Carte Interactive avec Véhicules (PRIORITÉ HAUTE)

**Focus**: Zoom sur la carte montrant:

#### Éléments visuels:
1. **Base de carte**: Fond OpenStreetMap (peut être capturé depuis https://www.openstreetmap.org/)

2. **Véhicule d'urgence** (ambulance):
   - Icône: 🚑 (grande taille, 40x40px)
   - Halo pulsant rouge autour
   - Ligne pointillée bleue montrant trajectoire prédite

3. **Zone RSU** (Road-Side Unit):
   - Cercle translucide bleu de 300m de rayon
   - Bordure en pointillés

4. **Feux tricolores**:
   - Cercle vert (mode normal)
   - Cercle vert avec bordure bleue épaisse (mode priorité)
   - Position aux intersections

5. **Corridor vert**:
   - Ligne verte épaisse (8px) en pointillés
   - De la position actuelle du véhicule vers l'intersection

**Annotations à ajouter**:
- "Trajectoire prédite (Kalman)"
- "Zone de détection V2I (300m)"
- "Corridor de vague verte actif"

---

### Mockup 3: Panneau des Requêtes Actives (PRIORITÉ MOYENNE)

**Dimensions**: 400x600 pixels

**Structure**:
```
┌────────────────────────────────────┐
│ Requêtes Actives (3)               │
│ ┌────────────────────────────────┐ │
│ │ [Trier par: Priorité ▼]        │ │
│ │ [Filtrer: Toutes ▼]            │ │
│ └────────────────────────────────┘ │
│                                    │
│ ┌────────────────────────────────┐ │
│ │ 🚑  AMB_001              [⚠️]  │ │
│ │ P1 - CRITIQUE           ┌────┐ │ │
│ │ ⏱️ ETA: 12s             │ ✓  │ │ │
│ │ 📍 Distance: 150m       │ ⏸  │ │ │
│ │ 📊 Statut: Accordée     │ ✕  │ │ │
│ │ Reçu: 14:32:15         └────┘ │ │
│ └────────────────────────────────┘ │
│                                    │
│ ┌────────────────────────────────┐ │
│ │ 🚒  FIRE_023            [⚠️]  │ │
│ │ P2 - HAUTE              ┌────┐ │ │
│ │ ⏱️ ETA: 45s             │ ✓  │ │ │
│ │ 📍 Distance: 680m       │ ⏸  │ │ │
│ │ 📊 Statut: En attente   │ ✕  │ │ │
│ │ Reçu: 14:31:52         └────┘ │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
```

**Code couleur des cartes**:
- P1: Bordure rouge (#C41E3A), fond rose pâle (#FFE5E8)
- P2: Bordure orange (#FF9800), fond orange pâle (#FFF3E0)
- P3: Bordure jaune (#FFC107), fond jaune pâle (#FFFDE7)

**Boutons**:
- ✓ Forcer: Vert (#4CAF50)
- ⏸ Suspendre: Orange (#FF9800)
- ✕ Annuler: Rouge (#C41E3A)

---

### Mockup 4: Système d'Alertes (PRIORITÉ BASSE)

**Position**: Coin supérieur droit (overlay)

**Structure d'une alerte**:
```
┌─────────────────────────────────────────┐
│ 🚨 ALERTE CRITIQUE               [✕]   │
│ Échec d'activation vague verte AMB_003 │
│ 14:35:22                                │
└─────────────────────────────────────────┘
```

**3 types à montrer**:
1. **Critique** (bordure gauche rouge 4px)
2. **Avertissement** (bordure gauche orange 4px)
3. **Info** (bordure gauche bleu 4px)

---

### Mockup 5: Barre de Métriques Détaillée (PRIORITÉ MOYENNE)

**Layout**: 4 cartes en ligne

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 📊          │ ⏱️          │ ✓           │ ⚡          │
│ Requêtes    │ Temps Moyen │ Taux Succès │ Latence     │
│ Actives     │             │             │             │
│             │             │             │             │
│    3        │   28s       │   98%       │   45ms      │
│             │             │ ✅ Normal   │ ✅ Normal   │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**État normal** (fond gris clair #F5F5F5):
- Texte en bleu #2E5C8A

**État alerte** (fond rose #FFE5E8):
- Bordure rouge 2px
- Texte en rouge #C41E3A
- Icône ⚠️ en bas

---

## 🎨 Guide de Style Détaillé

### Typographie
```
Titres principaux: Arial Bold, 28px, #2E5C8A
Sous-titres: Arial Bold, 18px, #000000
Corps de texte: Arial Regular, 14px, #555555
Labels: Arial Regular, 12px, #666666
Petites annotations: Arial Regular, 11px, #999999
```

### Espacements
```
Padding des cartes: 15-20px
Gap entre éléments: 10-15px
Marges externes: 20px
Border radius: 8px (cartes), 4px (boutons)
```

### Ombres
```
Cartes: box-shadow: 0 2px 8px rgba(0,0,0,0.1)
Boutons hover: box-shadow: 0 4px 12px rgba(0,0,0,0.15)
Alertes: box-shadow: 0 4px 12px rgba(0,0,0,0.15)
```

### Icônes
- Utiliser des emojis Unicode pour prototypage rapide
- Alternative: Font Awesome (si disponible dans l'outil)

---

## 📝 Tutoriel Figma Étape par Étape

### Étape 1: Création du projet
1. Aller sur https://www.figma.com/
2. Créer un compte gratuit
3. Nouveau fichier: "Urban Flow - Interface V2I"
4. Frame: 1920x1080 (Desktop HD)

### Étape 2: Composants de base
1. Rectangle: Créer le background (#F5F7FA)
2. Rectangle arrondi (r=8): En-tête blanc
3. Texte: "Module V2I - Supervision..."
4. Répéter pour chaque section

### Étape 3: Carte interactive
1. Rectangle: Zone de carte (70% largeur)
2. Importer image: Capture OpenStreetMap
3. Cercle: Zone RSU (stroke bleu pointillé)
4. Texte emoji: 🚑 pour véhicule
5. Cercle autour véhicule (opacity 30%, stroke rouge)
6. Ligne: Trajectoire pointillée bleue

### Étape 4: Panneau requêtes
1. Rectangle: Container (400px largeur)
2. Components: Créer "Request Card"
3. Dupliquer pour chaque requête
4. Boutons: Rectangles arrondis avec texte

### Étape 5: Export
1. Sélectionner frame complète
2. Export settings: PNG, 2x (haute résolution)
3. Exporter: `mockup_v2i_dashboard.png`

---

## 📸 Captures d'Écran Alternatives

Si la création de mockups est trop complexe, vous pouvez:

### Option A: Utiliser le code React fourni
1. Installer le projet React (si disponible)
2. Lancer `npm start`
3. Prendre des captures d'écran de l'interface
4. Utiliser un outil comme Snagit ou Greenshot

### Option B: Mockups rapides avec PowerPoint
1. Utiliser des formes simples dans PowerPoint
2. Ajouter des icônes depuis Insert > Icons
3. Capturer comme image
4. Moins professionnel mais rapide (30 min)

---

## ✅ Checklist Finale

**Avant de finaliser:**
- [ ] Tous les mockups créés (5 au total)
- [ ] Résolution haute qualité (minimum 1920px largeur)
- [ ] Palette de couleurs respectée
- [ ] Textes lisibles (pas de texte < 11px)
- [ ] Icônes et emojis visibles
- [ ] Exportés en PNG (pas JPG pour éviter compression)
- [ ] Nommés correctement:
  - `mockup_1_dashboard_complet.png`
  - `mockup_2_carte_interactive.png`
  - `mockup_3_panneau_requetes.png`
  - `mockup_4_alertes.png`
  - `mockup_5_metriques.png`

---

## 💡 Astuces Pro

### Gagner du temps:
1. **Réutiliser des templates**: Figma a des templates de dashboards gratuits
2. **Copier-coller**: Dupliquer les éléments répétitifs (cartes de requêtes)
3. **Composants**: Créer des composants réutilisables (boutons, cartes)
4. **Plugins Figma utiles**:
   - Iconify (icônes gratuites)
   - Unsplash (images de cartes)
   - Content Reel (texte factice)

### Qualité professionnelle:
1. Aligner tous les éléments (utiliser grille 8px)
2. Espacements cohérents partout
3. Ombres subtiles (pas trop prononcées)
4. Contraste suffisant pour textes (WCAG AA minimum)

---

## 📚 Ressources Supplémentaires

### Exemples de dashboards similaires:
- Google Maps (pour carte interactive)
- Waze Live Map (pour trafic en temps réel)
- FlightRadar24 (pour tracking de véhicules)

### Bibliothèques d'icônes:
- https://fontawesome.com/icons
- https://fonts.google.com/icons
- https://iconmonstr.com/

### Palettes de couleurs:
- https://coolors.co/
- https://colorhunt.co/

---

## ⏱️ Planning Suggéré

**Session 1 (1h30)**: Mockup 1 et 2
- Dashboard complet
- Carte interactive

**Session 2 (1h)**: Mockup 3 et 4
- Panneau des requêtes
- Système d'alertes

**Session 3 (30min)**: Mockup 5 + finitions
- Barre de métriques
- Ajustements et export

**TOTAL: 3 heures**

---

## 🎯 Critères d'Évaluation

Les mockups seront jugés sur:
1. **Clarté visuelle** (30%): Éléments bien visibles et organisés
2. **Cohérence** (25%): Respect de la palette de couleurs et du style
3. **Professionnalisme** (25%): Aspect soigné, pas "fait maison"
4. **Complétude** (20%): Tous les éléments décrits sont présents

**Note cible avec ces mockups: 17-20/20**

Bon courage! 🚀
