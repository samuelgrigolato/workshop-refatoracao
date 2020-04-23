from test.fabricas.leilao import fabricar_leilao, fabricar_lance


def test_com_lance_anterior(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1, diferenca_minima=2)
    fabricar_lance(cur, id_=-1, id_leilao=-1, valor=50)
  resp = client.post(
    '/leiloes/-1/lances/minimo',
    headers={ 'x_id_usuario': '5bfd3460-468e-4b30-bf1e-6917869b258c' }
  )
  assert resp.status_code == 204
  with con.cursor() as cur:
    cur.execute("""
      select count(1)
      from lances
      where id_leilao = -1
        and valor = 52
    """)
    assert (1, ) == cur.fetchone()


def test_sem_lance_anterior(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1, diferenca_minima=2)
  resp = client.post(
    '/leiloes/-1/lances/minimo',
    headers={ 'x_id_usuario': '5bfd3460-468e-4b30-bf1e-6917869b258c' }
  )
  assert resp.status_code == 204
  with con.cursor() as cur:
    cur.execute("""
      select count(1)
      from lances
      where id_leilao = -1
        and valor = 1
    """)
    assert (1, ) == cur.fetchone()
