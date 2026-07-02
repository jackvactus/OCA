#!/usr/bin/env python3
"""Add French accents to modules.json and questions.json."""
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")

REPLACEMENTS = [
    ("donnees", "données"), ("Donnees", "Données"), ("donnee", "donnée"),
    ("integrite", "intégrité"), ("Integrite", "Intégrité"),
    ("etrangeres", "étrangères"), ("Etrangeres", "Étrangères"), ("etrangere", "étrangère"),
    ("entites", "entités"), ("Entites", "Entités"), ("entite", "entité"),
    ("cardinalites", "cardinalités"), ("Cardinalites", "Cardinalités"),
    ("modifie", "modifie"), ("structure", "structure"),
    (" gere ", " gère "), ("Gere ", "Gère "),
    ("controle", "contrôle"), ("Controle", "Contrôle"),
    ("memoire", "mémoire"), ("Memoire", "Mémoire"),
    ("metadonnees", "métadonnées"), ("Metadonnees", "Métadonnées"),
    ("numeriques", "numériques"), ("Numeriques", "Numériques"), ("numerique", "numérique"),
    ("conversion", "conversion"),
    ("chaine", "chaîne"), ("Chaines", "Chaînes"), ("chaines", "chaînes"),
    (" caracteres", " caractères"), (" caracter", " caractère"),
    ("requete", "requête"), ("Requete", "Requête"), ("requetes", "requêtes"), ("Requetes", "Requêtes"),
    ("operateurs", "opérateurs"), ("Operateurs", "Opérateurs"), ("operateur", "opérateur"),
    ("logiques", "logiques"), ("priorite", "priorité"),
    ("joker", "joker"), ("echappement", "échappement"),
    ("positionnement", "positionnement"),
    ("agregation", "agrégation"), ("Agregation", "Agrégation"), ("agregat", "agrégat"), ("agregee", "agrégée"),
    ("agregation", "agrégation"),
    ("partageant", "partageant"),
    ("filtrage", "filtrage"),
    ("syntaxe", "syntaxe"),
    ("preserve", "préserve"), ("Preserve", "Préserve"), ("preservation", "préservation"),
    ("obligatoires", "obligatoires"),
    ("imprevisible", "imprévisible"),
    ("sequentiellement", "séquentiellement"),
    ("equivalent", "équivalent"), ("equivalence", "équivalence"),
    ("ensemblistes", "ensemblistes"),
    ("elimine", "élimine"), ("Elimine", "Élimine"),
    ("concatene", "concatène"),
    ("fenetre", "fenêtre"), ("Fenetre", "Fenêtre"), ("fenetres", "fenêtres"),
    ("analytiques", "analytiques"),
    ("ex-aequo", "ex-aequo"),
    ("precedente", "précédente"), ("precedent", "précédent"),
    ("Manipulation", "Manipulation"),
    ("Definition", "Définition"), ("definition", "définition"),
    ("Securite", "Sécurité"), ("securite", "sécurité"),
    ("Pieges", "Pièges"), ("pieges", "pièges"), ("piege", "piège"),
    ("execution", "exécution"), ("Execution", "Exécution"),
    ("aleatoires", "aléatoires"), ("aleatoire", "aléatoire"),
    (" differencier ", " différencier "),
    ("Maitriser", "Maîtriser"), ("maitriser", "maîtriser"),
    ("Utiliser", "Utiliser"),
    ("Creer", "Créer"), ("creer", "créer"),
    ("Inserer", "Insérer"), ("inserer", "insérer"),
    ("modifier", "modifier"),
    ("Comprendre", "Comprendre"),
    ("Differencier", "Différencier"), ("differencier", "différencier"),
    ("Interroger", "Interroger"),
    ("Eviter", "Éviter"),
    ("categories", "catégories"), ("Categories", "Catégories"), ("categorie", "catégorie"),
    ("unicite", "unicité"), ("Unicite", "Unicité"),
    ("reference", "référence"), ("Reference", "Référence"),
    ("dependances", "dépendances"),
    ("Irreversible", "Irréversible"),
    ("delegation", "délégation"), ("delegues", "délégués"), ("deleguer", "déléguer"),
    ("administration", "administration"),
    ("base de donnees", "base de données"), ("Base de donnees", "Base de données"),
    ("Fondamentaux de la base de donnees relationnelle", "Fondamentaux de la base de données relationnelle"),
    ("d integrite", "d'intégrité"),
    ("Differencier", "Différencier"),
    ("evaluer", "évaluer"), ("Evaluer", "Évaluer"),
    ("expressions scalars", "expressions scalaires"),
    ("embauche", "embauche"),
    ("inferieur", "inférieur"), ("Inferieur", "Inférieur"), ("superieur", "supérieur"), ("Superieur", "Supérieur"),
    ("decrement", "décrément"),
    ("deja", "déjà"),
    ("egalement", "également"),
    ("specifie", "spécifié"), ("specifier", "spécifier"),
    ("verifie", "vérifie"), ("Verifie", "Vérifie"),
    ("acces", "accès"), ("Acces", "Accès"),
    ("numero", "numéro"), ("numeros", "numéros"),
    ("sequential", "séquentiel"),
    ("Empeche", "Empêche"), ("empeche", "empêche"),
    ("Contraintes", "Contraintes"),
    ("recupere", "récupère"),
    ("auto-numerotation", "auto-numérotation"),
    ("Synonyme", "Synonyme"),
    ("Privileg", "Privilég"), ("privileg", "privilég"),
    ("revoquer", "révoquer"), ("Revoquer", "Révoquer"),
    ("predefinis", "prédéfinis"),
    ("absence de valeur", "absence de valeur"),
    ("modernne", "moderne"),
    ("Parametres", "Paramètres"),
    ("Resultat", "Résultat"), ("resultat", "résultat"),
    ("Examen blanc", "Examen blanc"),
    ("preparation", "préparation"),
    ("pedagogiques", "pédagogiques"), ("pedagogique", "pédagogique"),
    ("Objectifs pedagogiques", "Objectifs pédagogiques"),
    ("explications", "explications"),
    ("Sections du module", "Sections du module"),
]

def fix_text(text):
    if not isinstance(text, str):
        return text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text

def fix_obj(obj):
    if isinstance(obj, dict):
        return {k: fix_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [fix_obj(i) for i in obj]
    if isinstance(obj, str):
        return fix_text(obj)
    return obj

for fname in ("modules.json", "questions.json"):
    path = os.path.join(DATA, fname)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data = fix_obj(data)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Fixed accents in {fname}")
