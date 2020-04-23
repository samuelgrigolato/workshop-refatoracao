import logging
import os
import psycopg2
import psycopg2.extras
from flask import g


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def conexao_gerenciada():
  # Este é um padrão comum em projetos Flask,
  # pegue um objeto de "g", caso ele não exista ainda,
  # crie-o. Isso permite que a suíte de teste possa
  # prover um mock desse recurso mais facilmente.
  if 'conexao' not in g:
    g.conexao = abrir_conexao()
  return g.conexao


def liberar_conexao_gerenciada(testando=False):
  conexao = g.pop('conexao', None)
  if conexao is not None:
    if not testando:
      conexao.commit()
    else:
      conexao.rollback()
    conexao.close()


def abrir_conexao():
  # Exemplo: DB_CONN_STRING="dbname=banco1 user=postgres password=postgres host=localhost"
  conexao = psycopg2.connect(
    os.environ['DB_CONN_STRING'],
    connection_factory=psycopg2.extras.LoggingConnection
  )
  conexao.initialize(logger)
  return conexao
