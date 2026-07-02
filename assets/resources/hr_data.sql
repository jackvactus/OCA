-- ============================================================
-- Données exemple HR simplifiées - Oracle 1Z0-071
-- Exécuter après hr_schema.sql
-- ============================================================

-- Régions
INSERT INTO regions VALUES (1, 'Europe');
INSERT INTO regions VALUES (2, 'Amériques');
INSERT INTO regions VALUES (3, 'Asie');
INSERT INTO regions VALUES (4, 'Moyen-Orient et Afrique');

-- Pays
INSERT INTO countries VALUES ('FR', 'France', 1);
INSERT INTO countries VALUES ('US', 'États-Unis', 2);
INSERT INTO countries VALUES ('UK', 'Royaume-Uni', 1);
INSERT INTO countries VALUES ('DE', 'Allemagne', 1);

-- Localisations
INSERT INTO locations VALUES (1700, '2 rue de la Paix', '75002', 'Paris', NULL, 'FR');
INSERT INTO locations VALUES (1800, '147 Spadina Ave', 'M5V 2L7', 'Toronto', 'Ontario', 'US');
INSERT INTO locations VALUES (2400, '8200 Jones Rd', '26155', 'London', NULL, 'UK');
INSERT INTO locations VALUES (2500, 'Marlene-Dietrich-Platz 1', '10785', 'Berlin', NULL, 'DE');

-- Métiers
INSERT INTO jobs VALUES ('AD_PRES', 'President', 20000, 40000);
INSERT INTO jobs VALUES ('AD_VP', 'Administration Vice President', 15000, 30000);
INSERT INTO jobs VALUES ('IT_PROG', 'Programmer', 4000, 10000);
INSERT INTO jobs VALUES ('SA_REP', 'Sales Representative', 6000, 12000);
INSERT INTO jobs VALUES ('SA_MAN', 'Sales Manager', 10000, 20000);
INSERT INTO jobs VALUES ('HR_REP', 'Human Resources Representative', 4000, 9000);
INSERT INTO jobs VALUES ('FI_ACCOUNT', 'Accountant', 4200, 9000);
INSERT INTO jobs VALUES ('ST_CLERK', 'Stock Clerk', 2000, 5000);
INSERT INTO jobs VALUES ('ST_MAN', 'Stock Manager', 5500, 8500);
INSERT INTO jobs VALUES ('PU_MAN', 'Purchasing Manager', 8000, 15000);
INSERT INTO jobs VALUES ('PU_CLERK', 'Purchasing Clerk', 2500, 5500);
INSERT INTO jobs VALUES ('AD_ASST', 'Administration Assistant', 3000, 6000);
INSERT INTO jobs VALUES ('MK_MAN', 'Marketing Manager', 9000, 15000);
INSERT INTO jobs VALUES ('MK_REP', 'Marketing Representative', 4000, 9000);
INSERT INTO jobs VALUES ('PR_REP', 'Public Relations Representative', 4500, 10500);
INSERT INTO jobs VALUES ('AC_MGR', 'Accounting Manager', 8200, 16000);
INSERT INTO jobs VALUES ('AC_ACCOUNT', 'Accountant', 4200, 9000);

-- Départements
INSERT INTO departments VALUES (10, 'Administration', NULL, 1700);
INSERT INTO departments VALUES (20, 'Marketing', NULL, 1800);
INSERT INTO departments VALUES (30, 'Purchasing', NULL, 1700);
INSERT INTO departments VALUES (40, 'Human Resources', NULL, 2400);
INSERT INTO departments VALUES (50, 'Shipping', NULL, 2500);
INSERT INTO departments VALUES (60, 'IT', NULL, 1700);
INSERT INTO departments VALUES (70, 'Public Relations', NULL, 1800);
INSERT INTO departments VALUES (80, 'Sales', NULL, 2500);
INSERT INTO departments VALUES (90, 'Executive', NULL, 1700);
INSERT INTO departments VALUES (100, 'Finance', NULL, 1700);

-- Employés (échantillon représentatif)
INSERT INTO employees VALUES (100, 'Steven', 'King', 'SKING', '515.123.4567', DATE '2003-06-17', 'AD_PRES', 24000, NULL, NULL, 90);
INSERT INTO employees VALUES (101, 'Neena', 'Kochhar', 'NKOCHHAR', '515.123.4568', DATE '2005-09-21', 'AD_VP', 17000, NULL, 100, 90);
INSERT INTO employees VALUES (102, 'Lex', 'De Haan', 'LDEHAAN', '515.123.4569', DATE '2001-01-13', 'AD_VP', 17000, NULL, 100, 90);
INSERT INTO employees VALUES (103, 'Alexander', 'Hunold', 'AHUNOLD', '590.423.4567', DATE '2006-01-03', 'IT_PROG', 9000, NULL, 102, 60);
INSERT INTO employees VALUES (104, 'Bruce', 'Ernst', 'BERNST', '590.423.4568', DATE '2007-05-21', 'IT_PROG', 6000, NULL, 103, 60);
INSERT INTO employees VALUES (105, 'David', 'Austin', 'DAUSTIN', '590.423.4569', DATE '2005-06-25', 'IT_PROG', 4800, NULL, 103, 60);
INSERT INTO employees VALUES (106, 'Valli', 'Pataballa', 'VPATABAL', '590.423.4560', DATE '2006-02-05', 'IT_PROG', 4800, NULL, 103, 60);
INSERT INTO employees VALUES (107, 'Diana', 'Lorentz', 'DLORENTZ', '590.423.5567', DATE '2007-02-07', 'IT_PROG', 4200, NULL, 103, 60);
INSERT INTO employees VALUES (108, 'Nancy', 'Greenberg', 'NGREENBE', '515.124.4569', DATE '2002-08-17', 'FI_ACCOUNT', 12000, NULL, 101, 100);
INSERT INTO employees VALUES (109, 'Daniel', 'Faviet', 'DFAVIET', '515.124.4169', DATE '2002-08-16', 'FI_ACCOUNT', 9000, NULL, 108, 100);
INSERT INTO employees VALUES (110, 'John', 'Chen', 'JCHEN', '515.124.4269', DATE '2005-09-28', 'FI_ACCOUNT', 8200, NULL, 108, 100);
INSERT INTO employees VALUES (114, 'Den', 'Raphaely', 'DRAPHEAL', '515.127.4561', DATE '2002-12-07', 'PU_MAN', 11000, NULL, 100, 30);
INSERT INTO employees VALUES (115, 'Alexander', 'Khoo', 'AKHOO', '515.127.4562', DATE '2003-05-18', 'PU_CLERK', 3100, NULL, 114, 30);
INSERT INTO employees VALUES (116, 'Shelli', 'Baida', 'SBAIDA', '515.127.4563', DATE '2005-12-24', 'PU_CLERK', 2900, NULL, 114, 30);
INSERT INTO employees VALUES (117, 'Sigal', 'Tobias', 'STOBIAS', '515.127.4564', DATE '2005-07-24', 'PU_CLERK', 2800, NULL, 114, 30);
INSERT INTO employees VALUES (118, 'Guy', 'Himuro', 'GHIMURO', '515.127.4565', DATE '2006-11-15', 'PU_CLERK', 2600, NULL, 114, 30);
INSERT INTO employees VALUES (119, 'Karen', 'Colmenares', 'KCOLMENA', '515.127.4566', DATE '2007-08-10', 'PU_CLERK', 2500, NULL, 114, 30);
INSERT INTO employees VALUES (120, 'Matthew', 'Weiss', 'MWEISS', '650.123.1234', DATE '2004-07-18', 'ST_MAN', 8000, NULL, 100, 50);
INSERT INTO employees VALUES (121, 'Adam', 'Fripp', 'AFRIPP', '650.123.2234', DATE '2005-04-10', 'ST_MAN', 8200, NULL, 100, 50);
INSERT INTO employees VALUES (122, 'Payam', 'Kaufling', 'PKAUFLIN', '650.123.2234', DATE '2003-05-01', 'ST_MAN', 7900, NULL, 100, 50);
INSERT INTO employees VALUES (123, 'Shanta', 'Vollman', 'SVOLLMAN', '650.123.4234', DATE '2005-10-10', 'ST_MAN', 6500, NULL, 100, 50);
INSERT INTO employees VALUES (124, 'Kevin', 'Mourgos', 'KMOURGOS', '650.123.2874', DATE '2007-11-16', 'ST_MAN', 5800, NULL, 100, 50);
INSERT INTO employees VALUES (125, 'Julia', 'Nayer', 'JNAYER', '650.124.1214', DATE '2005-01-16', 'ST_CLERK', 3200, NULL, 120, 50);
INSERT INTO employees VALUES (126, 'Irene', 'Mikkilineni', 'IMIKKILI', '650.124.1224', DATE '2006-09-28', 'ST_CLERK', 2700, NULL, 120, 50);
INSERT INTO employees VALUES (127, 'James', 'Landry', 'JLANDRY', '650.124.1334', DATE '2007-01-14', 'ST_CLERK', 2400, NULL, 120, 50);
INSERT INTO employees VALUES (128, 'Steven', 'Markle', 'SMARKLE', '650.124.1434', DATE '2008-03-08', 'ST_CLERK', 2200, NULL, 120, 50);
INSERT INTO employees VALUES (129, 'Laura', 'Bissot', 'LBISSOT', '650.124.5234', DATE '2005-08-20', 'ST_CLERK', 3300, NULL, 121, 50);
INSERT INTO employees VALUES (130, 'Mozhe', 'Atkinson', 'MATKINSO', '650.124.6234', DATE '2005-10-30', 'ST_CLERK', 2800, NULL, 121, 50);
INSERT INTO employees VALUES (145, 'John', 'Russell', 'JRUSSEL', '011.44.1344.429268', DATE '2004-10-01', 'SA_MAN', 14000, 0.4, 100, 80);
INSERT INTO employees VALUES (146, 'Karen', 'Partners', 'KPARTNER', '011.44.1343.467268', DATE '2005-01-05', 'SA_MAN', 13500, 0.3, 100, 80);
INSERT INTO employees VALUES (147, 'Alberto', 'Errazuriz', 'AERRAZUR', '011.44.1344.429278', DATE '2005-03-10', 'SA_MAN', 12000, 0.3, 100, 80);
INSERT INTO employees VALUES (148, 'Gerald', 'Cambrault', 'GCAMBRAU', '011.44.1344.619268', DATE '2007-10-15', 'SA_MAN', 11000, 0.3, 100, 80);
INSERT INTO employees VALUES (149, 'Eleni', 'Zlotkey', 'EZLOTKEY', '011.44.1344.429018', DATE '2008-01-29', 'SA_MAN', 10500, 0.2, 100, 80);
INSERT INTO employees VALUES (150, 'Peter', 'Tucker', 'PTUCKER', '011.44.1344.129268', DATE '2005-01-30', 'SA_REP', 10000, 0.3, 145, 80);
INSERT INTO employees VALUES (151, 'David', 'Bernstein', 'DBERNSTE', '011.44.1343.345268', DATE '2005-03-24', 'SA_REP', 9500, 0.25, 145, 80);
INSERT INTO employees VALUES (152, 'Peter', 'Hall', 'PHALL', '011.44.1344.478968', DATE '2005-08-20', 'SA_REP', 9000, 0.25, 145, 80);
INSERT INTO employees VALUES (153, 'Christopher', 'Olsen', 'COLSEN', '011.44.1344.498718', DATE '2006-03-30', 'SA_REP', 8000, 0.2, 145, 80);
INSERT INTO employees VALUES (154, 'Nanette', 'Cambrault', 'NCAMBRAU', '011.44.1344.987668', DATE '2007-12-09', 'SA_REP', 7500, 0.2, 145, 80);
INSERT INTO employees VALUES (155, 'Oliver', 'Tuvault', 'OTUVAULT', '011.44.1344.486508', DATE '2007-11-23', 'SA_REP', 7000, 0.15, 145, 80);
INSERT INTO employees VALUES (156, 'Janette', 'King', 'JKING', '011.44.1345.429268', DATE '2004-01-30', 'SA_REP', 10000, 0.35, 146, 80);
INSERT INTO employees VALUES (157, 'Patrick', 'Sully', 'PSULLY', '011.44.1345.929268', DATE '2004-03-04', 'SA_REP', 9500, 0.35, 146, 80);
INSERT INTO employees VALUES (158, 'Allan', 'McEwen', 'AMCEWEN', '011.44.1345.829268', DATE '2004-08-01', 'SA_REP', 9000, 0.35, 146, 80);
INSERT INTO employees VALUES (159, 'Lindsey', 'Smith', 'LSMITH', '011.44.1345.729268', DATE '2005-03-10', 'SA_REP', 8000, 0.3, 146, 80);
INSERT INTO employees VALUES (160, 'Louise', 'Doran', 'LDORAN', '011.44.1345.631268', DATE '2007-12-15', 'SA_REP', 7500, 0.3, 146, 80);
INSERT INTO employees VALUES (161, 'Sarath', 'Sewall', 'SSEWALL', '011.44.1345.471268', DATE '2006-11-03', 'SA_REP', 7000, 0.25, 146, 80);
INSERT INTO employees VALUES (162, 'Clara', 'Vishney', 'CVISHNEY', '011.44.1346.129268', DATE '2005-11-11', 'SA_REP', 10500, 0.25, 147, 80);
INSERT INTO employees VALUES (163, 'Danielle', 'Greene', 'DGREENE', '011.44.1346.229268', DATE '2007-03-19', 'SA_REP', 9500, 0.15, 147, 80);
INSERT INTO employees VALUES (164, 'Mattea', 'Marvins', 'MMARVINS', '011.44.1346.329268', DATE '2008-01-24', 'SA_REP', 7200, 0.1, 147, 80);
INSERT INTO employees VALUES (165, 'David', 'Lee', 'DLEE', '011.44.1346.529268', DATE '2008-02-23', 'SA_REP', 6800, 0.1, 147, 80);
INSERT INTO employees VALUES (166, 'Sundar', 'Ande', 'SANDE', '011.44.1346.629268', DATE '2008-03-24', 'SA_REP', 6400, 0.1, 147, 80);
INSERT INTO employees VALUES (167, 'Amit', 'Banda', 'ABANDA', '011.44.1346.729268', DATE '2008-04-21', 'SA_REP', 6200, 0.1, 147, 80);
INSERT INTO employees VALUES (168, 'Lisa', 'Ozer', 'LOZER', '515.124.4569', DATE '2005-03-11', 'SA_REP', 11500, 0.25, 148, 80);
INSERT INTO employees VALUES (169, 'Harrison', 'Bloom', 'HBLOOM', '011.44.1346.829268', DATE '2006-03-23', 'SA_REP', 10000, 0.2, 148, 80);
INSERT INTO employees VALUES (170, 'Tayler', 'Fox', 'TFOX', '011.44.1346.929268', DATE '2006-01-24', 'SA_REP', 9600, 0.2, 148, 80);
INSERT INTO employees VALUES (171, 'William', 'Smith', 'WSMITH', '011.44.1347.029268', DATE '2007-02-23', 'SA_REP', 7400, 0.15, 148, 80);
INSERT INTO employees VALUES (172, 'Elizabeth', 'Bates', 'EBATES', '011.44.1347.129268', DATE '2007-03-24', 'SA_REP', 7300, 0.15, 148, 80);
INSERT INTO employees VALUES (173, 'Sundita', 'Kumar', 'SKUMAR', '011.44.1343.329268', DATE '2008-04-21', 'SA_REP', 6100, 0.1, 148, 80);
INSERT INTO employees VALUES (174, 'Ellen', 'Abel', 'EABEL', '011.44.1644.429267', DATE '2004-05-11', 'SA_REP', 11000, 0.3, 149, 80);
INSERT INTO employees VALUES (175, 'Alyssa', 'Hutton', 'AHUTTON', '011.44.1644.429267', DATE '2005-03-19', 'SA_REP', 8800, 0.25, 149, 80);
INSERT INTO employees VALUES (176, 'Jonathon', 'Taylor', 'JTAYLOR', '011.44.1644.429267', DATE '2006-03-24', 'SA_REP', 8600, 0.2, 149, 80);
INSERT INTO employees VALUES (177, 'Jack', 'Livingston', 'JLIVINGS', '011.44.1644.429267', DATE '2006-04-23', 'SA_REP', 8400, 0.2, 149, 80);
INSERT INTO employees VALUES (178, 'Kimberly', 'Grant', 'KGRANT', '011.44.1644.429267', DATE '2007-05-24', 'SA_REP', 7000, 0.15, 149, 80);
INSERT INTO employees VALUES (179, 'Charles', 'Johnson', 'CJOHNSON', '011.44.1644.429267', DATE '2008-01-04', 'SA_REP', 6200, 0.1, 149, 80);
INSERT INTO employees VALUES (200, 'Jennifer', 'Whalen', 'JWHALEN', '515.123.4444', DATE '2003-09-17', 'AD_ASST', 4400, NULL, 101, 10);
INSERT INTO employees VALUES (201, 'Michael', 'Hartstein', 'MHARTSTE', '515.123.5555', DATE '2004-02-17', 'MK_MAN', 13000, NULL, 100, 20);
INSERT INTO employees VALUES (202, 'Pat', 'Fay', 'PFAY', '603.123.6666', DATE '2005-08-17', 'MK_REP', 6000, NULL, 201, 20);
INSERT INTO employees VALUES (203, 'Susan', 'Mavris', 'SMAVRIS', '515.123.7777', DATE '2002-06-07', 'HR_REP', 6500, NULL, 101, 40);
INSERT INTO employees VALUES (204, 'Hermann', 'Baer', 'HBAER', '515.123.8888', DATE '2002-06-07', 'PR_REP', 10000, NULL, 101, 70);
INSERT INTO employees VALUES (205, 'Shelley', 'Higgins', 'SHIGGINS', '515.123.8080', DATE '2002-06-07', 'AC_MGR', 12000, NULL, 101, 100);
INSERT INTO employees VALUES (206, 'William', 'Gietz', 'WGIETZ', '515.123.8181', DATE '2002-06-07', 'AC_ACCOUNT', 8300, NULL, 205, 100);

-- Mise à jour managers départements
UPDATE departments SET manager_id = 200 WHERE department_id = 10;
UPDATE departments SET manager_id = 201 WHERE department_id = 20;
UPDATE departments SET manager_id = 114 WHERE department_id = 30;
UPDATE departments SET manager_id = 203 WHERE department_id = 40;
UPDATE departments SET manager_id = 121 WHERE department_id = 50;
UPDATE departments SET manager_id = 103 WHERE department_id = 60;
UPDATE departments SET manager_id = 204 WHERE department_id = 70;
UPDATE departments SET manager_id = 145 WHERE department_id = 80;
UPDATE departments SET manager_id = 100 WHERE department_id = 90;
UPDATE departments SET manager_id = 108 WHERE department_id = 100;

COMMIT;
PROMPT Données HR insérées avec succès.
