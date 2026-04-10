# Portfolio

Ce dépôt contient mon portfolio personnel. Il me sert à présenter mon profil, mes compétences, mes expériences professionnelles et quelques projets.

Le site est développé avec Flask afin de générer dynamiquement le contenu à partir de fichiers JSON. Une route permet également d’exporter une version statique du site.

---

## Installation

Créer un environnement virtuel :

```sh
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Site accessible sur: http://127.0.0.1:5000

Utiliser l'endpoint: http://127.0.0.1:5000/export pour générer une version statique du site et ainsi un fichier index.html à la racine du projet.

Générer la structure du projet avec:

```sh
tree /F /A > structure.txt
```

Mettre en blanc les svg en editant les fichiers:
```sh
fill="white"
```

## Ressources

- Palette de couleurs : https://paletadecolores.online/fr/bleu/

- Icônes technologies (Devicon) : https://devicon.dev/

- Icônes SVG (LinkedIn et autres) : https://www.svgrepo.com/vectors/linkedin/

- Documentation Flask : https://flask.palletsprojects.com/

- Documentation HTML : https://developer.mozilla.org/fr/docs/Web/HTML

- Documentation CSS : https://developer.mozilla.org/fr/docs/Web/CSS

- Documentation JavaScript : https://developer.mozilla.org/fr/docs/Web/JavaScript

