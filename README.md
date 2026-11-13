 # Organizador de Arquivos

Script em Python que organiza os arquivos de uma pasta em subpastas por tipo
(imagens, documentos, planilhas, vídeos, etc.).

## Funcionalidades

- Classifica os arquivos pela extensão
- Modo `--dry-run`: simula as mudanças sem mover nada
- Não sobrescreve arquivos: nomes repetidos ganham sufixo `_1`, `_2`...
- Registra tudo em log (tela e arquivo `organizador.log`)
- Trata erros e continua organizando os demais arquivos
- Pede confirmação antes de mover arquivos

## Requisitos

- Python 3.10 ou superior (sem bibliotecas externas)

## Como usar

```bash
# Simular, sem mover nada
python organizador.py CAMINHO_DA_PASTA --dry-run

# Organizar de verdade
python organizador.py CAMINHO_DA_PASTA
```

## Testando com arquivos fictícios

```bash
python criar_pasta_teste.py
python organizador.py pasta_teste --dry-run
python organizador.py pasta_teste
```

## O que aprendi

`pathlib`, `shutil`, `logging`, `argparse`, tratamento de erros com `try/except`
e organização de código em funções.