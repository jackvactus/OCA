# Formation Oracle Database SQL — Certification 1Z0-071

Site web pédagogique complet pour préparer la certification **Oracle Database SQL (1Z0-071)**. HTML5, CSS3 et JavaScript vanilla, sans framework ni backend.

## Démarrage rapide

### Option 1 : Serveur local (recommandé)

Les fichiers JSON sont chargés via `fetch()`. Un serveur HTTP local est nécessaire :

```bash
# Python 3
cd oracle-1z0-071-training
python -m http.server 8080

# Node.js (npx)
npx serve .

# Extension VS Code / Cursor : Live Server
# Clic droit sur index.html → "Open with Live Server"
```

Ouvrez : **http://localhost:8080**

### Option 2 : Ouverture directe

Ouvrir `index.html` dans le navigateur peut bloquer le chargement des JSON (politique CORS `file://`). Utilisez un serveur local.

## Structure du projet

```
oracle-1z0-071-training/
├── index.html              # SPA — point d'entrée
├── css/
│   ├── styles.css          # Styles principaux
│   └── responsive.css      # Media queries mobile-first
├── js/
│   ├── app.js              # Application principale, rendu des vues
│   ├── router.js           # Routage hash (#/modules, #/quiz...)
│   ├── quiz.js             # Module QCM interactif
│   ├── exam-simulator.js   # Simulateur 63 questions / 120 min
│   └── progress.js         # Gestion localStorage
├── data/
│   ├── modules.json        # 14 modules pédagogiques complets
│   └── questions.json      # 154 questions QCM type certification
├── assets/resources/
│   ├── hr_schema.sql       # Schéma HR simplifié
│   ├── hr_data.sql         # Données exemple
│   └── practice_queries.sql # 50 requêtes d'entraînement
├── scripts/
│   ├── generate_data.py    # Régénération des JSON
│   └── fix_accents.py      # Correction accents français
└── README.md
```

## Fonctionnalités

| Section | Description |
|---------|-------------|
| **Accueil** | Présentation certification, stats progression, accès modules |
| **Cours** | 14 modules, navigation latérale, accordéons, SQL coloré (highlight.js) |
| **QCM** | Questions par module, feedback immédiat, explications détaillées |
| **Examen** | 63 questions aléatoires, chronomètre 120 min, revue finale |
| **Progression** | Modules complétés, scores QCM, historique examens, temps d'étude |
| **Ressources** | Scripts SQL téléchargeables, fiches mémo, liens Oracle |
| **À propos** | FAQ, formulaire contact (stockage local) |

## Modules pédagogiques (14)

1. Fondamentaux BD relationnelle (ERD, DDL/DML/DCL/TCL)
2. SELECT et fonctions scalaires (DUAL, UPPER, SUBSTR, TO_CHAR, NVL, CASE)
3. Filtrage et tri (WHERE, BETWEEN, IN, LIKE, ORDER BY)
4. Agrégation (COUNT, GROUP BY, HAVING)
5. Jointures (INNER, OUTER, SELF, NON-EQUI, USING, NATURAL, Oracle +)
6. Sous-requêtes (corrélées, ANY/ALL, EXISTS, FROM)
7. Opérateurs ensemblistes (UNION, INTERSECT, MINUS)
8. Fonctions analytiques (OVER, ROW_NUMBER, RANK, LAG/LEAD)
9. DML (INSERT, UPDATE, DELETE, MERGE, FOR UPDATE)
10. DDL (CREATE/ALTER/DROP, TRUNCATE, FLASHBACK)
11. Vues, Séquences, Index, Synonymes
12. Dictionnaire de données (USER_*, ALL_*, DBA_*)
13. Sécurité DCL (GRANT, REVOKE, rôles)
14. Pièges examen (ordre exécution, NULL, ROWNUM vs ROW_NUMBER)

## Banque de questions

- **154 questions QCM** réparties sur les 14 modules (~11 par module)
- 4 options par question, index de bonne réponse, explication pédagogique
- Pool utilisé pour le quiz filtrable et le simulateur d'examen (63 questions tirées aléatoirement)

## Progression (localStorage)

Clé : `oracle_1z0_071_progress`

Données sauvegardées :
- Modules marqués comme complétés
- Scores et tentatives QCM par module
- Historique examens blancs (score, durée, réussite ≥ 63 %)
- Temps d'étude par module
- Messages formulaire contact

## Scripts SQL HR

1. Exécutez `hr_schema.sql` pour créer les tables
2. Exécutez `hr_data.sql` pour insérer les données
3. Utilisez `practice_queries.sql` pour vous entraîner

Environnement recommandé : [Oracle Live SQL](https://livesql.oracle.com/)

## Design et accessibilité

- Couleurs : primaire `#E74C3C`, secondaire `#2C3E50`, fond `#F8F9FA`
- Typographies : Inter/Roboto (titres), JetBrains Mono (code)
- Font Awesome 6, highlight.js (CDN)
- Responsive mobile-first, sémantique HTML5, ARIA, skip link, WCAG 2.1 AA visé

## Compatibilité

- Chrome, Firefox, Safari (versions récentes)
- ES6+ modules JavaScript
- Aucune dépendance npm requise

## Régénérer les données

```bash
python scripts/generate_data.py
python scripts/fix_accents.py
```

## Examen officiel 1Z0-071 — rappel

| Paramètre | Valeur |
|-----------|--------|
| Questions | ~63 |
| Durée | 120 minutes |
| Score de passage | ~63 % |
| Format | QCM, plusieurs réponses possibles selon version |

---

*Contenu pédagogique inspiré des objectifs Oracle University. Non affilié à Oracle Corporation.*
