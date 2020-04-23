import app
import db


def test_lance_valido(con, client):
  with con.cursor() as cur:
    cur.execute("""
      insert into leiloes (id, descricao, criador, data, diferenca_minima)
      values (-1, 'teste', 'cfb795dc-7c3d-406e-8cac-ae310e82e1b2', now(), 200)
    """)
    cur.execute("""
      insert into lances (id, id_leilao, comprador, data, valor)
      values (-1, -1, '63b02def-0a48-4fa9-b6d5-334c4538123f', now(), 50)
    """)
  resp = client.post(
    '/leiloes/-1/lances',
    json={ 'valor': 300 },
    headers={ 'x_id_usuario': '5bfd3460-468e-4b30-bf1e-6917869b258c' }
  )
  assert resp.status_code == 204
  with db.conexao_gerenciada().cursor() as cur:
    cur.execute("""
      select count(1)
      from lances
      where id_leilao = -1
        and valor = 300
    """)
    assert (1, ) == cur.fetchone()


def test_lance_menor(con, client):
  with con.cursor() as cur:
    cur.execute("""
      insert into leiloes (id, descricao, criador, data, diferenca_minima)
      values (-1, 'teste', 'cfb795dc-7c3d-406e-8cac-ae310e82e1b2', now(), 200)
    """)
    cur.execute("""
      insert into lances (id, id_leilao, comprador, data, valor)
      values (-1, -1, '63b02def-0a48-4fa9-b6d5-334c4538123f', now(), 50)
    """)
  resp = client.post(
    '/leiloes/-1/lances',
    json={ 'valor': 50 },
    headers={ 'x_id_usuario': '5bfd3460-468e-4b30-bf1e-6917869b258c' }
  )
  assert resp.status_code == 400
