# INE5608 - Alapo - Entrega 4

- [Vídeos de apresentação - Pedro e Gabriel](https://drive.google.com/drive/folders/1mm3XLVuhgV4KnJxWXXap6aT_GoVg9fgm?usp=drive_link)

O projeto está organizado da seguinte maneira:

```
.
├── ALAPO - Especificação de Requisitos.pdf
├── REAMDE.md
├── latex
│   └── // CÓDIGO FONTE DO DOC. DE ESPECIFICAÇÃO DE REQUISITOS
├── src
│   └── // CÓDIGO FONTE DO PROJETO
└── visualparadigm
    └── // ARQUIVO DE PROJETO - VISUAL PARADIGM
```

## Executando o projeto

O gerenciamento de dependências do projeto é feita através do [Poetry](https://python-poetry.org/); recomendamos que
utilize esta ferramenta para realizar a instalação das bibliotecas utilizadas com facilidade. Caso deseje, as
instruções para instalação e execução do projeto utilizando somente `pip` e `venv` estão disponíveis na próxima seção.

1. Instale o Poetry para realizar a instalação das dependências (recomendado instalar usando o 
[pipx](https://pipx.pypa.io/stable/installation/), para não interferir com os ambientes virtuais do seu sistema 
operacional):

```sh
pipx install poetry
```

2. Instale as dependências do projeto:

```sh
# pwd: INE5608-2024.02-4.0.0-entrega/src
poetry install
```

3. Execute o projeto:

```sh
# pwd: INE5608-2024.02-4.0.0-entrega/src
poetry run alapo
```

Alternativamente, a instalação e execução pode ser feita diretamente via `pip`:

1. Instancie e ative um ambiente virtual para a instalação do projeto:

```sh
# pwd: INE5608-2024.02-4.0.0-entrega/src
python -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências do projeto:

```sh
# pwd: INE5608-2024.02-4.0.0-entrega/src
pip install -r requirements.txt
```

3. Execute o projeto:

```sh
# pwd: INE5608-2024.02-4.0.0-entrega/src
python -m alapo
```
