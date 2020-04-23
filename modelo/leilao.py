import repositorio.leilao


class ValorMenorQueLanceAtual(Exception):
  pass


class ValorMenorQueDiferencaMinima(Exception):
  pass


def registrar_lance(cur, id_leilao, valor, id_usuario):
  valor_ultimo_lance = repositorio.leilao.buscar_valor_ultimo_lance(cur, id_leilao)
  if valor_ultimo_lance is not None:
    if valor_ultimo_lance >= valor:
      raise ValorMenorQueLanceAtual()
    diferenca_minima = repositorio.leilao.buscar_diferenca_minima(cur, id_leilao)
    if valor_ultimo_lance + diferenca_minima > valor:
      raise ValorMenorQueDiferencaMinima()
  repositorio.leilao.inserir_lance(cur, id_leilao, valor, id_usuario)
