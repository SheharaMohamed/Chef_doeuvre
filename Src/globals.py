from sqlalchemy import create_engine
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

engine = create_engine(
    "mysql+pymysql://admin:tashe1129@rds-first.c9xhdrdycaeq.eu-west-3.rds.amazonaws.com/emploi?charset=utf8mb4&binary_prefix=true")


conn = engine.connect()


q_cat = '''SELECT c.catégorie, p.* FROM année a
        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_catégorie USING (pop_id)) p USING (année)
        INNER JOIN catégorie c USING (cat_id)
        ORDER BY p.année;'''

q_cha = '''SELECT c.characteristique, p.*, t.* FROM année a
        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_chardemploi USING (pop_id)) p USING (année)
        INNER JOIN char_demploi c USING (cha_id)
        INNER JOIN type_char t USING (typ_id)
        ORDER BY p.année;'''

q_geo = '''SELECT d.departement, r.code_reg, r.region, p.* FROM année a
        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_departement USING (pop_id)) p USING (année)
        INNER JOIN departement d USING (code_postal)
        INNER JOIN région r USING (code_reg)
        ORDER BY p.année;'''

q_dip = '''SELECT d.diplôme, p.* FROM année a
        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_diplôme USING (pop_id)) p USING (année)
        INNER JOIN diplôme d USING (dip_id)
        ORDER BY p.année;'''

if conn:
        df_dip = pd.read_sql(q_dip, conn)
        df_geo = pd.read_sql(q_geo, conn)
        df_cha = pd.read_sql(q_cha, conn)
        df_cat = pd.read_sql(q_cat, conn)

else:
        df_dip = pd.read_csv("data/indicateur_diplôme.csv")
        df_geo = pd.read_csv("data/indicateur_departement.csv")
        df_cha = pd.read_csv("data/indicateur_caratéristique.csv")
        df_cat = pd.read_csv("data/indicateur_catégorie.csv")

q = '''SELECT * FROM 
	(SELECT a.année, SUM(i.nombre_employe)*1000 AS nombre_employe ,SUM(i.nombre_chomeur)*1000 AS nombre_chomeur FROM année a
				INNER JOIN indicateur_diplôme i USING (année)
				GROUP BY a.année
				ORDER BY a.année) AS A
INNER JOIN 
	(SELECT a.année, SUM(p.population) AS population FROM année a
				INNER JOIN (SELECT * FROM population INNER JOIN indicateur_departement USING (pop_id)) p USING (année)  
                WHERE p.group_dage NOT IN ('T0')
				GROUP BY a.année
				ORDER BY a.année) AS B
USING (année);'''

df = pd.read_sql(q, conn)
reg = LinearRegression().fit(df[['population']], df['nombre_employe'])
