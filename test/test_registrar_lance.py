from test.fabricas.leilao import fabricar_leilao, fabricar_lance


def test_lance_valido(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1)
    fabricar_lance(cur, id_=-1, id_leilao=-1, valor=50)
  resp = client.post(
    '/leiloes/-1/lances',
    json={ 'valor': 300 },
    headers={ 'x_id_usuario': '5bfd3460-468e-4b30-bf1e-6917869b258c' }
  )
  assert resp.status_code == 204
  with con.cursor() as cur:
    cur.execute("""
      select count(1)
      from lances
      where id_leilao = -1
        and valor = 300
    """)
    assert (1, ) == cur.fetchone()


def test_lance_menor(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1)
    fabricar_lance(cur, id_=-1, id_leilao=-1, valor=50)
  resp = client.post(
    '/leiloes/-1/lances',
    json={ 'valor': 50 },
    headers={ 'x_id_usuario': '5bfd3460-468e-4b30-bf1e-6917869b258c' }
  )
  assert resp.status_code == 400


def test_menor_que_diferenca_minima(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1, diferenca_minima=200)
    fabricar_lance(cur, id_=-1, id_leilao=-1, valor=50)
  resp = client.post(
    '/leiloes/-1/lances',
    json={ 'valor': 249 },
    headers={ 'x_id_usuario': '5bfd3460-468e-4b30-bf1e-6917869b258c' }
  )
  assert resp.status_code == 400


def test_lance_do_criador(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1, criador='5bfd3460-468e-4b30-bf1e-6917869b258c')
  resp = client.post(
    '/leiloes/-1/lances',
    json={ 'valor': 1 },
    headers={ 'x_id_usuario': '5bfd3460-468e-4b30-bf1e-6917869b258c' }
  )
  assert resp.status_code == 400
