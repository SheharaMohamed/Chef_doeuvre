SELECT c.catégorie, p.* FROM année a
	        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_catégorie USING (pop_id)) p USING (année)
            INNER JOIN catégorie c USING (cat_id)
            ORDER BY p.année;

SELECT c.characteristique, p.*, t.* FROM année a
	        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_chardemploi USING (pop_id)) p USING (année)
            INNER JOIN char_demploi c USING (cha_id)
            INNER JOIN type_char t USING (typ_id)
            ORDER BY p.année;
SHOW VARIABLES LIKE "secure_file_priv";

SELECT d.departement, r.region, p.* FROM année a
	        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_departement USING (pop_id)) p USING (année)
            INNER JOIN departement d USING (code_postal)
            INNER JOIN région r USING (code_reg)
            ORDER BY p.année;

#Backup
SHOW VARIABLES LIKE "secure_file_priv";
SELECT 'année'
UNION ALL
SELECT * FROM année
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/année.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY ''
LINES TERMINATED BY '\n';

SET @TS = DATE_FORMAT(NOW(),'_%Y_%m_%d_%H_%i_%s');

SET @FOLDER = 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/';
SET @PREFIX = 'indicateur_departement';
SET @EXT    = '.csv';
SET @CMD = CONCAT("
SELECT 'departement','region','pop_id','group_dage','sexe','année','code_postal','population','nombre_chomeur','salaire_moyen'
UNION ALL 
SELECT d.departement, r.region, p.* FROM année a
	        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_departement USING (pop_id)) p USING (année)
            INNER JOIN departement d USING (code_postal)
            INNER JOIN région r USING (code_reg)
INTO OUTFILE '",@FOLDER,@PREFIX,@TS,@EXT,
				   "' FIELDS ENCLOSED BY '\"' TERMINATED BY ';' ESCAPED BY '\"'",
				   "  LINES TERMINATED BY '\r\n';");
PREPARE statement FROM @CMD;
EXECUTE statement;

SELECT 'année'
UNION
SELECT *
FROM année
INTO OUTFILE @VAR
FIELDS ENCLOSED BY '"' TERMINATED BY ';' ESCAPED BY '"'
LINES TERMINATED BY '\r\n';


SELECT d.departement, r.code_reg, r.region, p.* FROM année a
	        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_departement USING (pop_id)) p USING (année)
            INNER JOIN departement d USING (code_postal)
            INNER JOIN région r USING (code_reg)
            ORDER BY p.année;
            
Drop table population;

SELECT pop_id FROM population WHERE group_dage = 'T15' AND sexe = 'F';

#Total emplois vs chomeurs

SELECT * FROM 
	(SELECT a.année, SUM(i.nombre_employe)*1000 AS nombre_employe ,SUM(i.nombre_chomeur)*1000 AS nombre_chomeur FROM année a
				INNER JOIN indicateur_diplôme i USING (année)
				GROUP BY a.année
				ORDER BY a.année) AS A
INNER JOIN 
	(SELECT a.année, SUM(p.population*1000) AS population FROM année a
				INNER JOIN (SELECT * FROM population INNER JOIN indicateur_departement USING (pop_id)) p USING (année)  
                WHERE p.group_dage != 'T0'
				GROUP BY a.année
				ORDER BY a.année) AS B
USING (année);

SELECT a.année, SUM(p.population*1000) AS population FROM année a
				INNER JOIN (SELECT * FROM population INNER JOIN indicateur_departement USING (pop_id)) p USING (année)  
                WHERE p.group_dage != 'T0'
				GROUP BY a.année
				ORDER BY a.année;

SELECT * FROM population INNER JOIN indicateur_departement USING (pop_id);
#Par diplôme par année            
SELECT a.année, d.diplôme, SUM(p.nombre_employe)*1000 AS nombre_employe ,SUM(p.nombre_chomeur)*1000 AS nombre_chomeur 
			FROM année a
            INNER JOIN (SELECT * FROM population INNER JOIN indicateur_diplôme USING (pop_id)) p USING (année)
            INNER JOIN diplôme d USING (dip_id)
            GROUP BY a.année, d.diplôme
            ORDER BY a.année;
            
SELECT a.année, d.diplôme, p.sexe, p.group_dage, p.nombre_employe*1000 , p.nombre_chomeur*1000
			FROM année a
            INNER JOIN (SELECT * FROM population INNER JOIN indicateur_diplôme USING (pop_id)) p USING (année)
            INNER JOIN diplôme d USING (dip_id)
            HAVING a.année = 2019
            ORDER BY a.année;
            
#La catégorie socioprofessionelle
SELECT a.année, c.catégorie, SUM(i.nombre_employe)*1000 AS nombre_employe ,SUM(i.nombre_chomeur)*1000 AS nombre_chomeur 
			FROM année a
            INNER JOIN indicateur_catégorie i USING (année)
            INNER JOIN catégorie c USING (cat_id)
            GROUP BY a.année, c.catégorie
            ORDER BY a.année;
            
SELECT a.année, c.catégorie, SUM(i.nombre_employe)*1000 AS nombre_employe ,SUM(i.nombre_chomeur)*1000 AS nombre_chomeur 
			FROM année a
            INNER JOIN indicateur_catégorie i USING (année)
            INNER JOIN catégorie c USING (cat_id)
            GROUP BY a.année, c.catégorie
            HAVING c.catégorie LIKE '%Agriculteurs%'
            ORDER BY a.année;
            
SELECT a.année, p.sexe, p.group_dage, c.characteristique, p.nombre_employe FROM année a
            INNER JOIN (SELECT * FROM population INNER JOIN indicateur_chardemploi USING (pop_id)) p USING (année)
            INNER JOIN char_demploi c USING (cha_id)
            INNER JOIN type_char t USING (typ_id)
            WHERE c.characteristique LIKE 'temp%' AND a.année >2015
            ORDER BY p.année;
            
#Géographie
SELECT a.année, d.code_postal, d.departement, SUM(i.population*1000) AS population, SUM(i.nombre_chomeur) AS nombre_chomeur, 
			ROUND(AVG(i.salaire_moyen),2) AS salaire_moyen FROM année a
            INNER JOIN indicateur_departement i USING (année)
            INNER JOIN departement d USING (code_postal)
            WHERE a.année = 2018
            GROUP BY d.departement
            ORDER BY a.année;
            
SELECT a.année, r.code_reg, r.region, SUM(i.population*1000) AS population, SUM(i.nombre_chomeur) AS nombre_chomeur, 
			ROUND(AVG(i.salaire_moyen),2) AS salaire_moyen FROM année a
            INNER JOIN indicateur_departement i USING (année)
            INNER JOIN departement d USING (code_postal)
            INNER JOIN région r USING (code_reg)            
            WHERE a.année = 2018
            GROUP BY r.region
            ORDER BY a.année;