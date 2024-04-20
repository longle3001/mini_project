# Introduce project #

## Overview ##
Build a basic CRUD application using FastAPI, Postgres and Qdrant/Fastembed. The API endpoint will support both creation and retrieval of embedded documents.

### Requirements ###
- Use Python 3.11 (or 3.10 if you find compatibility issues)
- Do NOT use sqlalchemy for postgres, use “psycopg v3” and regular sql statements
- Three test .txt documents have been provided to verify functionality, use these for testing

### Desired Flow ###
Full details are provided below, but the full final flow should approximately look like the following:
- POST calls to /embeddings with each txt document and body parameters
Store in Qdrant with FastEmbed to generate embeddings and store with parameters as payload
- Store in Postgres table including with FastEmbed id
- GET call to /embeddings/by-organisation-id/{organisation_id} with the chosen organisation id returns all the files with associated metadata
- POST call to /embeddings/search with “query” set to “a statement about sports” and type “.txt” returns the document metadata of “soccer.txt” and “tennis.txt” but not “food.txt” (or at least soccer.txt and tennis.txt should rank higher by similarity).

## Creation ##
### FastAPI ###
POST /embeddings endpoint which accepts:
- A file (.txt file)
- project (str)
- organisation_id (str)

### Qdrant ###
**Directions**: https://qdrant.tech/

- Use Qdrant and FastEmbed to embed and store the txt document contents and metadata
  - Use the BAAI/bge-small-en-v1.5 for the embeddings model (can find it supported here)
  - Store filename, content, type, project and organisation_id as metadata for file (in the Qdrant payload)

**Desired Result**

Three entries in a Qdrant collection with all metadata and correct embeddings for all 3 txt files.

### Postgres ###