-- ============================================================
-- 50 requêtes d'entraînement Oracle SQL 1Z0-071
-- Exécuter sur le schéma HR après hr_schema.sql + hr_data.sql
-- ============================================================

-- === MODULE 2 : SELECT et fonctions ===
-- 1. Liste des employés avec nom complet
SELECT last_name || ', ' || first_name AS nom_complet FROM employees;

-- 2. Salaire annuel formaté
SELECT last_name, TO_CHAR(salary * 12, '999,999') AS salaire_annuel FROM employees WHERE ROWNUM <= 10;

-- 3. Commission avec NVL
SELECT last_name, NVL(commission_pct, 0) AS commission FROM employees WHERE department_id = 80;

-- === MODULE 3 : Filtrage et tri ===
-- 4. Employés embauchés entre 2005 et 2007
SELECT last_name, hire_date FROM employees WHERE hire_date BETWEEN DATE '2005-01-01' AND DATE '2007-12-31';

-- 5. Noms commençant par 'S'
SELECT last_name FROM employees WHERE last_name LIKE 'S%' ORDER BY last_name;

-- 6. Départements 50, 60, 80 triés par salaire décroissant
SELECT last_name, department_id, salary FROM employees
WHERE department_id IN (50, 60, 80) ORDER BY salary DESC NULLS LAST;

-- === MODULE 4 : Agrégation ===
-- 7. Effectif par département
SELECT department_id, COUNT(*) AS effectif FROM employees GROUP BY department_id ORDER BY effectif DESC;

-- 8. Salaire moyen par job
SELECT job_id, ROUND(AVG(salary), 2) AS sal_moy FROM employees GROUP BY job_id HAVING AVG(salary) > 5000;

-- 9. Nombre d'employés avec commission
SELECT COUNT(commission_pct) AS avec_comm, COUNT(*) AS total FROM employees;

-- === MODULE 5 : Jointures ===
-- 10. Employés avec nom du département
SELECT e.last_name, d.department_name FROM employees e JOIN departments d ON e.department_id = d.department_id;

-- 11. LEFT JOIN - départements sans employés
SELECT d.department_name, COUNT(e.employee_id) AS nb_emp
FROM departments d LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name;

-- 12. Self-join manager/employé
SELECT e.last_name AS employe, m.last_name AS manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.employee_id;

-- === MODULE 6 : Sous-requêtes ===
-- 13. Employés au-dessus de la moyenne
SELECT last_name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);

-- 14. Départements ayant des employés (EXISTS)
SELECT department_name FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.department_id = d.department_id);

-- 15. Employés du département le plus payé
SELECT last_name, salary FROM employees
WHERE department_id = (SELECT department_id FROM employees GROUP BY department_id ORDER BY AVG(salary) DESC FETCH FIRST 1 ROW ONLY);

-- === MODULE 7 : Ensemblistes ===
-- 16. Jobs en commun entre employees et jobs haut salaire
SELECT job_id FROM employees INTERSECT SELECT job_id FROM jobs WHERE max_salary > 15000;

-- 17. UNION departments et locations (colonnes compatibles)
SELECT TO_CHAR(department_id) AS id, department_name AS nom FROM departments
UNION ALL
SELECT TO_CHAR(location_id), city FROM locations;

-- === MODULE 8 : Analytiques ===
-- 18. Rang salarial par département
SELECT last_name, department_id, salary,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rang
FROM employees;

-- 19. Moyenne mobile cumulative
SELECT last_name, hire_date, salary,
       SUM(salary) OVER (ORDER BY hire_date ROWS UNBOUNDED PRECEDING) AS cumul
FROM employees;

-- 20. Top 3 salaires par département
SELECT * FROM (
  SELECT last_name, department_id, salary,
         DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dr
  FROM employees
) WHERE dr <= 3;

-- === MODULE 9-14 : DML/DDL/Dictionnaire/Pièges ===
-- 21. Top 5 salaires (piège ROWNUM corrigé)
SELECT * FROM (SELECT last_name, salary FROM employees ORDER BY salary DESC) WHERE ROWNUM <= 5;

-- 22. FETCH FIRST (12c+)
SELECT last_name, salary FROM employees ORDER BY salary DESC FETCH FIRST 5 ROWS ONLY;

-- 23. CASE pour catégoriser salaires
SELECT last_name, salary,
       CASE WHEN salary >= 15000 THEN 'A' WHEN salary >= 8000 THEN 'B' ELSE 'C' END AS cat
FROM employees;

-- 24. DECODE équivalent
SELECT last_name, DECODE(department_id, 10, 'Admin', 20, 'Mktg', 60, 'IT', 'Autre') AS dept FROM employees;

-- 25. Colonnes table EMPLOYEES (dictionnaire)
-- SELECT column_name, data_type, nullable FROM user_tab_columns WHERE table_name = 'EMPLOYEES';

-- 26. Contraintes EMPLOYEES
-- SELECT constraint_name, constraint_type FROM user_constraints WHERE table_name = 'EMPLOYEES';

-- 27. Employés sans manager
SELECT last_name FROM employees WHERE manager_id IS NULL;

-- 28. NOT IN vs NULL (piège)
SELECT last_name FROM employees WHERE department_id NOT IN (10, 20, NULL); -- retourne 0 lignes!

-- 29. GROUP BY avec HAVING count
SELECT department_id, AVG(salary) FROM employees GROUP BY department_id HAVING COUNT(*) >= 5;

-- 30. NATURAL JOIN (attention colonnes communes)
-- SELECT * FROM employees NATURAL JOIN departments; -- joint sur department_id si nom identique

-- Requêtes 31-50 : révisions examen
-- 31. ADD_MONTHS
SELECT last_name, hire_date, ADD_MONTHS(hire_date, 6) AS fin_essai FROM employees WHERE ROWNUM <= 5;

-- 32. MONTHS_BETWEEN
SELECT last_name, ROUND(MONTHS_BETWEEN(SYSDATE, hire_date), 0) AS mois_service FROM employees WHERE ROWNUM <= 5;

-- 33. TRUNC date
SELECT TRUNC(SYSDATE, 'MM') AS debut_mois FROM dual;

-- 34. SUBSTR + INSTR
SELECT email, SUBSTR(email, 1, INSTR(email, '@') - 1) AS user_part FROM employees WHERE ROWNUM <= 5;

-- 35. COALESCE
SELECT last_name, COALESCE(commission_pct, 0, 0.1) FROM employees WHERE ROWNUM <= 5;

-- 36. NULLIF
SELECT NULLIF(salary, 0) FROM employees WHERE ROWNUM <= 5;

-- 37. LAG/LEAD
SELECT last_name, salary, LAG(salary) OVER (ORDER BY employee_id) AS prec FROM employees WHERE ROWNUM <= 10;

-- 38. FIRST_VALUE
SELECT department_id, last_name, salary,
       FIRST_VALUE(last_name) OVER (PARTITION BY department_id ORDER BY salary DESC) AS top_paid
FROM employees;

-- 39. CROSS JOIN count
SELECT COUNT(*) FROM employees CROSS JOIN departments; -- produit cartésien

-- 40. MINUS
SELECT job_id FROM employees MINUS SELECT job_id FROM jobs WHERE max_salary < 3000;

-- 41. ROWNUM avec sous-requête ordonnée
SELECT last_name, salary FROM (
  SELECT last_name, salary, ROWNUM AS rn FROM (
    SELECT last_name, salary FROM employees ORDER BY salary DESC
  ) WHERE ROWNUM <= 10
) WHERE rn > 5;

-- 42. DISTINCT + ORDER BY
SELECT DISTINCT department_id FROM employees ORDER BY department_id;

-- 43. Alias dans ORDER BY
SELECT last_name, salary * 12 AS annuel FROM employees ORDER BY annuel DESC FETCH FIRST 5 ROWS ONLY;

-- 44. WHERE vs HAVING
SELECT department_id, AVG(salary) FROM employees WHERE salary > 3000 GROUP BY department_id HAVING AVG(salary) > 6000;

-- 45. JOIN USING
-- SELECT * FROM employees JOIN departments USING (department_id);

-- 46. FULL OUTER JOIN
SELECT e.last_name, d.department_name FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.department_id;

-- 47. Scalar subquery in SELECT
SELECT last_name, salary, (SELECT ROUND(AVG(salary), 2) FROM employees) AS moy_globale FROM employees WHERE ROWNUM <= 5;

-- 48. Correlated subquery
SELECT e.last_name, e.salary FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.department_id = e.department_id);

-- 49. ANY operator
SELECT last_name FROM employees WHERE salary > ANY (SELECT salary FROM employees WHERE department_id = 30);

-- 50. ALL operator
SELECT last_name FROM employees WHERE salary > ALL (SELECT salary FROM employees WHERE department_id = 30);

PROMPT 50 requêtes d entraînement prêtes.
