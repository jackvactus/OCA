-- ============================================================
-- Schéma HR simplifié pour Oracle Database SQL 1Z0-071
-- Formation Oracle - Scripts téléchargeables
-- ============================================================

-- Suppression si existant (ordre inverse des FK)
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE employees CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE departments CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE jobs CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE locations CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE countries CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE regions CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- Régions
CREATE TABLE regions (
  region_id   NUMBER(5) PRIMARY KEY,
  region_name VARCHAR2(50) NOT NULL
);

-- Pays
CREATE TABLE countries (
  country_id   CHAR(2) PRIMARY KEY,
  country_name VARCHAR2(50) NOT NULL,
  region_id    NUMBER(5) REFERENCES regions(region_id)
);

-- Localisations
CREATE TABLE locations (
  location_id    NUMBER(4) PRIMARY KEY,
  street_address VARCHAR2(100),
  postal_code    VARCHAR2(20),
  city           VARCHAR2(50) NOT NULL,
  state_province VARCHAR2(50),
  country_id     CHAR(2) REFERENCES countries(country_id)
);

-- Départements
CREATE TABLE departments (
  department_id   NUMBER(4) PRIMARY KEY,
  department_name VARCHAR2(50) NOT NULL,
  manager_id      NUMBER(6),
  location_id     NUMBER(4) REFERENCES locations(location_id)
);

-- Métiers
CREATE TABLE jobs (
  job_id     VARCHAR2(10) PRIMARY KEY,
  job_title  VARCHAR2(50) NOT NULL,
  min_salary NUMBER(8),
  max_salary NUMBER(8)
);

-- Employés
CREATE TABLE employees (
  employee_id    NUMBER(6) PRIMARY KEY,
  first_name     VARCHAR2(20),
  last_name      VARCHAR2(25) NOT NULL,
  email          VARCHAR2(25) NOT NULL UNIQUE,
  phone_number   VARCHAR2(20),
  hire_date      DATE NOT NULL,
  job_id         VARCHAR2(10) NOT NULL REFERENCES jobs(job_id),
  salary         NUMBER(8,2),
  commission_pct NUMBER(2,2),
  manager_id     NUMBER(6),
  department_id  NUMBER(4) REFERENCES departments(department_id),
  CONSTRAINT emp_salary_min CHECK (salary > 0),
  CONSTRAINT emp_commission CHECK (commission_pct BETWEEN 0 AND 1 OR commission_pct IS NULL)
);

-- FK manager (self-reference)
ALTER TABLE employees ADD CONSTRAINT emp_manager_fk
  FOREIGN KEY (manager_id) REFERENCES employees(employee_id);

ALTER TABLE departments ADD CONSTRAINT dept_manager_fk
  FOREIGN KEY (manager_id) REFERENCES employees(employee_id);

-- Index pour performance
CREATE INDEX idx_emp_dept ON employees(department_id);
CREATE INDEX idx_emp_job ON employees(job_id);
CREATE INDEX idx_emp_manager ON employees(manager_id);

-- Séquence pour nouveaux employés
CREATE SEQUENCE emp_seq START WITH 1000 INCREMENT BY 1 NOCACHE;

-- Vue lecture seule
CREATE OR REPLACE VIEW v_emp_dept AS
SELECT e.employee_id, e.last_name, e.first_name, e.salary,
       d.department_name, j.job_title
FROM   employees e
JOIN   departments d ON e.department_id = d.department_id
JOIN   jobs j ON e.job_id = j.job_id
WITH READ ONLY;

PROMPT Schéma HR créé avec succès.
