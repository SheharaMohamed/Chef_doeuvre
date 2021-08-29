from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "mysql+pymysql://user1:mdp1@localhost/emploi?charset=utf8mb4&binary_prefix=true")


conn = engine.connect()


q_cat = '''SELECT c.catégorie, p.* FROM année a
        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_catégorie USING (pop_id)) p USING (année)
        INNER JOIN catégorie c USING (cat_id)
        ORDER BY p.année;'''

df_cat = pd.read_sql(q_cat, conn)


q_cha = '''SELECT c.characteristique, p.*, t.* FROM année a
        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_chardemploi USING (pop_id)) p USING (année)
        INNER JOIN char_demploi c USING (cha_id)
        INNER JOIN type_char t USING (typ_id)
        ORDER BY p.année;'''

df_cha = pd.read_sql(q_cha, conn)


q_geo = '''SELECT d.departement, r.code_reg, r.region, p.* FROM année a
        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_departement USING (pop_id)) p USING (année)
        INNER JOIN departement d USING (code_postal)
        INNER JOIN région r USING (code_reg)
        ORDER BY p.année;'''

df_geo = pd.read_sql(q_geo, conn)


q_dip = '''SELECT d.diplôme, p.* FROM année a
        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_diplôme USING (pop_id)) p USING (année)
        INNER JOIN diplôme d USING (dip_id)
        ORDER BY p.année;'''

df_dip = pd.read_sql(q_dip, conn)