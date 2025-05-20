import sqlite3
from typing import Iterator, Tuple, Any

CAMINHO_BD = 'DiagPlus.db'

def obter_conexao() -> sqlite3.Connection:
    conn = sqlite3.connect(CAMINHO_BD)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def executar_query(query: str, parametros: Tuple[Any, ...] = ()) -> Iterator[Tuple]:
    with obter_conexao() as conn:
        cursor = conn.execute(query, parametros)
        for row in cursor:
            yield row

def executar_comando(comando: str, parametros: Tuple[Any, ...] = ()) -> None:
    with obter_conexao() as conn:
        conn.execute(comando, parametros)
        conn.commit()
