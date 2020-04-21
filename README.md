# Workshop sobre refatoração

Toda pessoa que trabalha com software já passou, ou vai passar, pela experiência de adicionar/alterar funcionalidades de um sistema que está no ar. Com isso ela se vê em contato com uma base de código existente, produzida por uma outra equipe.

Qual a postura esperada desse profissional? Até onde é correto “colocar a culpa” na equipe de desenvolvimento anterior? Até onde é válido barrar demandas devido a limitações da arquitetura atual do sistema? Nesse workshop você será guiado por um processo simulado dessa situação, tendo a oportunidade de praticar desde a parte técnica (refatoração segura) quanto a parte ética e profissional dessa tarefa que normalmente negligenciamos durante nossa capacitação profissional.

## Pré-requisitos

Para seguir este workshop você precisa ter instalado na sua máquina:

- Python 3
- PostgreSQL

## Ambiente virtual Python

Recomenda-se o uso de um ambiente virtual Python, por exemplo com o comando:

```sh
python -m venv ~/.pyenvs/refatoracao
```

Sempre que quiser iniciar este ambiente em um terminal, execute:

```sh
source ~/.pyenvs/refatoracao/bin/activate
```

## Executando

Primeiro instale as dependências:

```sh
pip install -r requirements.txt
```

Depois execute a aplicação:

```sh
FLASK_APP=api.py flask run
```

Utilize `cUrl` ou outro cliente HTTP para fazer as chamadas.

## Exemplos de chamada cUrl

Nota: os exemplos abaixo usam `jq` para formatar respostas JSON. Caso não tenha esse utilitário na máquina, basta retirá-lo da chamada. Exemplo de alternativas:

```sh
$ curl -s http://localhost:5000/leiloes/1 | jq
$ curl -s http://localhost:5000/leiloes/1 | json_pp
$ curl http://localhost:5000/leiloes/1
```

Detalhes do leilão:

```sh
$ curl -s http://localhost:5000/leiloes/1 | jq
{
  "id": "1"
}
```

Submissão de lance:

```sh
$ curl -i -X POST -s http://localhost:5000/leiloes/1/lances \
  -H "Content-Type: application/json" \
  -d "{}"
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Tue, 21 Apr 2020 00:37:41 GMT
```

Submissão de lance mínimo:

```sh
$ curl -i -X POST -s http://localhost:5000/leiloes/1/lances/minimo \
  -H "Content-Type: application/json" \
  -d "{}"
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Tue, 21 Apr 2020 00:38:19 GMT
```

Detalhes do próximo leilão:

```sh
$ curl -s http://localhost:5000/leiloes/proximo | jq
{
  "id": 1
}
```
