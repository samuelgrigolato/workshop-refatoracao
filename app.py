from flask import Flask, jsonify, Response, request
from http import HTTPStatus

import db
import repositorio.leilao


app = Flask(__name__)


@app.teardown_appcontext
def liberar_conexao_gerenciada(_):
  db.liberar_conexao_gerenciada(testando=app.config['TESTING'])


@app.route('/leiloes/<id_leilao>', methods=['GET'])
def get_detalhes_do_leilao(id_leilao):
  with db.abrir_conexao() as conexao, conexao.cursor() as cur:
    cur.execute("""
      SELECT id, descricao, criador, data, diferenca_minima
      FROM leiloes
      WHERE id = %s
    """, (id_leilao, ))
    leilao = cur.fetchone()
    cur.execute("""
      SELECT id, valor, comprador, data
      FROM lances
      WHERE id_leilao = %s
      ORDER BY data DESC
      LIMIT 1
    """, (id_leilao, ))
    lance = cur.fetchone()
    return jsonify({
      'id': leilao[0],
      'descricao': leilao[1],
      'criador': leilao[2],
      'data': leilao[3].isoformat(),
      'diferenca_minima': leilao[4],
      'ultimo_lance': {
        'id': lance[0],
        'valor': lance[1],
        'comprador': lance[2],
        'data': lance[3].isoformat()
      } if lance is not None else None
    })


@app.route('/leiloes/<id_leilao>/lances', methods=['POST'])
def registrar_lance(id_leilao):
  dados = request.get_json()
  id_usuario = request.headers['X-Id-Usuario'] # simulação meia boca de autenticação
  with db.conexao_gerenciada().cursor() as cur:
    valor_ultimo_lance = repositorio.leilao.buscar_valor_ultimo_lance(cur, id_leilao)
    if valor_ultimo_lance is not None:
      if valor_ultimo_lance >= dados['valor']:
        return 'Lance deve ser maior que o último.', HTTPStatus.BAD_REQUEST
      diferenca_minima = repositorio.leilao.buscar_diferenca_minima(cur, id_leilao)
      if valor_ultimo_lance + diferenca_minima > dados['valor']:
        return 'Lance deve ser maior que o atual mais a diferença mínima.', HTTPStatus.BAD_REQUEST
    repositorio.leilao.inserir_lance(cur, id_leilao, dados['valor'], id_usuario)
  return '', HTTPStatus.NO_CONTENT


@app.route('/leiloes/<id_leilao>/lances/minimo', methods=['POST'])
def registrar_lance_minimo(id_leilao):
  id_usuario = request.headers['X-Id-Usuario'] # simulação meia boca de autenticação
  with db.abrir_conexao() as conexao, conexao.cursor() as cur:
    cur.execute("""
      SELECT valor
      FROM lances
      WHERE id_leilao = %s
      ORDER BY data DESC
      LIMIT 1
    """, (id_leilao, ))
    ultimo_lance = cur.fetchone()
    valor = 1 if ultimo_lance is None else ultimo_lance[0] + 1
    cur.execute("""
      INSERT INTO lances (id_leilao, valor, comprador, data)
      VALUES (%s, %s, %s, now())
    """, (id_leilao, valor, id_usuario))
  return '', HTTPStatus.NO_CONTENT


@app.route('/leiloes/proximo', methods=['GET'])
def get_detalhes_do_proximo_leilao():
  with db.abrir_conexao() as conexao, conexao.cursor() as cur:
    cur.execute("""
      SELECT id, descricao, criador, data, diferenca_minima
      FROM leiloes
      ORDER BY data
      LIMIT 1
    """)
    leilao = cur.fetchone()
    id_leilao = leilao[0]
    cur.execute("""
      SELECT id, valor, comprador, data
      FROM lances
      WHERE id_leilao = %s
      ORDER BY data DESC
      LIMIT 1
    """, (id_leilao, ))
    lance = cur.fetchone()
    return jsonify({
      'id': leilao[0],
      'descricao': leilao[1],
      'criador': leilao[2],
      'data': leilao[3].isoformat(),
      'diferenca_minima': leilao[4],
      'ultimo_lance': {
        'id': lance[0],
        'valor': lance[1],
        'comprador': lance[2],
        'data': lance[3].isoformat()
      } if lance is not None else None
    })
