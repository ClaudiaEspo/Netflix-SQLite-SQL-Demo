# Netflix-SQLite-SQL-Demo
Questo progetto mostra come usare Python, Pandas e SQLite per lavorare con un dataset reale di Netflix (netflix_titles.csv) e sperimentare diverse funzionalità SQL. Include esempi di CREATE TABLE, INSERT, SELECT, JOIN, UPDATE, DELETE, VIEW, INDEX, Subquery e CTE (WITH).
Struttura del codice
1️⃣ Download e importazione dataset
import kagglehub
import pandas as pd
import sqlite3

path = kagglehub.dataset_download("shivamb/netflix-shows")
df = pd.read_csv(f"{path}/netflix_titles.csv")

conn = sqlite3.connect("netflix.db")
df.to_sql("netflix", conn, if_exists="replace", index=False)
cur = conn.cursor()


Scarica il dataset Netflix da Kaggle

Lo legge con Pandas

Lo importa in un database SQLite (netflix.db)

La tabella principale si chiama netflix

2️⃣ Creazione e modifica tabelle
CREATE TABLE genres
ALTER TABLE netflix ADD COLUMN duration_minutes


CREATE TABLE: crea una nuova tabella genres collegata alla tabella netflix tramite show_id

ALTER TABLE: aggiunge una colonna aggiuntiva alla tabella netflix

3️⃣ Inserimento e selezione dei dati
INSERT INTO netflix ...
SELECT country, COUNT(*) ...


INSERT INTO: aggiunge nuovi record nella tabella

SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT ...: query base per filtrare e ordinare dati

Esempio: trovare i 5 film italiani più recenti

4️⃣ Clausole SQL comuni
WHERE, ORDER BY, GROUP BY, HAVING


WHERE: filtra i record secondo condizioni

GROUP BY: raggruppa i dati per una colonna

HAVING: filtra i gruppi creati con GROUP BY

ORDER BY: ordina i risultati

Esempio: Top 10 paesi con più titoli (>=50)

5️⃣ Join tra tabelle
SELECT n.title, g.genre
FROM netflix n
JOIN genres g ON n.show_id = g.show_id


JOIN: unisce due tabelle in base a chiavi comuni

Mostra come collegare i film ai loro generi

6️⃣ Funzioni aggregate
COUNT(), AVG()


COUNT(*): conta il numero di righe

AVG(): calcola la media

Esempio: conteggio dei tipi di contenuti e anno medio dei film

7️⃣ View
CREATE VIEW recent_movies AS ...


VIEW: salva una query come vista virtuale, utile per query complesse

Esempio: creare una vista con i film dal 2020

8️⃣ Indici
CREATE INDEX idx_country ON netflix(country)


Migliora le prestazioni delle query su colonne frequentemente utilizzate

9️⃣ Subquery
SELECT title FROM netflix WHERE release_year = (SELECT MAX(release_year) FROM netflix)


Query dentro un’altra query per filtrare i dati

Esempio: trovare il film più recente

🔟 UPDATE e DELETE
UPDATE netflix SET rating='NR' WHERE rating IS NULL
DELETE FROM netflix WHERE show_id='EX123'


UPDATE: modifica dati esistenti

DELETE: elimina record

1️⃣1️⃣ Common Table Expression (CTE)
WITH recent_movies AS (...) SELECT COUNT(*) FROM recent_movies


WITH: definisce una query temporanea per semplificare query complesse

Esempio: contare i film dal 2020 ad oggi

Come usare il progetto

Scaricare il dataset Netflix da Kaggle (shivamb/netflix-shows)

Eseguire lo script Python per creare il database SQLite

Utilizzare le query SQL presenti come esempi

Modificare o aggiungere query per sperimentare con SELECT, JOIN, GROUP BY, UPDATE, DELETE, VIEW, Subquery e CTE

Obiettivi didattici

Imparare le basi di SQL con SQLite

Usare Pandas per importare dati CSV in un database

Eseguire query complesse e utilizzare funzioni aggregate

Gestire tabelle, indici, viste, join e subquery
