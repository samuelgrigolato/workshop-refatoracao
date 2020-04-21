from flask import Flask, jsonify, Response
from http import HTTPStatus


app = Flask(__name__)


@app.route('/leiloes/<id_leilao>', methods=['GET'])
def get_detalhes_do_leilao(id_leilao):
  return jsonify({
    'id': id_leilao
  })


@app.route('/leiloes/<id_leilao>/lances', methods=['POST'])
def registrar_lance(id_leilao):
  return '', HTTPStatus.NO_CONTENT


@app.route('/leiloes/<id_leilao>/lances/minimo', methods=['POST'])
def registrar_lance_minimo(id_leilao):
  return '', HTTPStatus.NO_CONTENT


@app.route('/leiloes/proximo', methods=['GET'])
def get_detalhes_do_proximo_leilao():
  return jsonify({
    'id': 1
  })
