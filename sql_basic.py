import kagglehub
import pandas as pd
import sqlite3
# Download latest version
path = kagglehub.dataset_download("shivamb/netflix-shows")

print("Path to dataset files:", path)


# Leggi il file CSV
df = pd.read_csv(f"{path}/netflix_titles.csv")

# Crea un database SQLite e importa i dati
conn = sqlite3.connect("netflix.db")
df.to_sql("netflix", conn, if_exists="replace", index=False)
cur = conn.cursor()

# ==========================
# 1️⃣ Tables: CREATE, ALTER
# ==========================
# Creiamo una tabella aggiuntiva per i generi (listed_in)
cur.execute("""
CREATE TABLE IF NOT EXISTS genres (
    id INTEGER PRIMARY KEY,
    show_id TEXT,
    genre TEXT,
    FOREIGN KEY (show_id) REFERENCES netflix(show_id)
)
""")

# Aggiungiamo una colonna fittizia se non esiste
try:
    cur.execute("ALTER TABLE netflix ADD COLUMN duration_minutes INTEGER")
except:
    pass  # La colonna potrebbe già esistere

# ==========================
# 2️⃣ Insert e Select
# ==========================
# Inseriamo un film di esempio
cur.execute("""
INSERT INTO netflix (show_id, title, type, country, release_year, rating)
VALUES ('EX123', 'Example Movie', 'Movie', 'Italy', 2025, 'PG')
""")

query = """
SELECT country, COUNT(*) AS num_titles
FROM netflix
GROUP BY country
ORDER BY num_titles DESC
LIMIT 10;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Query base
query1 = """
SELECT title, country, release_year
FROM netflix
WHERE country='Italy'
ORDER BY release_year DESC
LIMIT 5
"""
df1 = pd.read_sql_query(query1, conn)
print("5 film italiani più recenti:")
print(df1)

# ==========================
# 3️⃣ Clauses: WHERE, ORDER BY, GROUP BY, HAVING
# ==========================
query2 = """
SELECT country, COUNT(*) AS num_titles
FROM netflix
WHERE country IS NOT NULL
GROUP BY country
HAVING num_titles > 50
ORDER BY num_titles DESC
LIMIT 10
"""
df2 = pd.read_sql_query(query2, conn)
print("\nTop 10 paesi con più titoli (>=50):")
print(df2)


# ==========================
# 4️⃣ Joins
# ==========================
# Inseriamo dati nella tabella genres
cur.execute("INSERT INTO genres (show_id, genre) VALUES (1, 'Drama')")
cur.execute("INSERT INTO genres (show_id, genre) VALUES (1, 'Action')")

query3 = """
SELECT n.title, g.genre
FROM netflix n
JOIN genres g ON n.rowid = g.show_id
"""
df3 = pd.read_sql_query(query3, conn)
print("\nEsempio JOIN film-genere:")
print(df3)

# ==========================
# 4️⃣ Joins
# ==========================
# Inseriamo dati nella tabella genres usando listed_in come esempio
cur.execute("INSERT INTO genres (show_id, genre) VALUES ('EX123', 'Drama')")
cur.execute("INSERT INTO genres (show_id, genre) VALUES ('EX123', 'Action')")

query3 = """
SELECT n.title, g.genre
FROM netflix n
JOIN genres g ON n.show_id = g.show_id
LIMIT 5
"""
df3 = pd.read_sql_query(query3, conn)
print("\nEsempio JOIN film-genere:")
print(df3)

# ==========================
# 5️⃣ Functions: COUNT, AVG
# ==========================
query4 = """
SELECT type, COUNT(*) AS count_type
FROM netflix
GROUP BY type
"""
df4 = pd.read_sql_query(query4, conn)
print("\nConteggio dei tipi di contenuti:")
print(df4)

query5 = """
SELECT AVG(release_year) AS avg_year
FROM netflix
WHERE type='Movie'
"""
df5 = pd.read_sql_query(query5, conn)
print("\nAnno medio dei film:")
print(df5)

# ==========================
# 6️⃣ View
# ==========================
cur.execute("DROP VIEW IF EXISTS recent_movies")
cur.execute("""
CREATE VIEW recent_movies AS
SELECT title, release_year, country
FROM netflix
WHERE release_year >= 2020
""")

df6 = pd.read_sql_query("SELECT * FROM recent_movies LIMIT 5", conn)
print("\nVista dei film recenti:")
print(df6)

# ==========================
# 7️⃣ Index
# ==========================
cur.execute("CREATE INDEX IF NOT EXISTS idx_country ON netflix(country)")

# ==========================
# 8️⃣ Subquery
# ==========================
query7 = """
SELECT title, release_year
FROM netflix
WHERE release_year = (
    SELECT MAX(release_year) FROM netflix
)
"""
df7 = pd.read_sql_query(query7, conn)
print("\nFilm più recente:")
print(df7)

# ==========================
# 8️⃣UPDATE Statement: modificare dati esistenti
# ==========================
cur.execute("""
UPDATE netflix
SET rating='NR'
WHERE rating IS NULL;
""")

# Verifica i risultati con una SELECT
query8 = """
SELECT title, rating
FROM netflix
WHERE rating='NR'
LIMIT 5;
"""
df8 = pd.read_sql_query(query8, conn)
print("\nUpdate:: film aggiornati con rating 'NR'")
print(df8)


# ==========================
# 9️⃣ DELETE Statement
# ==========================
# Esempio: rimuovere il film di prova inserito
cur.execute("""
DELETE FROM netflix
WHERE show_id='EX123'
""")

# Controllo DELETE
query9 = """
SELECT COUNT(*) AS deleted_check
FROM netflix
WHERE show_id='EX123'
"""
df9 = pd.read_sql_query(query9, conn)
print("\nDELETE controllo (0 = cancellato correttamente):")
print(df9)

# ==========================
# 🔟 Subquery
# ==========================
query10 = """
SELECT title, release_year
FROM netflix
WHERE release_year = (
    SELECT MAX(release_year) FROM netflix
)
"""
df10 = pd.read_sql_query(query10, conn)
print("\nFilm più recente:")
print(df10)

# ==========================
# 1️⃣1️⃣ Common Table Expression (WITH)
# ==========================
query11 = """
WITH recent_movies AS (
    SELECT title, release_year
    FROM netflix
    WHERE release_year >= 2020
)
SELECT COUNT(*) AS count_recent
FROM recent_movies
"""
df11 = pd.read_sql_query(query11, conn)
print("\nNumero di film dal 2020 ad oggi:")
print(df11)


# ==========================
# Commit e chiusura
# ==========================
conn.commit()
conn.close()
