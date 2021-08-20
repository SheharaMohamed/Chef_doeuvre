CREATE DATABASE IF NOT EXISTS emploi;
USE emploi;

#----------------------------------------#
		       ###Année###
#----------------------------------------#
CREATE TABLE année(
    année INT PRIMARY KEY
);

#----------------------------------------#
	  ###Type characteristic###
#----------------------------------------#
CREATE TABLE type_char(
    typ_id VARCHAR(6) PRIMARY KEY,
    type_characteristique VARCHAR(100)
);

#----------------------------------------#
	  ###Characteristic d'emploi###
#----------------------------------------#
CREATE TABLE char_demploi(
    cha_id VARCHAR(6) PRIMARY KEY,
    characteristique VARCHAR(200),
    typ_id VARCHAR(6),
    FOREIGN KEY (typ_id) REFERENCES type_char(typ_id)
);

#----------------------------------------#
			###Diplome###
#----------------------------------------#
CREATE TABLE diplôme(
	dip_id VARCHAR(6) PRIMARY KEY,
	diplôme VARCHAR(100)
);

#----------------------------------------#
			###Catégorie###
#----------------------------------------#
CREATE TABLE catégorie(
    cat_id VARCHAR(6) PRIMARY KEY,
    catégorie VARCHAR(100)
);

#----------------------------------------#
			###Population###
#----------------------------------------#
CREATE TABLE population(
    pop_id VARCHAR(6) PRIMARY KEY,
    group_dage VARCHAR(25),
    sexe VARCHAR(10)
);

#----------------------------------------#
			 ###Pays###
#----------------------------------------#
CREATE TABLE pays(
    code_pays VARCHAR(6) PRIMARY KEY,
    pays VARCHAR(100)
);

#----------------------------------------#
			  ###Région###
#----------------------------------------#
CREATE TABLE région(
    code_reg VARCHAR(6) PRIMARY KEY,
    region VARCHAR(100),
    code_pays VARCHAR(6),
    FOREIGN KEY (code_pays) REFERENCES pays(code_pays)
);

#----------------------------------------#
			###Departement###
#----------------------------------------#
CREATE TABLE departement(
    code_postal VARCHAR(5) PRIMARY KEY,
    departement VARCHAR(100),
    code_reg VARCHAR(6),
    FOREIGN KEY (code_reg) REFERENCES région(code_reg)
);

#----------------------------------------#
###Indicateur characteristics d'emploi###
#----------------------------------------#
CREATE TABLE indicateur_chardemploi(
    année int,
    pop_id VARCHAR(6),
    cha_id VARCHAR(6),
    nombre_employe FLOAT,
    FOREIGN KEY (pop_id) REFERENCES population(pop_id),
    FOREIGN KEY (année) REFERENCES année(année),
    FOREIGN KEY (cha_id) REFERENCES char_demploi(cha_id),
    PRIMARY KEY (pop_id,année,cha_id)
);

#----------------------------------------#
		###Indicateur catégorie###
#----------------------------------------#
CREATE TABLE indicateur_catégorie(    
    année int,
    pop_id VARCHAR(6),
    cat_id VARCHAR(6),
    nombre_employe FLOAT,
    nombre_chomeur FLOAT,
    FOREIGN KEY (pop_id) REFERENCES population(pop_id),
    FOREIGN KEY (année) REFERENCES année(année),
    FOREIGN KEY (cat_id) REFERENCES catégorie(cat_id),
    PRIMARY KEY (pop_id,année,cat_id)
);

#----------------------------------------#
		###Indicateur diplôme###
#----------------------------------------#
CREATE TABLE indicateur_diplôme(
    année int,
    pop_id VARCHAR(6),
    dip_id VARCHAR(6),
    nombre_employe FLOAT,
    nombre_chomeur FLOAT,
    FOREIGN KEY (pop_id) REFERENCES population(pop_id),
    FOREIGN KEY (année) REFERENCES année(année),
    FOREIGN KEY (dip_id) REFERENCES diplôme(dip_id),
    PRIMARY KEY (pop_id,année,dip_id)
);

#----------------------------------------#
	  ###Indicateur departement###
#----------------------------------------#
CREATE TABLE indicateur_departement(
    année int,
    pop_id VARCHAR(6),
    code_postal VARCHAR(6),
    population FLOAT,
    nombre_chomeur FLOAT,    
    salaire_moyen FLOAT,
    FOREIGN KEY (pop_id) REFERENCES population(pop_id),
    FOREIGN KEY (année) REFERENCES année(année),
    FOREIGN KEY (code_postal) REFERENCES departement(code_postal),
    PRIMARY KEY (pop_id,année,code_postal)
);