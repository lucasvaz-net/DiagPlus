import hashlib
from banco_dados import executar_query, executar_comando

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def registrar(nome_usuario: str, senha: str) -> bool:
    senha_hash = hash_senha(senha)
    try:
        executar_comando(
            "INSERT INTO usuarios (nome_usuario, senha_hash) VALUES (?, ?)",
            (nome_usuario, senha_hash)
        )
        return True
    except Exception:
        return False

def efetuar_login(nome_usuario: str, senha: str) -> int | None:
    senha_hash = hash_senha(senha)
    resultado = list(executar_query(
        "SELECT id FROM usuarios WHERE nome_usuario = ? AND senha_hash = ?",
        (nome_usuario, senha_hash)
    ))
    return resultado[0][0] if resultado else None
