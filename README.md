# Netflix SQLite SQL Demo

Questo progetto mostra come usare **Python**, **Pandas** e **SQLite** per lavorare con un dataset reale di Netflix (`netflix_titles.csv`) e sperimentare diverse funzionalità SQL.  
Include esempi di **CREATE TABLE, INSERT, SELECT, JOIN, UPDATE, DELETE, VIEW, INDEX, Subquery e CTE (WITH)**.

---

## 📂 Dataset

Il dataset usato è disponibile su Kaggle: [shivamb/netflix-shows](https://www.kaggle.com/shivamb/netflix-shows)  

Colonne principali:

- `show_id` → ID unico per ogni titolo  
- `type` → Movie o TV Show  
- `title` → Titolo  
- `director` → Regista  
- `cast` → Attori principali  
- `country` → Paese di produzione  
- `date_added` → Data di aggiunta su Netflix  
- `release_year` → Anno di uscita  
- `rating` → Classificazione (PG, R, etc.)  
- `duration` → Durata (minuti o stagioni)  
- `listed_in` → Generi  
- `description` → Breve descrizione  

---

## ⚙️ Funzionalità principali del codice

### 1️⃣ Download e importazione CSV

```python
import kagglehub
import pandas as pd
import sqlite3

path = kagglehub.dataset_download("shivamb/netflix-shows")
df = pd.read_csv(f"{path}/netflix_titles.csv")

conn = sqlite3.connect("netflix.db")
df.to_sql("netflix", conn, if_exists="replace", index=False)
```

- Scarica il dataset da Kaggle
- Lo legge con Pandas
- Lo importa in un database SQLite (netflix.db)

### 2️⃣ Creazione e modifica tabelle

```sql
CREATE TABLE genres (...);
ALTER TABLE netflix ADD COLUMN duration_minutes;
```

- **CREATE TABLE**: crea nuove tabelle, in questo caso `genres`
- **ALTER TABLE**: aggiunge colonne nuove a tabelle esistenti

### 3️⃣ Inserimento e selezione dei dati

```sql
INSERT INTO netflix (...) VALUES (...);
SELECT title, country, release_year FROM netflix WHERE country='Italy';
```

- **INSERT INTO**: aggiunge nuovi record
- **SELECT**: recupera dati filtrati e ordinati
- Esempio: 5 film italiani più recenti

### 4️⃣ Clausole SQL comuni

- **WHERE** → filtra righe secondo condizioni
- **GROUP BY** → raggruppa i dati
- **HAVING** → filtra i gruppi creati con GROUP BY
- **ORDER BY** → ordina i risultati
- **LIMIT** → limita il numero di risultati

### 5️⃣ JOIN tra tabelle

```sql
SELECT n.title, g.genre
FROM netflix n
JOIN genres g ON n.show_id = g.show_id;
```

- **JOIN**: unisce due tabelle tramite chiavi comuni
- Mostra come collegare film e generi

### 6️⃣ Funzioni aggregate

- **COUNT(*)** → conta le righe
- **AVG()** → calcola la media

Esempi:
- Conteggio dei tipi di contenuti (Movie, TV Show)
- Anno medio dei film

### 7️⃣ View

```sql
CREATE VIEW recent_movies AS 
SELECT title, release_year, country 
FROM netflix 
WHERE release_year >= 2020;
```

- **VIEW** salva una query come tabella virtuale
- Utile per query complesse o frequenti

### 8️⃣ Indici

```sql
CREATE INDEX idx_country ON netflix(country);
```

- Migliora le prestazioni delle query sulle colonne più utilizzate

### 9️⃣ Subquery

```sql
SELECT title 
FROM netflix 
WHERE release_year = (SELECT MAX(release_year) FROM netflix);
```

- Query dentro un'altra query per filtrare dati
- Esempio: trovare il film più recente

### 🔟 UPDATE e DELETE

```sql
UPDATE netflix SET rating='NR' WHERE rating IS NULL;
DELETE FROM netflix WHERE show_id='EX123';
```

- **UPDATE** → modifica dati esistenti
- **DELETE** → rimuove record

### 1️⃣1️⃣ Common Table Expression (CTE)

```sql
WITH recent_movies AS (
    SELECT title, release_year
    FROM netflix
    WHERE release_year >= 2020
)
SELECT COUNT(*) AS count_recent FROM recent_movies;
```

- **WITH** definisce query temporanee
- Utile per semplificare query complesse

---

## 📝 Come usare il progetto

1. Scaricare il dataset Netflix da Kaggle
2. Eseguire lo script Python per creare il database SQLite
3. Usare le query SQL presenti come esempi
4. Modificare o aggiungere query per sperimentare con SELECT, JOIN, GROUP BY, UPDATE, DELETE, VIEW, Subquery e CTE

---

## 🎯 Obiettivi didattici

- Imparare le basi di SQL con SQLite
- Usare Pandas per importare dati CSV in un database
- Eseguire query complesse e utilizzare funzioni aggregate
- Gestire tabelle, indici, viste, join e subquery
