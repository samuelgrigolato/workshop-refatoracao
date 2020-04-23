from datetime import datetime


def fabricar_leilao(cur, id_, descricao='teste', criador='c153c124-7daa-4328-8f04-1dd824f5c309', data=None, diferenca_minima=100):
  cur.execute(f"""
    insert into leiloes (id, descricao, criador, data, diferenca_minima)
    values (%s, %s, %s, %s, %s)
  """, (
    id_,
    descricao,
    criador,
    data if data is not None else datetime.now(),
    diferenca_minima
  ))


def fabricar_lance(cur, id_, id_leilao, comprador='8f1061a8-a687-436a-8b1b-7a302994474a', valor=100, data=None):
  cur.execute(f"""
    insert into lances (id, id_leilao, comprador, valor, data)
    values (%s, %s, %s, %s, %s)
  """, (
    id_,
    id_leilao,
    comprador,
    valor,
    data if data is not None else datetime.now()
  ))
