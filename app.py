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
  with db.conexao_gerenciada().cursor() as cur:
    leilao = repositorio.leilao.buscar(cur, id_leilao)
    lances = repositorio.leilao.buscar_lances(cur, id_leilao)
    ultimo_lance = lances[-1] if len(lances) > 0 else None
    return jsonify({
      'id': leilao[0],
      'descricao': leilao[1],
      'criador': leilao[2],
      'data': leilao[3].isoformat(),
      'diferenca_minima': leilao[4],
      'lances': [
        {
          'id': lance[0],
          'valor': lance[1],
          'comprador': lance[2],
          'data': lance[3].isoformat()
        }
        for lance in lances
      ]
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
  with db.conexao_gerenciada().cursor() as cur:
    valor_ultimo_lance = repositorio.leilao.buscar_valor_ultimo_lance(cur, id_leilao)
    diferenca_minima = repositorio.leilao.buscar_diferenca_minima(cur, id_leilao)
    valor = 1 if valor_ultimo_lance is None else valor_ultimo_lance + diferenca_minima
    repositorio.leilao.inserir_lance(cur, id_leilao, valor, id_usuario)
  return '', HTTPStatus.NO_CONTENT
