PROJET BOT DISCORD B2
Thème : Assistant Marvel Rivals & Gestionnaire de Commandes
Auteur : COSTE Ugo

DESCRIPTION
===========
Le bot propose un système de discussion interactif sur le jeu "Marvel Rivals", 
un historique des commandes persistant et des outils de modération.

FONCTIONNALITÉS TECHNIQUES 

=============================================
1. Historique des Commandes (Fait main)
   - Structure : Pile (Stack) basée sur une Liste Chaînée.
   - Fichier : structures.py (Classe HistoriquePile).
   - Fonctionnalité : Stocke les commandes, permet de voir la dernière ou tout l'historique.

2. Système de Discussion
   - Structure : Arbre n-aire.
   - Fichier : structures.py
   - Fonctionnalité : Scénario à embranchements multiples sur les rôles et héros de Marvel Rivals.
   - Algorithme : Recherche récursive pour la commande /speak_about.

3. Sauvegarde Persistante
   - Format : JSON (data.json).
   - Fonctionnement : Sauvegarde automatique à chaque commande et chargement au démarrage.
   - Conversion : Les Piles sont converties en listes pour le JSON, et reconstruites en Piles au chargement.

4. Fonctionnalités Bonus
   - Jeu de dé.
   - Suppression de messages.
   - Listing automatique des commandes.

INSTALLATION & LANCEMENT
========================
1. Prérequis :
   - Python
   - Modules requis : discord.py, python-dotenv

   Installation des modules :
   pip install discord.py python-dotenv

2. Configuration :
   Créez un fichier nommé ".env" à la racine du dossier et ajoutez votre token :
   DISCORD_TOKEN=votre_token_discord_ici

3. Démarrage :
   Ouvrez un terminal dans le dossier du projet et lancez :
   py bot.py

LISTE DES COMMANDES
===================

--- Discussion (Arbre) ---
/discussion   : Lance le questionnaire interactif sur Marvel Rivals.
/reset        : Réinitialise la discussion au début.
/speak_about  : Vérifie si un sujet (ex: "Hulk") existe dans l'arbre (Recherche récursive).

--- Historique (Pile) ---
/last_cmd     : Affiche la toute dernière commande envoyée.
/all_history  : Affiche l'historique complet de l'utilisateur.
/clear_history: Vide l'historique de l'utilisateur (et le fichier de sauvegarde).

--- Utilitaires & Bonus ---
/supp [nb]    : Supprime les [nb] derniers messages du salon (nécessite permissions).
/dès          : Lance un dé à 6 faces.
/commands     : Affiche la liste dynamique de toutes les commandes disponibles.

STRUCTURE DES FICHIERS
======================
- bot.py        : Cœur du bot, gestion des événements Discord et des commandes Slash.
- structures.py : Contient uniquement les classes algorithmiques (Noeud, Pile, Arbre).
- data.json     : Fichier généré automatiquement pour la sauvegarde des données.
- .env          : Fichier de configuration (non fourni, à créer).
