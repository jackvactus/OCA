#!/usr/bin/env python3
"""Generate modules.json and questions.json for Oracle 1Z0-071 training site."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")

MODULES = [
    {
        "id": 1,
        "title": "Fondamentaux de la base de donnees relationnelle",
        "summary": "Modele relationnel, ERD, categories SQL DDL/DML/DCL/TCL et architecture Oracle.",
        "objectives": [
            "Comprendre le modele relationnel et les contraintes d integrite",
            "Differencier DDL, DML, DCL et TCL",
            "Identifier les composants d une instance Oracle"
        ],
        "sections": [
            {
                "title": "Modele relationnel et ERD",
                "content": "Une base relationnelle organise les donnees en tables (relations). Chaque table possede des colonnes (attributs) et des lignes (tuples).\nLes cles primaires identifient uniquement chaque ligne. Les cles etrangeres etablissent les relations entre tables.\nUn diagramme ERD (Entity-Relationship Diagram) represente visuellement entites, attributs et cardinalites (1:1, 1:N, N:N).",
                "code": "-- Exemple : relation DEPARTMENTS -> EMPLOYEES (1:N)\nSELECT d.department_name, e.last_name\nFROM   departments d\nJOIN   employees e ON d.department_id = e.department_id;",
                "result": "DEPARTMENT_NAME  LAST_NAME\nExecutive        King\nExecutive        Kochhar\n...",
                "pitfalls": ["Confondre cle primaire et cle candidate", "Oublier que NULL n est pas une valeur comparable"]
            },
            {
                "title": "Categories de commandes SQL",
                "content": "DDL (Data Definition Language) : CREATE, ALTER, DROP, TRUNCATE, RENAME - modifie la structure.\nDML (Data Manipulation Language) : SELECT, INSERT, UPDATE, DELETE, MERGE - manipule les donnees.\nDCL (Data Control Language) : GRANT, REVOKE - gere les privileges.\nTCL (Transaction Control Language) : COMMIT, ROLLBACK, SAVEPOINT - controle les transactions.",
                "code": "CREATE TABLE demo (id NUMBER PRIMARY KEY, nom VARCHAR2(50));\nINSERT INTO demo VALUES (1, 'Test');\nCOMMIT;",
                "result": "Table created.\n1 row inserted.\nCommit complete.",
                "pitfalls": ["TRUNCATE est DDL (COMMIT implicite), DELETE est DML", "SELECT est considere comme DML a l examen Oracle"]
            },
            {
                "title": "Architecture Oracle simplifiee",
                "content": "Instance Oracle = SGA (memoire partagee) + processus background (DBWn, LGWR, PMON...).\nLa base de donnees = fichiers physiques (datafiles, redo logs, control files).\nChaque session utilisateur a une PGA (Program Global Area).\nLe dictionnaire de donnees stocke les metadonnees dans des vues USER_*, ALL_*, DBA_*.",
                "code": "SELECT instance_name, host_name, version\nFROM   v$instance;",
                "result": "INSTANCE_NAME  HOST_NAME  VERSION\nORCL           srv01      19.0.0.0.0",
                "pitfalls": ["v$instance necessite privileges systeme - USER_* suffit pour l examen SQL"]
            }
        ]
    },
    {
        "id": 2,
        "title": "SELECT et fonctions scalaires",
        "summary": "Requetes SELECT, table DUAL, fonctions caractere, numeriques, date et conversion.",
        "objectives": [
            "Construire des requetes SELECT avec alias et concatenation",
            "Utiliser les fonctions UPPER, SUBSTR, TO_CHAR, NVL, CASE",
            "Comprendre le role de la table DUAL"
        ],
        "sections": [
            {
                "title": "Syntaxe SELECT de base",
                "content": "SELECT column_list FROM table [WHERE condition] [ORDER BY columns].\nDISTINCT elimine les doublons. Les alias de colonnes utilisent AS ou un espace.\nEn Oracle, la concatenation se fait avec || (pas CONCAT pour plusieurs arguments).",
                "code": "SELECT employee_id AS id,\n       last_name || ', ' || first_name AS nom_complet,\n       salary * 12 AS salaire_annuel\nFROM   employees\nWHERE  department_id = 50;",
                "result": "ID   NOM_COMPLET      SALAIRE_ANNUEL\n200  Whalen, Jennifer  252000",
                "pitfalls": ["DISTINCT s applique a toute la combinaison de colonnes", "Les alias ne sont pas utilisables dans WHERE"]
            },
            {
                "title": "Table DUAL",
                "content": "DUAL est une table Oracle a une seule ligne et une colonne (DUMMY), creee par Oracle.\nElle sert a evaluer des expressions, fonctions ou sequences sans acceder a une vraie table.",
                "code": "SELECT SYSDATE FROM dual;\nSELECT UPPER('oracle sql') FROM dual;\nSELECT 1+1 AS resultat FROM dual;",
                "result": "SYSDATE\n29-JUN-26\n\nORACLE SQL\n\nRESULTAT\n2",
                "pitfalls": ["DUAL existe uniquement en Oracle", "Ne pas oublier FROM dual pour les expressions scalars"]
            },
            {
                "title": "Fonctions caractere et conversion",
                "content": "UPPER/LOWER/INITCAP transforment la casse. SUBSTR(chaine, debut, longueur) extrait.\nINSTR trouve une sous-chaine. LENGTH compte les caracteres.\nTO_CHAR convertit date/nombre en texte. TO_DATE convertit texte en date.\nNVL(expr1, expr2) remplace NULL par expr2. CASE WHEN ... END remplace DECODE.",
                "code": "SELECT last_name,\n       UPPER(last_name) AS maj,\n       SUBSTR(last_name, 1, 3) AS prefixe,\n       TO_CHAR(hire_date, 'DD-MON-YYYY') AS embauche,\n       NVL(commission_pct, 0) AS comm\nFROM   employees\nWHERE  ROWNUM <= 3;",
                "result": "LAST_NAME  MAJ     PREFIXE  EMBAUCHE     COMM\nKing       KING    Kin      17-JUN-2003  0\nKochhar    KOCHHAR Koc      21-SEP-2005  0",
                "pitfalls": ["SUBSTR commence a 1 en Oracle (pas 0)", "TO_DATE sans format = erreur ou resultat imprevisible"]
            },
            {
                "title": "CASE et DECODE",
                "content": "CASE evalue des conditions sequentiellement. DECODE est une alternative Oracle limitee a l egalite.\nNVL2(expr1, expr2, expr3) : si expr1 non NULL retourne expr2 sinon expr3.\nNULLIF(a, b) retourne NULL si a = b.",
                "code": "SELECT last_name, salary,\n       CASE WHEN salary >= 10000 THEN 'Eleve'\n            WHEN salary >= 5000  THEN 'Moyen'\n            ELSE 'Standard'\n       END AS categorie\nFROM   employees\nWHERE  ROWNUM <= 5;",
                "result": "LAST_NAME  SALARY  CATEGORIE\nKing       24000   Eleve\nKochhar    17000   Eleve",
                "pitfalls": ["CASE sans ELSE retourne NULL pour les non-correspondances", "DECODE compare uniquement par egalite"]
            }
        ]
    }
]

# Additional modules 3-14 will be appended by the script continuation
# For brevity in generation, we use a function to build remaining modules

def build_remaining_modules():
    mods = []
    mod3 = {
        "id": 3, "title": "Filtrage et tri",
        "summary": "Clauses WHERE, operateurs de comparaison, BETWEEN, IN, LIKE, IS NULL et ORDER BY.",
        "objectives": ["Filtrer avec WHERE et operateurs logiques", "Utiliser BETWEEN, IN, LIKE correctement", "Trier avec ORDER BY ASC/DESC NULLS FIRST/LAST"],
        "sections": [
            {"title": "Operateurs de comparaison", "content": "WHERE filtre les lignes avant projection.\nOperateurs : =, !=, <>, <, >, <=, >=. AND, OR, NOT combinent les conditions.\nLes parentheses controlent la priorite.", "code": "SELECT last_name, salary\nFROM   employees\nWHERE  salary BETWEEN 5000 AND 10000\n  AND  department_id IN (50, 60, 80)\n  AND  last_name NOT LIKE 'K%';", "result": "LAST_NAME  SALARY\nBaer       10000\n...", "pitfalls": ["BETWEEN inclut les bornes", "!= et <> sont equivalents en Oracle"]},
            {"title": "LIKE et caracteres joker", "content": "% represente zero ou plusieurs caracteres. _ represente exactement un caractere.\nESCAPE definit un caractere d echappement pour % et _ litteraux.", "code": "SELECT last_name FROM employees\nWHERE  last_name LIKE '_a%' ESCAPE '\\';", "result": "LAST_name\nGrant\n...", "pitfalls": ["LIKE est sensible a la casse selon NLS_SORT", "NULL LIKE '%' retourne NULL (pas TRUE)"]},
            {"title": "ORDER BY et NULLS", "content": "ORDER BY trie le resultat final. ASC (defaut) ou DESC.\nNULLS FIRST et NULLS LAST controlent le positionnement des NULL (comportement par defaut depend de ASC/DESC).", "code": "SELECT last_name, salary, commission_pct\nFROM   employees\nORDER BY commission_pct DESC NULLS LAST, salary ASC;", "result": "Tri par commission decroissante, NULL en dernier", "pitfalls": ["ORDER BY s execute apres SELECT - alias utilisables", "ROWNUM filtre AVANT ORDER BY sans sous-requete"]}
        ]
    }
    mod4 = {
        "id": 4, "title": "Agregation",
        "summary": "Fonctions COUNT, SUM, AVG, MIN, MAX, GROUP BY et HAVING.",
        "objectives": ["Appliquer les fonctions d agregation", "Grouper avec GROUP BY", "Filtrer les groupes avec HAVING"],
        "sections": [
            {"title": "Fonctions d agregation", "content": "COUNT(*) compte toutes les lignes. COUNT(col) ignore les NULL.\nSUM, AVG, MIN, MAX operent sur des valeurs numeriques ou dates.\nLes fonctions d agregation transforment plusieurs lignes en une valeur.", "code": "SELECT COUNT(*) AS nb_emp,\n       ROUND(AVG(salary), 2) AS sal_moy,\n       MIN(hire_date) AS premiere_embauche\nFROM   employees;", "result": "NB_EMP  SAL_MOY  PREMIERE_EMBAUCHE\n107     6461.83  17-JAN-2002", "pitfalls": ["COUNT(DISTINCT col) compte valeurs uniques non NULL", "AVG ignore les NULL dans le calcul"]},
            {"title": "GROUP BY", "content": "GROUP BY regroupe les lignes partageant les memes valeurs.\nToute colonne du SELECT non agregee doit figurer dans GROUP BY.\nOn peut grouper par plusieurs colonnes.", "code": "SELECT department_id,\n       COUNT(*) AS effectif,\n       ROUND(AVG(salary), 0) AS sal_moy\nFROM   employees\nGROUP BY department_id\nORDER BY effectif DESC;", "result": "DEPARTMENT_ID  EFFECTIF  SAL_MOY\n100            12        9500\n...", "pitfalls": ["WHERE filtre avant GROUP BY, HAVING apres", "Impossible de grouper par alias dans GROUP BY (sauf Oracle 12c+ avec certains cas)"]},
            {"title": "HAVING", "content": "HAVING filtre les groupes apres agregation.\nEquivalent de WHERE mais pour les resultats de GROUP BY.\nPeut utiliser des fonctions d agregation dans sa condition.", "code": "SELECT department_id, AVG(salary) AS sal_moy\nFROM   employees\nGROUP BY department_id\nHAVING AVG(salary) > 8000;", "result": "DEPARTMENT_ID  SAL_MOY\n90             19333.33\n...", "pitfalls": ["HAVING sans GROUP BY traite toute la table comme un groupe", "Ne pas confondre WHERE et HAVING"]}
        ]
    }
    mod5 = {
        "id": 5, "title": "Jointures",
        "summary": "INNER, OUTER (LEFT/RIGHT/FULL), SELF, NON-EQUI, NATURAL, USING et syntaxe Oracle (+).",
        "objectives": ["Maitriser les jointures ANSI et Oracle (+)", "Utiliser NATURAL JOIN et JOIN USING", "Comprendre les self-joins et non-equi-joins"],
        "sections": [
            {"title": "INNER JOIN", "content": "INNER JOIN retourne uniquement les lignes avec correspondance dans les deux tables.\nSyntaxe : FROM t1 JOIN t2 ON t1.col = t2.col ou FROM t1, t2 WHERE t1.col = t2.col (ancienne syntaxe).", "code": "SELECT e.last_name, d.department_name\nFROM   employees e\nINNER JOIN departments d\n  ON   e.department_id = d.department_id;", "result": "LAST_NAME  DEPARTMENT_NAME\nKing       Executive\n...", "pitfalls": ["Oublier la condition de jointure = produit cartesien", "Produit cartesien : n x m lignes"]},
            {"title": "OUTER JOIN et syntaxe (+)", "content": "LEFT OUTER JOIN : toutes les lignes de gauche + correspondances droite.\nRIGHT OUTER JOIN : inverse. FULL OUTER JOIN : toutes les lignes des deux cotes.\nOracle (+) : place sur la table qui peut manquer (cote oppose de la preservation).", "code": "SELECT e.last_name, d.department_name\nFROM   employees e, departments d\nWHERE  e.department_id = d.department_id(+);", "result": "Employes sans departement inclus avec DEPARTMENT_NAME NULL", "pitfalls": ["(+) ne peut pas etre combine avec (+) des deux cotes", "FULL OUTER JOIN n a pas d equivalent (+)"]},
            {"title": "SELF JOIN et NON-EQUI JOIN", "content": "SELF JOIN : une table jointe a elle-meme via alias differents.\nNON-EQUI JOIN : condition autre que l egalite (<, >, BETWEEN).", "code": "SELECT e.last_name AS employe,\n       m.last_name AS manager\nFROM   employees e\nJOIN   employees m ON e.manager_id = m.employee_id;", "result": "EMPLOYE   MANAGER\nKochhar   King\n...", "pitfalls": ["Alias obligatoires en self-join", "NATURAL JOIN joint sur toutes les colonnes de meme nom - risque de jointures imprevues"]}
        ]
    }
    mods.extend([mod3, mod4, mod5])
    return mods

MODULES.extend(build_remaining_modules())

def build_modules_6_14():
    return [
        {"id": 6, "title": "Sous-requetes", "summary": "Sous-requetes simples, correlees, ANY/ALL, EXISTS et sous-requetes dans FROM.", "objectives": ["Ecrire des sous-requetes scalars et multi-lignes", "Utiliser EXISTS vs IN", "Placer des sous-requetes dans FROM (inline views)"], "sections": [
            {"title": "Sous-requetes scalaires", "content": "Retourne une seule valeur. Utilisable dans SELECT, WHERE, HAVING.\nDoit retourner exactement une ligne et une colonne sinon erreur ORA-01427.", "code": "SELECT last_name, salary\nFROM   employees\nWHERE  salary > (SELECT AVG(salary) FROM employees);", "result": "Employes au-dessus de la moyenne", "pitfalls": ["Sous-requete scalar retournant 0 ligne = NULL en comparaison", "ORA-01427 si plusieurs lignes retournees"]},
            {"title": "ANY, ALL, IN", "content": "IN equivaut a = ANY. NOT IN ignore si sous-requete contient NULL.\n> ALL signifie superieur a toutes les valeurs. < ANY signifie inferieur a au moins une.", "code": "SELECT last_name FROM employees\nWHERE  salary > ALL (SELECT salary FROM employees WHERE department_id = 30);", "result": "Employes gagnant plus que tous ceux du dept 30", "pitfalls": ["NOT IN (NULL) retourne toujours FALSE/UNKNOWN", "EXISTS est plus performant que IN pour grandes tables"]},
            {"title": "EXISTS et sous-requetes correlees", "content": "EXISTS retourne TRUE si la sous-requete retourne au moins une ligne.\nCorrelee : la sous-requete reference la requete externe.", "code": "SELECT d.department_name\nFROM   departments d\nWHERE  EXISTS (SELECT 1 FROM employees e\n               WHERE e.department_id = d.department_id);", "result": "Departements ayant au moins un employe", "pitfalls": ["SELECT 1 ou SELECT NULL suffit avec EXISTS", "Correlee execute une fois par ligne externe"]}
        ]},
        {"id": 7, "title": "Operateurs ensemblistes", "summary": "UNION, UNION ALL, INTERSECT, MINUS - combinaison de resultats.", "objectives": ["Combiner des requetes avec UNION/INTERSECT/MINUS", "Differencier UNION et UNION ALL", "Respecter les regles de compatibilite des colonnes"], "sections": [
            {"title": "UNION et UNION ALL", "content": "UNION combine resultats et elimine les doublons (tri implicite).\nUNION ALL concatene sans eliminer les doublons - plus performant.\nLes requetes doivent avoir le meme nombre de colonnes compatibles.", "code": "SELECT last_name, job_id FROM employees WHERE department_id = 90\nUNION ALL\nSELECT last_name, job_id FROM employees WHERE department_id = 60;", "result": "Combinaison des deux departements", "pitfalls": ["UNION effectue un DISTINCT implicite", "Types de colonnes doivent etre compatibles (conversion implicite)"]},
            {"title": "INTERSECT et MINUS", "content": "INTERSECT retourne les lignes communes aux deux requetes.\nMINUS (Oracle) = EXCEPT (standard) : lignes de la 1ere absentes de la 2eme.\nOrdre : MINUS a priorite egale a UNION, evaluation de gauche a droite.", "code": "SELECT job_id FROM employees\nMINUS\nSELECT job_id FROM jobs WHERE max_salary < 5000;", "result": "Jobs occupes mais pas dans jobs bas salaire", "pitfalls": ["Pas de MINUS ALL en Oracle standard", "INTERSECT elimine aussi les doublons"]}
        ]},
        {"id": 8, "title": "Fonctions analytiques", "summary": "Fenetres analytiques OVER, ROW_NUMBER, RANK, LAG, LEAD.", "objectives": ["Utiliser OVER (PARTITION BY ORDER BY)", "Differencier RANK, DENSE_RANK, ROW_NUMBER", "Appliquer LAG et LEAD"], "sections": [
            {"title": "Syntaxe OVER", "content": "Fonctions analytiques calculent par fenetre sans reduire les lignes.\nOVER (PARTITION BY col ORDER BY col [ROWS|RANGE BETWEEN ...]).\nContrairement a GROUP BY, les lignes detail restent visibles.", "code": "SELECT last_name, department_id, salary,\n       AVG(salary) OVER (PARTITION BY department_id) AS moy_dept\nFROM   employees;", "result": "Chaque ligne avec moyenne de son departement", "pitfalls": ["Pas de GROUP BY avec analytiques sur meme niveau sans regles", "ORDER BY dans OVER definit la fenetre"]},
            {"title": "ROW_NUMBER, RANK, DENSE_RANK", "content": "ROW_NUMBER : numero unique sequentiel.\nRANK : meme rang pour ex-aequo, saute des numeros.\nDENSE_RANK : ex-aequo sans sauter de numeros.", "code": "SELECT last_name, salary,\n       ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,\n       RANK() OVER (ORDER BY salary DESC) AS rk\nFROM   employees\nWHERE  ROWNUM <= 10;", "result": "Classement par salaire", "pitfalls": ["ROW_NUMBER != ROWNUM", "ROWNUM assigne avant ORDER BY"]},
            {"title": "LAG et LEAD", "content": "LAG(col, offset, default) accede a la ligne precedente.\nLEAD accede a la ligne suivante dans la fenetre ordonnee.", "code": "SELECT last_name, hire_date,\n       LAG(hire_date) OVER (ORDER BY hire_date) AS embauche_precedente\nFROM   employees;", "result": "Date embauche employe precedent", "pitfalls": ["LAG/LEAD necessitent ORDER BY dans OVER", "Offset par defaut = 1"]}
        ]},
        {"id": 9, "title": "DML - Manipulation des donnees", "summary": "INSERT, UPDATE, DELETE, MERGE et clause FOR UPDATE.", "objectives": ["Inserer, modifier, supprimer des donnees", "Utiliser MERGE pour upsert", "Comprendre FOR UPDATE pour verrouillage"], "sections": [
            {"title": "INSERT et UPDATE", "content": "INSERT INTO ... VALUES ou INSERT INTO ... SELECT.\nUPDATE modifie des lignes existantes. WHERE obligatoire pour cibler.\nRETURNING INTO (PL/SQL) retourne les valeurs modifiees.", "code": "INSERT INTO employees (employee_id, last_name, email, hire_date, job_id)\nVALUES (999, 'Dupont', 'DUPONT', SYSDATE, 'IT_PROG');\n\nUPDATE employees SET salary = salary * 1.1\nWHERE  department_id = 80;", "result": "1 row inserted.\nN rows updated.", "pitfalls": ["Oublier WHERE en UPDATE = toutes les lignes", "Contraintes verifiees a chaque DML"]},
            {"title": "DELETE et MERGE", "content": "DELETE supprime des lignes. TRUNCATE supprime tout (DDL).\nMERGE combine INSERT/UPDATE selon correspondance ON.", "code": "MERGE INTO bonuses b\nUSING (SELECT employee_id, salary*0.1 AS bonus FROM employees) e\nON (b.employee_id = e.employee_id)\nWHEN MATCHED THEN UPDATE SET b.amount = e.bonus\nWHEN NOT MATCHED THEN INSERT (employee_id, amount) VALUES (e.employee_id, e.bonus);", "result": "Merge complete.", "pitfalls": ["DELETE sans WHERE supprime tout", "MERGE necessite une condition ON"]},
            {"title": "FOR UPDATE", "content": "SELECT ... FOR UPDATE verrouille les lignes selectionnees.\nEmpeche modification concurrente jusqu au COMMIT/ROLLBACK.\nFOR UPDATE OF col limite le verrouillage.", "code": "SELECT employee_id, salary\nFROM   employees\nWHERE  department_id = 90\nFOR UPDATE OF salary NOWAIT;", "result": "Lignes verrouillees", "pitfalls": ["NOWAIT echoue si verrou existe", "Join + FOR UPDATE : specifier table"]}
        ]},
        {"id": 10, "title": "DDL - Definition des structures", "summary": "CREATE, ALTER, DROP, TRUNCATE, contraintes et FLASHBACK.", "objectives": ["Creer et modifier tables avec contraintes", "Comprendre TRUNCATE vs DELETE", "Utiliser FLASHBACK TABLE"], "sections": [
            {"title": "CREATE TABLE et contraintes", "content": "Contraintes : PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK.\nInline ou out-of-line. Nommage explicite recommande.", "code": "CREATE TABLE emp_copy (\n  id NUMBER PRIMARY KEY,\n  nom VARCHAR2(50) NOT NULL,\n  dept_id NUMBER REFERENCES departments(department_id),\n  salaire NUMBER(8,2) CHECK (salaire > 0)\n);", "result": "Table created.", "pitfalls": ["FOREIGN KEY necessite cle primaire/unique parent", "CHECK condition par ligne"]},
            {"title": "ALTER et DROP", "content": "ALTER TABLE ADD/MODIFY/DROP column ou contrainte.\nDROP TABLE supprime structure et donnees. CASCADE CONSTRAINTS supprime FK dependantes.", "code": "ALTER TABLE emp_copy ADD (email VARCHAR2(100));\nALTER TABLE emp_copy MODIFY nom VARCHAR2(100);\nALTER TABLE emp_copy DROP COLUMN email;", "result": "Table altered.", "pitfalls": ["MODIFY sur colonne existante peut echouer si donnees incompatibles", "DROP COLUMN irreversible sans flashback"]},
            {"title": "TRUNCATE et FLASHBACK", "content": "TRUNCATE supprime toutes les lignes, conserve structure, COMMIT implicite.\nFLASHBACK TABLE TO TIMESTAMP/SYSTEM recupere donnees supprimees (si recycle bin/undo).", "code": "TRUNCATE TABLE emp_copy;\n-- FLASHBACK TABLE emp_copy TO TIMESTAMP ...", "result": "Table truncated.", "pitfalls": ["TRUNCATE ne peut pas etre ROLLBACK (DDL)", "FLASHBACK necessite UNDO et retention suffisante"]}
        ]},
        {"id": 11, "title": "Vues, Sequences, Index, Synonymes", "summary": "Objets schema Oracle : vues, sequences, index et synonymes.", "objectives": ["Creer des vues simples et complexes", "Gerer sequences pour auto-numerotation", "Comprendre index et synonymes"], "sections": [
            {"title": "Vues", "content": "Vue = requete stockee. CREATE OR REPLACE VIEW.\nWITH READ ONLY empeche DML. FORCE cree meme si tables absentes.", "code": "CREATE OR REPLACE VIEW v_emp_dept AS\nSELECT e.last_name, d.department_name, e.salary\nFROM   employees e JOIN departments d\n  ON   e.department_id = d.department_id\nWITH READ ONLY;", "result": "View created.", "pitfalls": ["Vue complexe peut etre non modifiable", "DROP VIEW vs DROP TABLE"]},
            {"title": "Sequences", "content": "Sequence genere numeros uniques. NEXTVAL avance, CURRVAL valeur courante session.\nCREATE SEQUENCE start WITH increment BY maxvalue cache.", "code": "CREATE SEQUENCE emp_seq START WITH 1000 INCREMENT BY 1;\nSELECT emp_seq.NEXTVAL FROM dual;\nINSERT INTO emp_copy (id, nom) VALUES (emp_seq.NEXTVAL, 'Martin');", "result": "1000 puis insertion", "pitfalls": ["CURRVAL invalide avant premier NEXTVAL en session", "Gaps normaux (rollback, cache)"]},
            {"title": "Index et synonymes", "content": "Index accelere les recherches. UNIQUE index enforce unicite.\nSynonyme = alias pour objet. CREATE SYNONYM ... FOR schema.objet.", "code": "CREATE INDEX idx_emp_dept ON employees(department_id);\nCREATE SYNONYM emp FOR hr.employees;", "result": "Index and synonym created.", "pitfalls": ["Trop d index ralentit DML", "Synonyme public necessite privilege CREATE PUBLIC SYNONYM"]}
        ]},
        {"id": 12, "title": "Dictionnaire de donnees", "summary": "Vues USER_*, ALL_*, DBA_* pour interroger les metadonnees.", "objectives": ["Interroger USER_TABLES, USER_TAB_COLUMNS", "Differencier USER, ALL et DBA prefixes", "Trouver contraintes et index"], "sections": [
            {"title": "Prefixes USER, ALL, DBA", "content": "USER_* : objets du schema connecte.\nALL_* : objets accessibles (privileges).\nDBA_* : tous objets (role DBA requis).", "code": "SELECT table_name FROM user_tables;\nSELECT column_name, data_type, nullable\nFROM   user_tab_columns\nWHERE  table_name = 'EMPLOYEES';", "result": "Liste tables et colonnes", "pitfalls": ["Noms en MAJUSCULES dans dictionnaire si non quotes", "USER_* vs ALL_* a l examen"]},
            {"title": "Contraintes et index", "content": "USER_CONSTRAINTS, USER_CONS_COLUMNS pour cles.\nUSER_INDEXES, USER_IND_COLUMNS pour index.", "code": "SELECT constraint_name, constraint_type\nFROM   user_constraints\nWHERE  table_name = 'EMPLOYEES';", "result": "P=Primary, R=Foreign, U=Unique, C=Check", "pitfalls": ["Constraint_type C peut etre NOT NULL ou CHECK", "TABLE_NAME en majuscules"]}
        ]},
        {"id": 13, "title": "Securite DCL", "summary": "Privileges systeme et objet, GRANT, REVOKE et roles.", "objectives": ["Accorder et revoquer privileges", "Comprendre roles predefinis", "Differencier privileges systeme et objet"], "sections": [
            {"title": "GRANT et REVOKE", "content": "GRANT privilege ON objet TO user [WITH GRANT OPTION].\nREVOKE retire privileges. CASCADE retire privileges delegues.", "code": "GRANT SELECT, UPDATE ON employees TO hr_clerk;\nGRANT CREATE SESSION TO hr_user;\nREVOKE UPDATE ON employees FROM hr_clerk;", "result": "Grant succeeded.", "pitfalls": ["WITH GRANT OPTION permet re-delegation", "REVOKE CASCADE CONSTRAINTS pour FK"]},
            {"title": "Roles", "content": "Role = groupe de privileges. CONNECT, RESOURCE (legacy), DBA.\nCREATE ROLE, GRANT role TO user.", "code": "CREATE ROLE read_only;\nGRANT SELECT ON employees TO read_only;\nGRANT read_only TO hr_report;", "result": "Role created and granted.", "pitfalls": ["Minimum CREATE SESSION pour connexion", "Roles simplifies administration"]}
        ]},
        {"id": 14, "title": "Pieges examen 1Z0-071", "summary": "Ordre execution SQL, NULL, ROWNUM vs ROW_NUMBER, pièges classiques.", "objectives": ["Maitriser l ordre logique d execution SQL", "Eviter les pieges NULL", "Differencier ROWNUM et fonctions analytiques"], "sections": [
            {"title": "Ordre d execution SQL", "content": "Ordre logique : FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY.\nROWNUM assigne lors de l acces aux lignes, avant ORDER BY.\nPour top-N : sous-requete avec ORDER BY puis filtre ROWNUM externe.", "code": "SELECT * FROM (\n  SELECT last_name, salary\n  FROM   employees\n  ORDER BY salary DESC\n) WHERE ROWNUM <= 5;", "result": "Top 5 salaires corrects", "pitfalls": ["WHERE ROWNUM <= 5 avant ORDER BY = 5 lignes aleatoires", "HAVING avant SELECT logiquement"]},
            {"title": "Pieges NULL", "content": "NULL = absence de valeur. Toute comparaison avec NULL = UNKNOWN.\nIS NULL / IS NOT NULL obligatoires.\nNVL, NVL2, COALESCE, NULLIF pour traiter NULL.\nCOUNT(col) ignore NULL, COUNT(*) non.", "code": "SELECT COUNT(*) AS total,\n       COUNT(commission_pct) AS avec_comm\nFROM   employees;", "result": "TOTAL 107, AVEC_COMM ~35", "pitfalls": ["WHERE col = NULL toujours faux", "NOT IN avec NULL dans liste"]},
            {"title": "ROWNUM vs ROW_NUMBER", "content": "ROWNUM pseudo-colonne assignee sequentiellement a la lecture.\nROW_NUMBER() fonction analytique apres tri.\nFETCH FIRST n ROWS ONLY (12c+) alternative moderne.", "code": "SELECT last_name,\n       ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn\nFROM   employees\nFETCH FIRST 5 ROWS ONLY;", "result": "Top 5 avec ROW_NUMBER", "pitfalls": ["ROWNUM > 1 impossible directement", "ROW_NUMBER peut avoir ex-aequo avec PARTITION"]}
        ]}
    ]

MODULES.extend(build_modules_6_14())

def generate_questions():
    """Generate 154 Oracle SQL certification questions."""
    questions = []
    qid = 1

    def add(module, question, options, correct, explanation, code=None):
        nonlocal qid
        questions.append({
            "id": qid, "module": module, "question": question,
            "options": options, "correctIndex": correct,
            "explanation": explanation, "code": code
        })
        qid += 1

    # Module 1 - 11 questions
    add(1, "Quelle categorie SQL comprend la commande CREATE TABLE ?", ["DML", "DDL", "DCL", "TCL"], 1, "CREATE TABLE modifie la structure = DDL (Data Definition Language).")
    add(1, "Quelle commande fait partie du TCL ?", ["GRANT", "SELECT", "COMMIT", "ALTER"], 2, "COMMIT valide une transaction = TCL.")
    add(1, "Quel type de contrainte garantit l unicite et interdit NULL ?", ["UNIQUE", "PRIMARY KEY", "FOREIGN KEY", "CHECK"], 1, "PRIMARY KEY = UNIQUE + NOT NULL.")
    add(1, "SELECT est classifie comme :", ["DDL", "DML", "DCL", "TCL"], 1, "A l examen Oracle, SELECT est DML.")
    add(1, "TRUNCATE est une commande :", ["DML avec rollback possible", "DDL avec commit implicite", "DCL", "TCL"], 1, "TRUNCATE = DDL, commit implicite, non rollbackable.")
    add(1, "Une cle etrangere reference :", ["N importe quelle colonne", "Une cle primaire ou unique parent", "Une vue", "Un index"], 1, "FK reference PK ou UNIQUE de la table parente.")
    add(1, "GRANT appartient a :", ["DDL", "DML", "DCL", "TCL"], 2, "GRANT/REVOKE = DCL.")
    add(1, "ROLLBACK appartient a :", ["DDL", "DML", "DCL", "TCL"], 3, "ROLLBACK annule transaction = TCL.")
    add(1, "Le modele relationnel stocke les donnees sous forme de :", ["Documents JSON", "Tables", "Graphes", "Fichiers"], 1, "Modele relationnel = tables.")
    add(1, "Une relation 1:N signifie :", ["Un enregistrement lie a un seul", "Un enregistrement lie a plusieurs", "Plusieurs a plusieurs", "Aucune relation"], 1, "1:N = un parent, plusieurs enfants.")
    add(1, "Le dictionnaire de donnees Oracle est consulte via :", ["Vues USER_*/ALL_*/DBA_*", "Table DUAL uniquement", "Fichiers redo log", "Control file directement"], 0, "Metadonnees dans vues USER_, ALL_, DBA_.")

    # Module 2 - 12 questions
    add(2, "Quelle table Oracle permet d evaluer des expressions sans table metier ?", ["EMPLOYEES", "DUAL", "SYSTEM", "SYS"], 1, "DUAL = table dummy Oracle.")
    add(2, "SUBSTR('ORACLE', 2, 3) retourne :", ["ORA", "RAC", "RACLE", "OR"], 1, "Position 2, longueur 3 = RAC.")
    add(2, "NVL(commission_pct, 0) remplace :", ["Zero par NULL", "NULL par 0", "Toutes valeurs par 0", "Erreur si NULL"], 1, "NVL remplace NULL par la valeur 2.")
    add(2, "La concatenation Oracle utilise :", ["+", "||", "CONCAT uniquement", "&"], 1, "|| est l operateur de concatenation.")
    add(2, "TO_CHAR(salary, '999,999') sert a :", ["Convertir texte en nombre", "Formater nombre en texte", "Convertir date", "Supprimer format"], 1, "TO_CHAR formate en chaine.")
    add(2, "UPPER('Sql') retourne :", ["sql", "SQL", "Sql", "ERROR"], 1, "UPPER met en majuscules.")
    add(2, "LENGTH('Oracle') retourne :", ["5", "6", "7", "8"], 1, "6 caracteres.")
    add(2, "INITCAP('jean dupont') retourne :", ["JEAN DUPONT", "Jean Dupont", "jean dupont", "Jean dupont"], 1, "INITCAP capitalise chaque mot.")
    add(2, "Un alias de colonne est defini avec :", ["ALIAS uniquement", "AS ou espace", "RENAME", "LABEL"], 1, "AS ou espace apres expression.")
    add(2, "DISTINCT dans SELECT :", ["Trie les resultats", "Elimine les doublons", "Filtre les NULL", "Compte les lignes"], 1, "DISTINCT supprime combinaisons dupliquees.")
    add(2, "MOD(10, 3) retourne :", ["3", "1", "0", "10"], 1, "Reste de 10/3 = 1.")
    add(2, "CASE WHEN salary > 10000 THEN 'H' ELSE 'L' END est :", ["Fonction d agregation", "Expression conditionnelle", "Jointure", "Sous-requete"], 1, "CASE = expression conditionnelle.")

    # Module 3 - 11 questions
    add(3, "BETWEEN 100 AND 200 inclut :", ["100 et 200", "101 a 199", "100 seulement", "200 seulement"], 0, "BETWEEN inclut les bornes.")
    add(3, "WHERE last_name LIKE 'S%' trouve :", ["Noms finissant par S", "Noms commencant par S", "Noms avec S au milieu", "Exactement S"], 1, "% = zero ou plus caracteres apres S.")
    add(3, "Pour tester NULL on utilise :", ["= NULL", "IS NULL", "== NULL", "EQUALS NULL"], 1, "IS NULL est la syntaxe correcte.")
    add(3, "ORDER BY salary DESC trie :", ["Croissant", "Decroissant", "Alphabetique", "Par departement"], 1, "DESC = decroissant.")
    add(3, "NULLS FIRST avec ORDER BY DESC place NULL :", ["En premier", "En dernier", "Exclus", "Erreur"], 0, "NULLS FIRST explicite.")
    add(3, "NOT IN (1, 2, NULL) retourne :", ["Toutes lignes", "Aucune ligne", "Erreur", "Lignes sauf 1 et 2"], 1, "NULL dans NOT IN = resultat vide/unknown.")
    add(3, "WHERE a = 5 AND b = 10 : si a=5 et b=NULL resultat :", ["TRUE", "FALSE", "UNKNOWN/FALSE", "Erreur"], 2, "AND avec NULL = UNKNOWN, ligne exclue.")
    add(3, "IN (10, 20, 30) equivaut a :", ["= ANY (...)", "= ALL (...)", "BETWEEN 10 AND 30", "LIKE"], 0, "IN = = ANY.")
    add(3, "Le joker _ dans LIKE signifie :", ["Zero ou plus caracteres", "Exactement un caractere", "N importe quel caractere special", "Debut de chaine"], 1, "_ = un caractere.")
    add(3, "WHERE peut utiliser un alias de colonne ?", ["Oui toujours", "Non", "Seulement avec AS", "Seulement en Oracle 19c"], 1, "Alias non disponibles dans WHERE.")
    add(3, "ORDER BY peut utiliser un alias ?", ["Non", "Oui", "Seulement en HAVING", "Seulement avec DISTINCT"], 1, "ORDER BY accepte les alias.")

    # Module 4 - 12 questions
    add(4, "COUNT(*) compte :", ["Valeurs non NULL", "Toutes les lignes", "Distinct values", "Groupes uniquement"], 1, "COUNT(*) = toutes lignes.")
    add(4, "COUNT(email) ignore :", ["Doublons", "NULL", "Zero", "Espaces"], 1, "COUNT(col) ignore NULL.")
    add(4, "HAVING filtre :", ["Avant GROUP BY", "Apres GROUP BY", "Avant WHERE", "Les colonnes seulement"], 1, "HAVING filtre les groupes.")
    add(4, "WHERE salary > 5000 avec GROUP BY department_id :", ["Valide si salary dans GROUP BY", "Valide car filtre avant agregation", "Erreur", "Remplace HAVING"], 1, "WHERE filtre lignes avant groupement.")
    add(4, "AVG(salary) ignore :", ["Zero", "NULL", "Negatifs", "Doublons"], 1, "AVG ignore NULL.")
    add(4, "SELECT dept, AVG(sal) sans GROUP BY dept :", ["Valide", "Erreur ORA", "Retourne NULL", "Retourne une ligne"], 1, "Colonne non agregee doit etre dans GROUP BY.")
    add(4, "GROUP BY department_id, job_id cree groupes par :", ["Dept seulement", "Combinaison dept+job", "Job seulement", "Toute la table"], 1, "Groupes = combinaison unique.")
    add(4, "HAVING COUNT(*) > 5 equivaut logiquement a filtrer :", ["Lignes individuelles", "Groupes ayant plus de 5 membres", "Colonnes", "Index"], 1, "HAVING sur agregat de groupe.")
    add(4, "SUM(DISTINCT salary) :", ["Somme avec doublons", "Somme valeurs uniques", "Erreur", "Compte lignes"], 1, "DISTINCT dans agregat.")
    add(4, "MIN() peut s appliquer a :", ["Numeriques seulement", "Dates et nombres", "Texte seulement", "BLOB"], 1, "MIN/MAX sur dates et nombres.")
    add(4, "SELECT COUNT(DISTINCT department_id) :", ["Compte tous dept", "Compte dept uniques", "Erreur", "Compte lignes"], 1, "DISTINCT = uniques.")
    add(4, "Sans GROUP BY, COUNT(*) retourne :", ["Une ligne", "Une ligne par dept", "Erreur", "Zero lignes"], 0, "Agregat sans GROUP BY = une ligne.")

    # Module 5 - 12 questions
    add(5, "INNER JOIN retourne :", ["Toutes lignes des deux tables", "Lignes avec correspondance", "Lignes sans correspondance", "Produit cartesien"], 1, "INNER = intersection.")
    add(5, "LEFT OUTER JOIN preserve :", ["Table droite", "Table gauche", "Les deux", "Aucune"], 1, "LEFT preserve gauche.")
    add(5, "En syntaxe Oracle (+), pour LEFT JOIN sur e.dept=d.dept_id :", ["(+) sur e.dept_id", "(+) sur d.department_id", "(+) des deux cotes", "Pas de (+)"], 1, "(+) cote table non preservee (droite).")
    add(5, "Produit cartesien resulte de :", ["JOIN sans ON", "INNER JOIN", "UNION", "GROUP BY"], 0, "Jointure sans condition = cartesien.")
    add(5, "NATURAL JOIN joint sur :", ["Cle primaire", "Colonnes meme nom", "Toutes colonnes", "Index"], 1, "Colonnes identiques nom.")
    add(5, "JOIN USING (department_id) :", ["Requiert alias", "Joint sur colonne commune nommee", "Est un CROSS JOIN", "Remplace WHERE"], 1, "USING(col) joint sur nom identique.")
    add(5, "FULL OUTER JOIN :", ["Existe en syntaxe (+)", "Retourne toutes lignes des deux", "Identique INNER", "Exclut NULL"], 1, "FULL = union des OUTER.")
    add(5, "Self-join necessite :", ["Deux tables differentes", "Alias de table", "UNION", "HAVING"], 1, "Alias pour distinguer instances.")
    add(5, "CROSS JOIN produit :", ["Lignes correspondantes", "Produit cartesien", "UNION", "INTERSECT"], 1, "CROSS JOIN = cartesien explicite.")
    add(5, "RIGHT JOIN a.dept = b.dept equivaut LEFT JOIN :", ["Identique", "b LEFT JOIN a", "Impossible", "FULL JOIN"], 1, "RIGHT(a,b) = LEFT(b,a).")
    add(5, "Non-equi join utilise :", ["= uniquement", "<, >, BETWEEN", "UNION", "MINUS"], 1, "Conditions non-egalite.")
    add(5, "Combien de (+) max par condition ?", ["0", "1", "2", "Illimite"], 1, "Un seul cote par condition.")

    # Module 6 - 11 questions
    add(6, "Sous-requete scalar doit retourner :", ["Plusieurs lignes", "Une ligne, une colonne", "Zero colonnes", "Plusieurs colonnes"], 1, "Scalar = 1 ligne, 1 colonne.")
    add(6, "EXISTS retourne TRUE si :", ["Sous-requete retourne 0 ligne", "Au moins une ligne", "Valeur NULL", "Erreur"], 1, "EXISTS teste presence lignes.")
    add(6, "IN vs EXISTS : performance souvent favorise :", ["IN toujours", "EXISTS pour grandes tables correlees", "Identique", "NOT EXISTS jamais"], 1, "EXISTS s arretent au premier match.")
    add(6, "> ALL (100, 200) signifie :", ["Superieur a au moins un", "Superieur a tous", "Inferieur a tous", "Egal a un"], 1, "> ALL = superieur a chaque valeur.")
    add(6, "Sous-requete dans FROM est :", ["Inline view", "Scalar subquery", "Correlee obligatoire", "Interdit"], 0, "FROM (SELECT...) = inline view.")
    add(6, "Correlated subquery :", ["Independante", "Reference requete externe", "Dans SELECT uniquement", "Retourne toujours NULL"], 1, "Reference colonnes externes.")
    add(6, "ORA-01427 indique :", ["Division par zero", "Sous-requete retourne trop de lignes", "Syntaxe invalide", "Table inexistante"], 1, "Single-row subquery returns more than one row.")
    add(6, "< ANY (5, 10, 15) signifie :", ["Inferieur a tous", "Inferieur a au moins un", "Superieur a tous", "Egal"], 1, "< ANY = inferieur a un des valeurs.")
    add(6, "SELECT avec sous-requete dans SELECT (scalar) :", ["Interdit", "Autorise si 1 ligne/col", "Requiert GROUP BY", "Requiert UNION"], 1, "Scalar subquery dans SELECT OK.")
    add(6, "NOT EXISTS (SELECT 1 FROM ... WHERE ...) :", ["Retourne lignes si sous-requete vide", "Retourne lignes si sous-requete a lignes", "Erreur", "Equivaut IN"], 0, "NOT EXISTS vrai si sous-requete vide.")
    add(6, "= ANY equivaut a :", ["IN", "NOT IN", "ALL", "EXISTS"], 0, "= ANY = IN.")

    # Module 7 - 10 questions
    add(7, "UNION vs UNION ALL :", ["Identiques", "UNION elimine doublons", "UNION ALL elimine doublons", "UNION ALL trie"], 1, "UNION = distinct implicite.")
    add(7, "INTERSECT retourne :", ["Lignes des deux requetes", "Lignes communes", "Lignes differentes", "Produit cartesien"], 1, "INTERSECT = intersection ensembliste.")
    add(7, "MINUS en Oracle equivaut a :", ["UNION", "EXCEPT en SQL standard", "INTERSECT", "CROSS JOIN"], 1, "MINUS = EXCEPT.")
    add(7, "Requetes en UNION doivent avoir :", ["Meme nombre colonnes compatibles", "Meme table", "Meme WHERE", "GROUP BY identique"], 0, "Meme nb colonnes, types compatibles.")
    add(7, "ORDER BY avec UNION s applique :", ["A chaque requete", "Au resultat final", "Impossible", "Seulement premier SELECT"], 1, "ORDER BY final sur ensemble.")
    add(7, "UNION ALL est :", ["Plus lent que UNION", "Plus rapide car pas de dedup", "Interdit en Oracle", "Identique INTERSECT"], 1, "Pas de tri/distinct = plus rapide.")
    add(7, "MINUS A MINUS B :", ["Ordre important", "Commutatif", "Impossible", "Egale INTERSECT"], 0, "MINUS non commutatif.")
    add(7, "Colonne 1 number, colonne 1 varchar en UNION :", ["Erreur toujours", "Conversion implicite possible", "Interdit Oracle", "UNION ALL requis"], 1, "Oracle convertit implicitement si possible.")
    add(7, "INTERSECT elimine :", ["Doublons", "NULL", "Colonnes", "Index"], 0, "INTERSECT fait DISTINCT.")
    add(7, "Combien de requetes minimum pour UNION ?", ["1", "2", "3", "4"], 1, "Au moins 2 SELECT.")

    # Module 8 - 11 questions
    add(8, "AVG(sal) OVER (PARTITION BY dept) calcule :", ["Moyenne globale", "Moyenne par departement", "Somme", "Count"], 1, "PARTITION BY dept = fenetre par dept.")
    add(8, "ROW_NUMBER vs RANK avec ex-aequo :", ["Identiques", "RANK saute numeros", "ROW_NUMBER saute", "RANK identique toujours"], 1, "RANK 1,1,3 vs ROW_NUMBER 1,2,3.")
    add(8, "LAG(salary, 1) retourne :", ["Salaire suivant", "Salaire ligne precedente", "Premier salaire", "Moyenne"], 1, "LAG = ligne precedente.")
    add(8, "OVER () sans PARTITION BY :", ["Erreur", "Fenetre sur toute la table", "Une ligne", "NULL"], 1, "Pas de partition = table entiere.")
    add(8, "DENSE_RANK vs RANK :", ["DENSE_RANK saute des rangs", "DENSE_RANK ne saute pas", "Identiques", "DENSE_RANK plus lent"], 1, "DENSE_RANK 1,1,2 sans gap.")
    add(8, "Fonctions analytiques vs GROUP BY :", ["Reduisent lignes", "Conservent detail lignes", "Identiques", "Interdites ensemble"], 1, "Analytiques gardent chaque ligne.")
    add(8, "LEAD(hire_date, 2) :", ["2 dates avant", "2 dates apres", "Erreur", "Date actuelle"], 1, "LEAD = lignes suivantes, offset 2.")
    add(8, "FIRST_VALUE(salary) OVER (...) :", ["Derniere valeur", "Premiere valeur fenetre", "Minimum", "Maximum"], 1, "FIRST_VALUE = premiere de la fenetre.")
    add(8, "ORDER BY dans OVER est requis pour :", ["COUNT(*)", "ROW_NUMBER", "SUM sans tri", "MAX"], 1, "ROW_NUMBER necessite ORDER BY.")
    add(8, "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW :", ["Fenetre mobile", "Fenetre cumulative", "Erreur", "Toute partition"], 1, "Cumulative depuis debut partition.")
    add(8, "SUM(sal) OVER (ORDER BY hire_date) :", ["Somme globale", "Somme cumulative", "Moyenne", "Count"], 1, "Running total avec ORDER BY.")

    # Module 9 - 11 questions
    add(9, "INSERT INTO t SELECT ... :", ["Interdit", "Insert depuis requete", "Update", "Merge"], 1, "INSERT...SELECT valide.")
    add(9, "UPDATE sans WHERE :", ["Erreur", "Modifie toutes lignes", "Modifie une ligne", "Rollback auto"], 1, "Sans WHERE = toutes lignes.")
    add(9, "DELETE vs TRUNCATE :", ["Identiques", "DELETE DML rollbackable, TRUNCATE DDL", "TRUNCATE rollbackable", "DELETE plus rapide toujours"], 1, "DELETE DML, TRUNCATE DDL.")
    add(9, "MERGE ... ON (...) WHEN MATCHED :", ["Insert seulement", "Update si correspondance", "Delete seulement", "Truncate"], 1, "WHEN MATCHED = UPDATE typiquement.")
    add(9, "FOR UPDATE sur SELECT :", ["Lecture seule", "Verrouille lignes", "Commit auto", "Supprime lignes"], 1, "Verrou pessimiste.")
    add(9, "INSERT avec liste colonnes explicite :", ["Obligatoire", "Recommandee/bonne pratique", "Interdite", "Remplace VALUES"], 1, "Specifie colonnes ciblees.")
    add(9, "SAVEPOINT :", ["Valide transaction", "Point de rollback partiel", "DDL", "Grant privilege"], 1, "SAVEPOINT = rollback partiel.")
    add(9, "WHEN NOT MATCHED THEN INSERT dans MERGE :", ["Update", "Insert nouvelles lignes", "Delete", "Truncate"], 1, "NOT MATCHED = INSERT.")
    add(9, "FOR UPDATE NOWAIT :", ["Attend indefiniment", "Erreur si verrou indisponible", "Ignore verrous", "Commit"], 1, "NOWAIT = pas d attente.")
    add(9, "Apres INSERT sans COMMIT :", ["Visible par tous", "Visible session courante", "Permanent", "Rollback impossible"], 1, "Non commite = session seulement.")
    add(9, "RETURNING clause avec INSERT :", ["Interdit SQL", "Retourne valeurs inserees (SQL/PLSQL)", "Remplace SELECT", "DDL only"], 1, "RETURNING disponible DML.")

    # Module 10 - 11 questions
    add(10, "ALTER TABLE ADD column :", ["Supprime colonne", "Ajoute colonne", "Cree table", "Drop index"], 1, "ADD ajoute colonne.")
    add(10, "CHECK constraint verifie :", ["Par transaction", "Par ligne inseree/modifiee", "Par table entiere", "Jamais"], 1, "CHECK par ligne.")
    add(10, "DROP TABLE CASCADE CONSTRAINTS :", ["Garde FK dependantes", "Supprime FK dependantes", "Erreur", "Truncate"], 1, "CASCADE supprime contraintes dependantes.")
    add(10, "CREATE TABLE AS SELECT (CTAS) :", ["Cree table vide", "Cree table avec donnees", "Cree vue", "Insert seulement"], 1, "CTAS copie structure+donnees.")
    add(10, "FLASHBACK TABLE necessite :", ["Privilege FLASHBACK", "DBA only toujours", "Impossible Oracle", "DROP d abord"], 0, "FLASHBACK TABLE privilege requis.")
    add(10, "NOT NULL constraint :", ["Permet NULL", "Interdit NULL", "Unique seulement", "FK"], 1, "NOT NULL interdit NULL.")
    add(10, "RENAME TABLE en Oracle :", ["ALTER TABLE ... RENAME TO", "RENAME TABLE", "UPDATE", "Impossible"], 0, "ALTER TABLE t RENAME TO new_t.")
    add(10, "PRIMARY KEY implique :", ["UNIQUE seulement", "UNIQUE + NOT NULL", "FK", "CHECK"], 1, "PK = unique + not null.")
    add(10, "TRUNCATE libere espace immediatement ?", ["Toujours", "Depend options/storage", "Jamais", "DELETE identique"], 1, "TRUNCATE DEALLOCATE selon config.")
    add(10, "ADD CONSTRAINT pk PRIMARY KEY :", ["Out-of-line ou inline", "Interdit", "Vue seulement", "Index seulement"], 0, "Contraintes inline ou out-of-line.")
    add(10, "MODIFY column en Oracle :", ["Change type/taille", "Supprime table", "Grant", "Merge"], 0, "MODIFY altere colonne.")

    # Module 11 - 10 questions
    add(11, "CREATE SEQUENCE : NEXTVAL :", ["Valeur precedente", "Prochaine valeur", "Reset", "Currant sans avance"], 1, "NEXTVAL avance sequence.")
    add(11, "CURRVAL avant NEXTVAL en session :", ["Retourne 0", "Erreur ORA", "Retourne 1", "Retourne NULL"], 1, "CURRVAL invalide avant NEXTVAL.")
    add(11, "CREATE VIEW :", ["Stocke donnees", "Stocke requete", "Est une table", "Index"], 1, "Vue = requete enregistree.")
    add(11, "Index UNIQUE :", ["Permet doublons", "Enforce unicite", "Remplace PK", "Interdit SELECT"], 1, "UNIQUE index = unicite.")
    add(11, "Synonyme PUBLIC :", ["Schema user only", "Accessible tous users", "DBA only view", "Temporaire"], 1, "PUBLIC synonyme global.")
    add(11, "WITH READ ONLY sur vue :", ["Permet INSERT", "Interdit DML", "Supprime vue", "Cree index"], 1, "READ ONLY bloque modifications.")
    add(11, "Sequence CACHE option :", ["Stocke en memoire pour perf", "Supprime gaps", "Interdit NEXTVAL", "Rollback proof"], 0, "CACHE pre-alloue valeurs.")
    add(11, "CREATE INDEX sur FK column :", ["Inutile", "Ameliore jointures/recherches", "Interdit", "Remplace FK"], 1, "Index sur FK = bonne pratique.")
    add(11, "CREATE OR REPLACE VIEW :", ["Erreur si existe", "Remplace vue existante", "Cree nouvelle table", "Drop table"], 1, "OR REPLACE met a jour definition.")
    add(11, "Synonyme prive :", ["Schema owner seulement", "User courant", "Tous schemas", "PUBLIC"], 1, "Synonyme prive = user/schema.")

    # Module 12 - 10 questions
    add(12, "USER_TABLES liste :", ["Toutes tables BD", "Tables du schema connecte", "Tables DBA only", "Vues seulement"], 1, "USER_* = schema courant.")
    add(12, "ALL_TABLES vs USER_TABLES :", ["Identiques", "ALL inclut accessibles", "USER inclut tout", "ALL = DBA"], 1, "ALL = objets avec privilege.")
    add(12, "USER_TAB_COLUMNS contient :", ["Donnees lignes", "Metadonnees colonnes", "Privileges", "Redo logs"], 1, "Colonnes des tables user.")
    add(12, "TABLE_NAME dans dictionnaire sans quotes :", ["minuscules", "MAJUSCULES", "mixte", "NULL"], 1, "Noms non quotes = uppercase.")
    add(12, "USER_CONSTRAINTS constraint_type R :", ["Primary Key", "Foreign Key", "Unique", "Check"], 1, "R = Referential (FK).")
    add(12, "DBA_* vues necessitent :", ["Aucun privilege", "Role/privileges DBA", "CONNECT only", "Synonyme"], 1, "DBA_* = vue administration.")
    add(12, "USER_INDEXES montre :", ["Toutes indexes BD", "Indexes du schema user", "FK seulement", "Sequences"], 1, "Indexes du schema connecte.")
    add(12, "USER_VIEWS :", ["Tables", "Vues du schema", "Synonymes", "Sequences"], 1, "Liste des vues.")
    add(12, "USER_SEQUENCES :", ["Tables", "Sequences du schema", "Jobs", "Roles"], 1, "Metadonnees sequences.")
    add(12, "USER_SYNONYMS :", ["Synonymes accessibles user", "Tous publics", "DBA only", "FK"], 0, "Synonymes du user.")

    # Module 13 - 10 questions
    add(13, "GRANT SELECT ON table TO user :", ["Privilege objet", "Privilege systeme", "Role", "DDL"], 0, "SELECT ON = privilege objet.")
    add(13, "CREATE SESSION permet :", ["Creer tables", "Se connecter", "DROP user", "Backup"], 1, "CREATE SESSION = connexion.")
    add(13, "WITH GRANT OPTION :", ["Revoke auto", "Permet re-deleguer privilege", "Cree role", "Commit"], 1, "Delegue le droit de GRANT.")
    add(13, "REVOKE SELECT ON t FROM u CASCADE :", ["Ignore dependances", "Revoke aussi privileges delegues", "Erreur", "Drop table"], 1, "CASCADE retire delegations.")
    add(13, "Privilege systeme exemple :", ["SELECT ON emp", "CREATE TABLE", "INSERT ON dept", "UPDATE col"], 1, "CREATE TABLE = systeme.")
    add(13, "Role CONNECT (legacy) incluait :", ["DBA", "CREATE SESSION typiquement", "DROP ANY TABLE", "SYSDBA"], 1, "CONNECT = connexion basique.")
    add(13, "Object privilege INSERT :", ["Creer table", "Inserer lignes table", "Grant role", "Alter system"], 1, "INSERT ON table.")
    add(13, "REVOKE sans CASCADE :", ["Revoke delegues aussi", "Revoke seulement user direct", "Erreur", "Drop user"], 1, "Sans CASCADE = direct seulement.")
    add(13, "CREATE USER necessite typiquement :", ["SELECT", "Privilege CREATE USER (DBA)", "Synonyme", "Sequence"], 1, "Admin privilege pour CREATE USER.")
    add(13, "GRANT role TO user :", ["Accorde privileges du role", "Cree table", "Revoke", "Commit"], 0, "Role regroupe privileges.")

    # Module 14 - 12 questions
    add(14, "Ordre logique : WHERE avant :", ["FROM", "SELECT", "GROUP BY", "ORDER BY"], 2, "FROM->WHERE->GROUP BY->HAVING->SELECT->ORDER BY.")
    add(14, "SELECT * FROM t WHERE ROWNUM <= 5 ORDER BY sal DESC :", ["Top 5 salaires", "5 lignes aleatoires triees", "Erreur", "Toutes lignes"], 1, "ROWNUM avant ORDER BY = mauvais top-N.")
    add(14, "WHERE col = NULL retourne :", ["Lignes NULL", "Aucune ligne", "Erreur syntaxe", "Toutes lignes"], 1, "= NULL toujours UNKNOWN.")
    add(14, "ROWNUM > 1 directement :", ["Retourne lignes 2+", "Retourne 0 lignes", "Erreur", "Toutes lignes"], 1, "ROWNUM > 1 impossible sans sous-requete.")
    add(14, "FETCH FIRST 5 ROWS ONLY (12c+) :", ["Syntaxe top-N moderne", "Interdit", "Remplace MERGE", "DDL"], 0, "Alternative a ROWNUM pour top-N.")
    add(14, "COUNT(*) vs COUNT(col) avec NULLs :", ["Identiques", "COUNT(*) inclut NULL lignes", "COUNT(col) compte NULL", "Erreur"], 1, "COUNT(*) compte lignes, COUNT(col) ignore NULL valeurs.")
    add(14, "HAVING sans GROUP BY :", ["Erreur toujours", "Traite table entiere comme un groupe", "Interdit Oracle", "Remplace WHERE"], 1, "Agregat sans GROUP BY = 1 groupe.")
    add(14, "DECODE vs CASE :", ["DECODE plus flexible", "CASE plus flexible", "Identiques", "DECODE standard SQL"], 1, "CASE = standard, plus flexible.")
    add(14, "SYSDATE retourne :", ["Date sans heure", "Date et heure courante", "Timestamp UTC", "Nombre"], 1, "SYSDATE = date+heure serveur.")
    add(14, "TO_DATE sans format mask :", ["Toujours OK", "Depend NLS, risque erreur", "Interdit", "Retourne SYSDATE"], 1, "Format explicite recommande.")
    add(14, "MINUS ALL existe en Oracle ?", ["Oui", "Non standard Oracle", "Identique MINUS", "Requis"], 1, "Oracle a MINUS pas MINUS ALL standard.")
    add(14, "SELECT DISTINCT applique avant ORDER BY ?", ["Non", "Oui logiquement", "Apres ORDER BY", "Remplace GROUP BY"], 1, "DISTINCT avant ORDER BY logiquement.")

    return questions

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, "modules.json"), "w", encoding="utf-8") as f:
        json.dump({"modules": MODULES}, f, ensure_ascii=False, indent=2)
    questions = generate_questions()
    with open(os.path.join(DATA_DIR, "questions.json"), "w", encoding="utf-8") as f:
        json.dump({"questions": questions}, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(MODULES)} modules and {len(questions)} questions")

if __name__ == "__main__":
    main()
