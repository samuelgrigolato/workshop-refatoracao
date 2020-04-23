

def test_sem_lances(con, client):
  with con.cursor() as cur:
    cur.execute("""
      insert into leiloes (id, descricao, criador, data, diferenca_minima)
      values (-1, 'teste', 'cfb795dc-7c3d-406e-8cac-ae310e82e1b2', now(), 200)
    """)
  resp = client.get('/leiloes/-1')
  assert resp.status_code == 200
  json = resp.json
  assert json['criador'] == 'cfb795dc-7c3d-406e-8cac-ae310e82e1b2'
  assert json['id'] == -1
  assert json['ultimo_lance'] is None


def test_com_lances(con, client):
  with con.cursor() as cur:
    cur.execute("""
      insert into leiloes (id, descricao, criador, data, diferenca_minima)
      values (-1, 'teste', 'cfb795dc-7c3d-406e-8cac-ae310e82e1b2', now(), 1)
    """)
    cur.execute("""
      insert into lances (id, id_leilao, comprador, data, valor)
      values (-1, -1, '63b02def-0a48-4fa9-b6d5-334c4538123f', '2020-01-01 10:30', 50)
    """)
    cur.execute("""
      insert into lances (id, id_leilao, comprador, data, valor)
      values (-2, -1, '63b02def-0a48-4fa9-b6d5-334c4538123f', '2020-01-01 10:31', 51)
    """)
    cur.execute("""
      insert into lances (id, id_leilao, comprador, data, valor)
      values (-3, -1, '63b02def-0a48-4fa9-b6d5-334c4538123f', '2020-01-01 10:29', 49)
    """)
  resp = client.get('/leiloes/-1')
  assert resp.status_code == 200
  json = resp.json
  assert json['criador'] == 'cfb795dc-7c3d-406e-8cac-ae310e82e1b2'
  assert json['id'] == -1
  ultimo_lance = json['ultimo_lance']
  assert ultimo_lance is not None
  assert ultimo_lance['id'] == -2
