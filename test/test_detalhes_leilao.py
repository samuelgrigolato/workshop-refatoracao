from test.fabricas.leilao import fabricar_leilao, fabricar_lance


def test_sem_lances(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1, criador='cfb795dc-7c3d-406e-8cac-ae310e82e1b2')
  resp = client.get('/leiloes/-1')
  assert resp.status_code == 200
  json = resp.json
  assert json['criador'] == 'cfb795dc-7c3d-406e-8cac-ae310e82e1b2'
  assert json['id'] == -1
  assert json['lances'] == []


def test_com_lances(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1, criador='cfb795dc-7c3d-406e-8cac-ae310e82e1b2')
    fabricar_lance(cur, id_=-1, id_leilao=-1, data='2020-01-01 10:30', valor=50)
    fabricar_lance(cur, id_=-2, id_leilao=-1, data='2020-01-01 10:31', valor=51)
    fabricar_lance(cur, id_=-3, id_leilao=-1, data='2020-01-01 10:29', valor=49)
  resp = client.get('/leiloes/-1')
  assert resp.status_code == 200
  json = resp.json
  assert json['criador'] == 'cfb795dc-7c3d-406e-8cac-ae310e82e1b2'
  assert json['id'] == -1
  lances = json['lances']
  assert lances is not None
  assert len(lances) == 3
  assert lances[0]['id'] == -3
  assert lances[1]['id'] == -1
  assert lances[2]['id'] == -2
