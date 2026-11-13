"""Cria uma pasta de teste com arquivos fictícios para testar o organizador."""

from pathlib import Path

PASTA = Path(__file__).parent / "pasta_teste"

ARQUIVOS = [
    "foto_viagem.jpg",
    "logo.PNG",
    "relatorio.pdf",
    "notas.txt",
    "vendas.xlsx",
    "clipe.mp4",
    "musica.mp3",
    "backup.zip",
    "script.py",
    "dados.json",
    "semextensao",
    "arquivo.xyz",
    ".oculto",
]

PASTA.mkdir(exist_ok=True)

for nome in ARQUIVOS:
    (PASTA / nome).write_text("arquivo de teste", encoding="utf-8")

print(f"{len(ARQUIVOS)} arquivos criados em: {PASTA}")