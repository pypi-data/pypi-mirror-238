# Bibliothèque de Gestion des Tâches pour Python (to_do_list)

Ce projet est une bibliothèque Python conçue pour faciliter la gestion des tâches, des projets et des ressources dans le cadre de la planification des projets. La bibliothèque permet d'ajouter, de compléter, de supprimer et de lister des tâches facilement.

Nous sommes 4 à travailler sur une to-do list. Les membres sont :

- Rayann
- Armand
- Matthias
- Erwan

## Caractéristiques

- Ajout de nouvelles tâches avec un nom et une description.
- Marquage d'une tâche comme terminée.
- Suppression de tâches de la liste.
- Affichage de la liste des tâches en cours.

## Installation

Ce projet utilise [Poetry](https://python-poetry.org/) pour la gestion des dépendances. Assurez-vous de l'avoir installé sur votre système.

### Instruction 

verifier que poetry est bien installé avec la commande suivante : 

```bash
poetry install
```

```bash 
poetry --version
```

installer l'environnement virtuel avec les commandes suivante : 

Lancer Windows PowerShell en tant qu'administrateur et exécuter la commande suivante : 

```bash
set-executionpolicy unrestricted
```

Valider par « O » (le o de oui).

Dans le terminal de to_do_list, lancer la commande suivante : 

Pour activer l'environnement virtuel :
```bash
.\venv\Scripts\activate
```

Pour désactiver l'environnement virtuel :
```bash
.\venv\Scripts\deactivate
```

Lancer le projet avec la commande suivante : 

```bash
poetry run python -m to_do_list
```
Lancer la base de donées avec la commande suivante : 

```bash
python cli.py --initdb
```
Ajouter un utilisateur & mot de passe avec la commande suivante : 

```bash
python cli.py --adduser username password
```
Lancer la console cli : 

```bash
python cli.py
```

## Utilisation

Pour utiliser la bibliothèque, il suffit d'importer le module `to_do_list` et d'utiliser les fonctions suivantes :

- `add_task(name, description)`: Ajoute une nouvelle tâche à la liste.
- `complete_task(name)`: Marque une tâche comme terminée.
- `delete_task(name)`: Supprime une tâche de la liste.
- `list_tasks()`: Affiche la liste des tâches en cours.

