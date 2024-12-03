# automatizador-compras-lotofacil
Automatizador desenvolvido em Python para efetuar jogos no site https://www.loteriasonline.caixa.gov.br/silce-web/#/lotofacil ```É necessário ter uma conta ativa.```

# Arquivo "credenciais.txt"
O arquivo credenciais.txt é obrigatório e de ve estar na raiz do projeto:
```
username=XXXXXXXXXXX (trocar pelo CPF)
senha=999999 (trocar pela senha) 
```

# Arquivo "jogos.txt"
O arquivo jogos.txt é obrigatório e de ve estar na raiz do projeto, seu formato é UTF-8.
```
Seu conteúdo por linha deve conter 15 dezenas separadas pelo caractere "-":
01-02-03-04-05-06-07-08-10-13-14-15-16-22-24
ou
1-2-3-4-5-6-7-8-10-13-14-15-16-22-24
```

# Compatível com versao_sistema_apostador 2.98.30.3

# Instalação
Criar ambiente virtual:
```python -m venv venv```

Ativar ambiente virtual:
```.\venv\Scripts\activate```

Instalar as dependências do projeto:
```pip install -r requirements.txt```

Executar aplicativo:
```python app.py```

# License
[MIT license](https://opensource.org/licenses/MIT).