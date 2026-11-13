"""Organizador de arquivos: separa os arquivos de uma pasta em subpastas por tipo."""

import argparse
import logging
import shutil
from pathlib import Path

ARQUIVO_LOG = Path(__file__).parent / "organizador.log"
PASTA_OUTROS = "outros"

CATEGORIAS = {
    "imagens": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".md"},
    "planilhas": {".xls", ".xlsx", ".csv"},
    "apresentacoes": {".ppt", ".pptx"},
    "videos": {".mp4", ".mkv", ".avi", ".mov"},
    "audios": {".mp3", ".wav", ".ogg"},
    "compactados": {".zip", ".rar", ".7z"},
    "codigo": {".py", ".js", ".html", ".css", ".json"},
}


def configurar_log():
    """Configura o log para aparecer na tela e ser gravado em arquivo."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(ARQUIVO_LOG, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def descobrir_categoria(arquivo):
    """Devolve o nome da categoria de um arquivo, de acordo com a extensão."""
    extensao = arquivo.suffix.lower()
    for categoria, extensoes in CATEGORIAS.items():
        if extensao in extensoes:
            return categoria
    return PASTA_OUTROS


def gerar_destino_livre(destino):
    """Se já existir um arquivo com esse nome, acrescenta _1, _2, _3..."""
    if not destino.exists():
        return destino
    contador = 1
    while True:
        candidato = destino.with_name(f"{destino.stem}_{contador}{destino.suffix}")
        if not candidato.exists():
            return candidato
        contador += 1


def organizar(pasta, dry_run=False):
    """Move cada arquivo da pasta para a subpasta da sua categoria.

    Devolve uma tupla (quantidade de arquivos movidos, quantidade de erros).
    """
    movidos = 0
    erros = 0

    for item in sorted(pasta.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue

        pasta_destino = pasta / descobrir_categoria(item)
        destino = gerar_destino_livre(pasta_destino / item.name)

        if dry_run:
            logging.info("[SIMULAÇÃO] %s -> %s", item.name, destino.relative_to(pasta))
            movidos += 1
            continue

        try:
            pasta_destino.mkdir(exist_ok=True)
            shutil.move(str(item), str(destino))
            logging.info("%s -> %s", item.name, destino.relative_to(pasta))
            movidos += 1
        except OSError as erro:
            logging.error("Falha ao mover %s: %s", item.name, erro)
            erros += 1

    return movidos, erros


def main():
    parser = argparse.ArgumentParser(
        description="Organiza os arquivos de uma pasta em subpastas por tipo."
    )
    parser.add_argument("pasta", help="caminho da pasta que será organizada")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="mostra o que seria feito, sem mover nenhum arquivo",
    )
    args = parser.parse_args()

    pasta = Path(args.pasta)
    if not pasta.is_dir():
        print(f"Erro: '{pasta}' não é uma pasta válida.")
        return

    if not args.dry_run:
        resposta = input(f"Mover os arquivos de '{pasta}'? (s/n): ")
        if resposta.strip().lower() != "s":
            print("Operação cancelada.")
            return

    configurar_log()
    modo = "SIMULAÇÃO" if args.dry_run else "EXECUÇÃO"
    logging.info("Iniciando organização de '%s' (%s)", pasta, modo)

    movidos, erros = organizar(pasta, args.dry_run)

    logging.info("Concluído: %d arquivo(s) processado(s), %d erro(s).", movidos, erros)


if __name__ == "__main__":
    main()