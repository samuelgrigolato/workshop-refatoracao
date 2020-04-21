import os
import psycopg2


def abrir_conexao():
  # Exemplo: DB_CONN_STRING="dbname=banco1 user=postgres password=postgres host=localhost"
  return psycopg2.connect(os.environ['DB_CONN_STRING'])
