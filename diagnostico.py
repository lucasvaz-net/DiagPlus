from banco_dados import executar_query
from typing import Dict

def texto_para_vetor(texto: str) -> Dict[int, int]:
    vetor = {}
    for id_sintoma, descricao in executar_query("SELECT id, descricao FROM sintomas"):
        vetor[id_sintoma] = 1 if descricao.lower() in texto else 0
    return vetor

def comparar_e_diagnosticar(vetor: Dict[int, int]) -> int | None:
    melhor_id = None
    melhor_score = -1

    for id_doenca, in executar_query("SELECT id FROM doencas"):
        ids_sintomas = [s[0] for s in executar_query(
            "SELECT sintoma_id FROM doenca_sintoma WHERE doenca_id = ?", (id_doenca,)
        )]
        if not ids_sintomas:
            continue
        correspondentes = sum(vetor.get(s, 0) for s in ids_sintomas)
        score = correspondentes / len(ids_sintomas)
        if score > melhor_score:
            melhor_score = score
            melhor_id = id_doenca

    return melhor_id
