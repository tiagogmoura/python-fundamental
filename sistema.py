"""
Sistema de Gerenciamento de Contatos
=====================================
Requisitos atendidos:
  - Login
  - CRUD: Cadastrar, Consultar, Alterar, Excluir
  - Saída: exibição na tela e gravação em arquivo CSV
"""

import csv
import os

# ---------------------------------------------------------------------------
# Configurações de login
# ATENÇÃO: estas credenciais são apenas para fins didáticos.
# Em produção, use variáveis de ambiente ou senhas com hash (ex.: bcrypt).
# Substitua pelo valor da variável de ambiente se ela estiver definida:
#   SISTEMA_ADMIN_SENHA  →  senha do usuário "admin"
#   SISTEMA_USER_SENHA   →  senha do usuário "usuario"
# ---------------------------------------------------------------------------
USUARIOS = {
    "admin": os.environ.get("SISTEMA_ADMIN_SENHA", "1234"),
    "usuario": os.environ.get("SISTEMA_USER_SENHA", "senha"),
}

# ---------------------------------------------------------------------------
# Dados em memória  (id -> dict)
# ---------------------------------------------------------------------------
contatos: dict[int, dict] = {}
_proximo_id = 1

ARQUIVO_CSV = "contatos.csv"


# ---------------------------------------------------------------------------
# Utilitários de tela
# ---------------------------------------------------------------------------

def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    input("\nPressione ENTER para continuar...")


def cabecalho(titulo: str) -> None:
    print("\n" + "=" * 50)
    print(f"  {titulo}")
    print("=" * 50)


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def fazer_login() -> bool:
    """Solicita credenciais e retorna True se o login for bem-sucedido."""
    limpar_tela()
    cabecalho("LOGIN DO SISTEMA")
    tentativas = 3
    while tentativas > 0:
        usuario = input("Usuário: ").strip()
        senha = input("Senha  : ").strip()
        if USUARIOS.get(usuario) == senha:
            print(f"\nBem-vindo, {usuario}!")
            pausar()
            return True
        tentativas -= 1
        restantes = tentativas
        print(f"Credenciais inválidas. Tentativas restantes: {restantes}")
    print("Número máximo de tentativas atingido. Encerrando.")
    return False


# ---------------------------------------------------------------------------
# CRUD — Cadastrar
# ---------------------------------------------------------------------------

def cadastrar_contato() -> None:
    global _proximo_id
    limpar_tela()
    cabecalho("CADASTRAR CONTATO")
    nome = input("Nome      : ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        pausar()
        return
    email = input("E-mail    : ").strip()
    telefone = input("Telefone  : ").strip()
    # O campo "id" é incluído no dict para facilitar a exportação CSV e exibição em tabela.
    contatos[_proximo_id] = {"id": _proximo_id, "nome": nome, "email": email, "telefone": telefone}
    print(f"\nContato '{nome}' cadastrado com ID {_proximo_id}.")
    _proximo_id += 1
    pausar()


# ---------------------------------------------------------------------------
# CRUD — Consultar
# ---------------------------------------------------------------------------

def _exibir_tabela(registros: list[dict]) -> None:
    """Imprime os registros em formato de tabela simples."""
    if not registros:
        print("\nNenhum contato encontrado.")
        return
    print(f"\n{'ID':<5} {'Nome':<25} {'E-mail':<30} {'Telefone':<15}")
    print("-" * 78)
    for c in registros:
        print(f"{c['id']:<5} {c['nome']:<25} {c['email']:<30} {c['telefone']:<15}")


def consultar_contatos() -> None:
    limpar_tela()
    cabecalho("CONSULTAR CONTATOS")
    termo = input("Pesquisar por nome (deixe em branco para listar todos): ").strip().lower()
    if termo:
        resultado = [
            c for c in contatos.values()
            if termo in c["nome"].lower()
            or termo in c["email"].lower()
            or termo in c["telefone"].lower()
        ]
    else:
        resultado = list(contatos.values())
    _exibir_tabela(resultado)
    pausar()


# ---------------------------------------------------------------------------
# CRUD — Alterar
# ---------------------------------------------------------------------------

def alterar_contato() -> None:
    limpar_tela()
    cabecalho("ALTERAR CONTATO")
    _exibir_tabela(list(contatos.values()))
    if not contatos:
        pausar()
        return
    try:
        id_str = input("\nInforme o ID do contato a alterar: ").strip()
        cid = int(id_str)
    except ValueError:
        print("ID inválido.")
        pausar()
        return
    if cid not in contatos:
        print(f"Contato com ID {cid} não encontrado.")
        pausar()
        return
    c = contatos[cid]
    print(f"\nContato atual: {c['nome']} | {c['email']} | {c['telefone']}")
    print("(Deixe em branco para manter o valor atual)")
    novo_nome = input(f"Novo nome [{c['nome']}]: ").strip()
    novo_email = input(f"Novo e-mail [{c['email']}]: ").strip()
    novo_tel = input(f"Novo telefone [{c['telefone']}]: ").strip()
    if novo_nome:
        c["nome"] = novo_nome
    if novo_email:
        c["email"] = novo_email
    if novo_tel:
        c["telefone"] = novo_tel
    print(f"\nContato ID {cid} atualizado com sucesso.")
    pausar()


# ---------------------------------------------------------------------------
# CRUD — Excluir
# ---------------------------------------------------------------------------

def excluir_contato() -> None:
    limpar_tela()
    cabecalho("EXCLUIR CONTATO")
    _exibir_tabela(list(contatos.values()))
    if not contatos:
        pausar()
        return
    try:
        id_str = input("\nInforme o ID do contato a excluir: ").strip()
        cid = int(id_str)
    except ValueError:
        print("ID inválido.")
        pausar()
        return
    if cid not in contatos:
        print(f"Contato com ID {cid} não encontrado.")
        pausar()
        return
    nome = contatos[cid]["nome"]
    confirmacao = input(f"Confirma exclusão de '{nome}'? (s/N): ").strip().lower()
    if confirmacao == "s":
        del contatos[cid]
        print(f"Contato '{nome}' excluído com sucesso.")
    else:
        print("Operação cancelada.")
    pausar()


# ---------------------------------------------------------------------------
# Saída — Gravar em arquivo CSV
# ---------------------------------------------------------------------------

def exportar_csv() -> None:
    limpar_tela()
    cabecalho("EXPORTAR PARA ARQUIVO CSV")
    if not contatos:
        print("Nenhum contato para exportar.")
        pausar()
        return
    with open(ARQUIVO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nome", "email", "telefone"])
        writer.writeheader()
        writer.writerows(contatos.values())
    caminho = os.path.abspath(ARQUIVO_CSV)
    print(f"\n{len(contatos)} contato(s) exportado(s) para:\n  {caminho}")
    pausar()


# ---------------------------------------------------------------------------
# Menu principal
# ---------------------------------------------------------------------------

MENU = """
  [1] Cadastrar contato
  [2] Consultar contatos
  [3] Alterar contato
  [4] Excluir contato
  [5] Exportar para CSV
  [0] Sair
"""


def menu_principal() -> None:
    acoes = {
        "1": cadastrar_contato,
        "2": consultar_contatos,
        "3": alterar_contato,
        "4": excluir_contato,
        "5": exportar_csv,
    }
    while True:
        limpar_tela()
        cabecalho("SISTEMA DE GERENCIAMENTO DE CONTATOS")
        print(MENU)
        opcao = input("Opção: ").strip()
        if opcao == "0":
            print("\nAté logo!")
            break
        acao = acoes.get(opcao)
        if acao:
            acao()
        else:
            print("Opção inválida. Tente novamente.")
            pausar()


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    if fazer_login():
        menu_principal()


if __name__ == "__main__":
    main()
