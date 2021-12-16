# Twitch to the Moon
## MA-VI
#### Made by Florian Feuillade, Massimo De Santis et Cédric Campos Carvalho

### Description

Twitch to the Moon sert à visualiser les informations sur les statistiques des jeux diffusés sur le site [Twitch.tv](https://twitch.tv). Le site montre des chiffres et statistiques globales de la plateforme. L'objectif principal est de pouvoir comparer les jeux entre eux sur des chiffres présentés et choisis sur l'application.

### Installation

*Testé sous python: `3.9.7`*

Pour lancer le serveur il est conseillé de créer un environnement:
1. Se placer dans le dossier du projet `twitch-to-the-moon`.
2. Créer l'envrionnement *python*:
```
python -m venv venv
```
3. Activer l'environnement:
<p style="text-align: center;">Sous <i>Windows</i>:</p>

```
venv\Scripts\activate.bat
```

<p style="text-align: center;">Sous <i>Linux/MacOS</i>:</p>

```
source venv\bin\activate
```

4. Install the *python* modules:

```
pip install -r requirements.txt
```

5. Lancer le serveur python en exécutant le `main.py`:

```
python main.py
```

6. Se connecter sur l'adresse *localhost* : [http://127.0.0.1:8888](http://127.0.0.1:8888).

### Source

[Top games on Twitch 2016 - 2021 sur kaggle.com](https://www.kaggle.com/rankirsh/evolution-of-top-games-on-twitch)