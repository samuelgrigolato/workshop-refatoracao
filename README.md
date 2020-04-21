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

## Banco de dados

Execute os seguintes scripts para criar as tabelas iniciais:

```sql
create table leiloes (
  id serial primary key,
  descricao text not null,
  criador uuid not null,
  data timestamp with time zone not null,
  diferenca_minima smallint not null
);
insert into leiloes (descricao, criador, data, diferenca_minima)
values ('Caneca', 'efd28c1e-2538-4842-a97a-92759903c2fa', now(), 500);
insert into leiloes (descricao, criador, data, diferenca_minima)
values ('Cadeira', 'efd28c1e-2538-4842-a97a-92759903c2fa', now(), 1);

create table lances (
  id serial primary key,
  valor smallint not null,
  comprador uuid not null,
  data timestamp with time zone not null,
  id_leilao int not null,

  constraint fk_lances_leilao foreign key (id_leilao) references leiloes (id)
);
insert into lances (valor, comprador, data, id_leilao)
values (501, '1027c0fc-77c8-44d0-8b0b-4fdf9634bcd8', now(), 1);
insert into lances (valor, comprador, data, id_leilao)
values (1001, '05feb8af-89a1-4320-bf0f-29dc1b8754c5', now(), 1);
```

## Executando

Primeiro instale as dependências:

```sh
pip install -r requirements.txt
```

Depois execute a aplicação:

```sh
export DB_CONN_STRING="dbname=banco1 user=postgres password=postgres host=localhost"
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
$ curl -s http://localhost:5000/leiloes/2 | jq
{
  "criador": "efd28c1e-2538-4842-a97a-92759903c2fa",
  "data": "2020-04-21T22:45:24.179684+00:00",
  "descricao": "Cadeira",
  "diferenca_minima": 1,
  "id": 2,
  "ultimo_lance": null
}
```

Submissão de lance:

```sh
$ curl -i -X POST -s http://localhost:5000/leiloes/1/lances \
  -H "Content-Type: application/json" \
  -H "X-Id-Usuario: 43a72ab6-8abf-44c2-b6c2-da54f62f79cc" \
  -d "{ \"valor\": 200 }"
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Tue, 21 Apr 2020 00:37:41 GMT
```

Submissão de lance mínimo:

```sh
$ curl -i -X POST -s http://localhost:5000/leiloes/1/lances/minimo \
  -H "X-Id-Usuario: 43a72ab6-8abf-44c2-b6c2-da54f62f79cc"
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Tue, 21 Apr 2020 00:38:19 GMT
```

Detalhes do próximo leilão:

```sh
$ curl -s http://localhost:5000/leiloes/proximo | jq
{
  "criador": "efd28c1e-2538-4842-a97a-92759903c2fa",
  "data": "2020-04-21T22:45:23.933300+00:00",
  "descricao": "Caneca",
  "diferenca_minima": 500,
  "id": 1,
  "ultimo_lance": {
    "comprador": "43a72ab6-8abf-44c2-b6c2-da54f62f79cc",
    "data": "2020-04-21T23:11:24.205915+00:00",
    "id": 10,
    "valor": 207
  }
}
```
