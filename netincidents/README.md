# 🌐 NetIncidents — Application de Gestion d'Incidents Réseaux

Application web Django professionnelle pour la gestion complète des incidents réseaux.

---

## 🚀 Installation rapide (VS Code)

### 1. Prérequis
- Python 3.10+
- pip

### 2. Installation des dépendances

```bash
cd netincidents

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Initialisation de la base de données

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Charger les données de démonstration

```bash
python manage.py seed_demo_data
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

Accéder à l'application : **http://127.0.0.1:8000**

---

## 👤 Comptes de connexion

| Utilisateur    | Mot de passe | Rôle              |
|----------------|--------------|-------------------|
| `admin`        | `admin123`   | Administrateur    |
| `technicien1`  | `tech123`    | Technicien réseau |
| `technicien2`  | `tech456`    | Technicien réseau |
| `superviseur`  | `sup123`     | Superviseur       |
| `utilisateur1` | `user123`    | Utilisateur       |

Interface d'administration Django : **http://127.0.0.1:8000/admin/**

---

## 📦 Structure du projet

```
netincidents/
├── manage.py
├── requirements.txt
├── demo_data.py             ← Données de démo
├── netincidents/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── incidents/
    ├── models.py            ← Modèles de données
    ├── views.py             ← Logique métier
    ├── urls.py              ← Routage URL
    ├── forms.py             ← Formulaires
    ├── admin.py             ← Interface admin
    ├── utils.py             ← Génération PDF
    ├── apps.py
    └── templates/incidents/
        ├── base.html        ← Layout principal (sidebar)
        ├── login.html       ← Page de connexion
        ├── dashboard.html   ← Tableau de bord + graphiques
        ├── liste_incidents.html
        ├── detail_incident.html
        ├── form_incident.html
        ├── liste_equipements.html
        ├── form_equipement.html
        ├── rapports.html
        ├── historique.html
        ├── notifications.html
        ├── profil.html
        ├── confirmer_suppression.html
        └── confirmer_suppression_eq.html
```

---

## ✨ Fonctionnalités

### Gestion des incidents
- ✅ Création, modification, suppression d'incidents
- ✅ Catégories : panne réseau, sécurité, lenteur, configuration, etc.
- ✅ Priorités : Critique / Haute / Moyenne / Basse
- ✅ Statuts : Ouvert → En cours → Résolu → Fermé
- ✅ Assignation à un technicien
- ✅ Lien avec les équipements concernés
- ✅ Champ impact métier, cause racine, solution appliquée
- ✅ Changement de statut rapide (clic ou AJAX)

### Journal d'activité
- ✅ Commentaires par type (commentaire, action, escalade, mise à jour)
- ✅ Timeline visuelle par incident
- ✅ Historique global de tous les changements de statut

### Équipements réseau
- ✅ CRUD complet : routeur, switch, firewall, serveur, Wi-Fi, WAN
- ✅ Adresse IP, localisation, statut
- ✅ Lien vers les incidents associés

### Rapports PDF
- ✅ Rapport par incident (fiche détaillée)
- ✅ Rapport global filtrable (statut, priorité, dates)
- ✅ Export PDF professionnel avec ReportLab
- ✅ Statistiques récapitulatives dans le rapport

### Dashboard
- ✅ KPIs temps réel (total, ouverts, en cours, résolus, critiques)
- ✅ Alerte incidents critiques
- ✅ Graphiques Chart.js : statuts, priorités, tendance semaine
- ✅ Tableau des derniers incidents
- ✅ Mes incidents assignés
- ✅ Jeu de données de démonstration multi-rôles pour alimenter le dashboard

### Autres
- ✅ Système de notifications internes
- ✅ Profil utilisateur avec avatar
- ✅ Pagination sur toutes les listes
- ✅ Filtres et recherche avancés
- ✅ Tri des colonnes
- ✅ Connexion classique Django et connexion rapide de démonstration
- ✅ Mode sombre / clair (toggle)
- ✅ Design responsive (mobile-friendly)
- ✅ Interface admin Django complète

---

## 🛠️ Dépannage

**Erreur "No module named 'reportlab'"** :
```bash
pip install reportlab
```
Sans ReportLab, les rapports seront générés en `.txt` (fallback automatique).

**Réinitialiser la base de données** :
```bash
del db.sqlite3          # Windows
rm db.sqlite3           # Linux/Mac
python manage.py migrate
python manage.py seed_demo_data
```
1. Créer l’incident avec utilisateur1

Connectez-vous avec utilisateur1 / user123.
Dans le menu de gauche, cliquez sur Nouvel incident.
Remplissez au minimum :
Titre
Description
Catégorie
Priorité
Vous pouvez aussi choisir un ou plusieurs équipements si besoin.
Cliquez sur Créer.
Résultat attendu :

l’incident est créé
il est en statut Ouvert
il est automatiquement adressé à un administrateur
2. Assigner l’incident à technicien1 avec admin

Déconnectez-vous.
Connectez-vous avec admin / admin123.
Dans le menu, cliquez sur Incidents.
Ouvrez l’incident créé à l’étape 1.
Cliquez sur Modifier.
Dans le champ Assigné à, choisissez technicien1.
Vérifiez les autres informations si besoin.
Cliquez sur Enregistrer.
Résultat attendu :

l’incident est maintenant affecté à technicien1
technicien1 pourra le voir dans ses incidents
3. Prendre en charge l’incident avec technicien1

Déconnectez-vous.
Connectez-vous avec technicien1 / tech123.
Dans le menu, cliquez sur Incidents.
Ouvrez l’incident qui vous a été assigné.
Cliquez sur Modifier.
Dans le champ Statut, choisissez En cours.
Cliquez sur Enregistrer.
Résultat attendu :

l’incident passe en En cours
cela signifie que le technicien a commencé le traitement
4. Résoudre l’incident avec technicien1

Toujours connecté avec technicien1, ouvrez à nouveau l’incident.
Cliquez sur Modifier.
Remplissez le champ Solution appliquée.
Exemple : Redémarrage du service et correction de la configuration.
Dans le champ Statut, choisissez Résolu.
Cliquez sur Enregistrer.
Résultat attendu :

l’incident passe en Résolu
la date de résolution est enregistrée
sans Solution appliquée, la résolution est refusée
5. Clore l’incident avec technicien1

Toujours sur le même incident, cliquez encore sur Modifier.
Vérifiez que Solution appliquée est toujours renseignée.
Dans le champ Statut, choisissez Fermé.
Cliquez sur Enregistrer.
Résultat attendu :

l’incident passe en Fermé
la date de fermeture est enregistrée
le cycle de vie du ticket est terminé
Résumé très simple
_________________________________________

voici ce que chaque rôle ne peut pas faire dans l’application actuelle.

Utilisateur
L’utilisateur simple ne peut pas :

assigner un incident à un technicien
choisir librement le cycle de traitement
passer un incident en En cours, Résolu ou Fermé
modifier un incident une fois qu’il n’est plus Ouvert
supprimer un incident
traiter les incidents des autres utilisateurs
En pratique :

il crée son ticket
il suit son évolution
il peut seulement modifier son propre ticket tant qu’il est encore Ouvert
Admin
L’administrateur ne peut pas :

assigner un incident à un utilisateur qui n’a pas le rôle technicien
mettre un incident sur un statut incohérent s’il n’y a pas de technicien assigné
En pratique :

il voit tout
il qualifie
il adresse au technicien
il pilote la circulation du ticket
c’est aussi le seul qui peut supprimer un incident
Technicien
Le technicien ne peut pas :

voir tous les incidents, seulement ceux qui lui sont assignés
modifier un incident qui n’est pas affecté à lui
assigner un incident à quelqu’un d’autre
remettre un incident en Ouvert
traiter un incident avec un statut hors de En cours, Résolu, Fermé
résoudre ou clôturer un incident si Solution appliquée est vide
supprimer un incident
En pratique :

il exécute le traitement technique sur ses tickets
il ne fait pas l’aiguillage initial
Superviseur
Le superviseur ne peut pas :

supprimer un incident
agir comme un admin pour l’assignation complète à un technicien, sauf selon les écrans/visibilités déjà autorisés par les règles métier
traiter librement tous les incidents comme un admin
En pratique :

il a une visibilité intermédiaire
il peut suivre et créer
mais il n’a pas les droits de suppression admin ni les droits de traitement technicien sur des tickets non assignés
Très important
Dans votre logique actuelle :

seul admin peut supprimer
seul le technicien assigné peut vraiment faire avancer vers En cours, Résolu, Fermé
l’utilisateur reste surtout déclarant/suiveur