import numpy as np
import random
import math
from typing import List

# ====================================================
# Classe que representa uma solução de alocação de turmas em salas/horários
# ====================================================
class Solucao:
    def __init__(self, horarios: int, salas: int):
        # Matriz (horário x sala), inicialmente com todas células vazias (-1)
        self.matriz = np.full((horarios, salas), fill_value=-1, dtype=int)

    def alocar(self, horario: int, sala: int, turma: int):
        self.matriz[horario, sala] = turma

    def desalocar(self, horario: int, sala: int):
        self.matriz[horario, sala] = -1

    def get(self, horario: int, sala: int) -> int:
        return self.matriz[horario, sala]

    def copiar(self):
        nova = Solucao(*self.matriz.shape)
        nova.matriz = self.matriz.copy()
        return nova

# ====================================================
# Dados sintéticos: turmas com horários e número de alunos
# Salas com capacidade e horários indisponíveis
# ====================================================
turmas = [
    {"id": 1, "alunos": 40, "horarios": [1, 2]},
    {"id": 2, "alunos": 25, "horarios": [2, 3]},
    {"id": 3, "alunos": 60, "horarios": [3, 4]},
    {"id": 4, "alunos": 35, "horarios": [1, 4]},
]

salas = [
    {"id": 0, "capacidade": 30, "indisponiveis": [3]},
    {"id": 1, "capacidade": 50, "indisponiveis": []},
    {"id": 2, "capacidade": 70, "indisponiveis": [2]},
]

NUM_HORARIOS = 5
NUM_SALAS = len(salas)

# ====================================================
# Avaliação de uma solução: f(s) = 100*g(s) + h(s)
# Penaliza violações essenciais fortemente (g)
# Penaliza desperdício de espaço levemente (h)
# ====================================================
def avaliar(solucao: Solucao, turmas: List[dict], salas: List[dict]) -> float:
    g = 0  # penalidades essenciais
    h = 0  # penalidades não essenciais

    for sala_idx, sala in enumerate(salas):
        for hora in range(solucao.matriz.shape[0]):
            turma_id = solucao.get(hora, sala_idx)
            if turma_id == -1:
                continue

            turma = next((t for t in turmas if t["id"] == turma_id), None)
            if not turma:
                continue

            # (a) Mais de uma sala com mesma turma no mesmo horário (erro)
            if np.sum(solucao.matriz[hora] == turma_id) > 1:
                g += 1

            # (b) Capacidade da sala menor que número de alunos (erro)
            if turma["alunos"] > sala["capacidade"]:
                g += 1

            # (c) Sala indisponível nesse horário (erro)
            if hora in sala["indisponiveis"]:
                g += 1

            # (f) Penalidade leve: desperdício de espaço
            h += abs(sala["capacidade"] - turma["alunos"]) ** 0.5

    return 100 * g + h  # Mais peso para g(s)

# ====================================================
# Geração de uma solução vizinha: troca de turmas entre duas salas no mesmo horário
# ====================================================
def gerar_vizinho(solucao: Solucao) -> Solucao:
    novo = solucao.copiar()
    horario = random.randint(0, novo.matriz.shape[0] - 1)
    sala1, sala2 = random.sample(range(novo.matriz.shape[1]), 2)

    t1 = novo.get(horario, sala1)
    t2 = novo.get(horario, sala2)
    novo.matriz[horario, sala1], novo.matriz[horario, sala2] = t2, t1

    return novo

# ====================================================
# Simulated Annealing
# ====================================================
def simulated_annealing(solucao_inicial, turmas, salas, T0=1000, alpha=0.95, max_iter=100):
    s = solucao_inicial
    melhor = s.copiar()
    T = T0

    while T > 1:
        for _ in range(max_iter):
            vizinho = gerar_vizinho(s)
            delta = avaliar(vizinho, turmas, salas) - avaliar(s, turmas, salas)
            if delta < 0 or random.random() < math.exp(-delta / T):
                s = vizinho
                if avaliar(s, turmas, salas) < avaliar(melhor, turmas, salas):
                    melhor = s.copiar()
        T *= alpha
    return melhor

# ====================================================
# Busca Tabu
# ====================================================
def busca_tabu(solucao_inicial, turmas, salas, max_iter=200, tamanho_tabu=10):
    s = solucao_inicial
    melhor = s.copiar()
    lista_tabu = []

    for _ in range(max_iter):
        vizinhos = [gerar_vizinho(s) for _ in range(30)]
        vizinhos = [v for v in vizinhos if str(v.matriz) not in lista_tabu]

        if not vizinhos:
            continue

        vizinho_melhor = min(vizinhos, key=lambda v: avaliar(v, turmas, salas))

        if avaliar(vizinho_melhor, turmas, salas) < avaliar(melhor, turmas, salas):
            melhor = vizinho_melhor.copiar()

        s = vizinho_melhor

        lista_tabu.append(str(s.matriz))
        if len(lista_tabu) > tamanho_tabu:
            lista_tabu.pop(0)

    return melhor

# ====================================================
# Construção da solução inicial com base em GRASP
# ====================================================
def gerar_solucao_inicial(horarios: int, salas: List[dict], turmas: List[dict]) -> Solucao:
    solucao = Solucao(horarios, len(salas))
    for turma in turmas:
        for h in turma["horarios"]:
            candidatos = [i for i, sala in enumerate(salas)
                          if h not in sala["indisponiveis"]
                          and solucao.get(h, i) == -1]
            sala_escolhida = random.choice(candidatos) if candidatos else random.randint(0, len(salas) - 1)
            solucao.alocar(h, sala_escolhida, turma["id"])
    return solucao

# ====================================================
# Algoritmo híbrido: Simulated Annealing + Busca Tabu
# ====================================================
def algoritmo_hibrido(turmas, salas):
    inicial = gerar_solucao_inicial(NUM_HORARIOS, salas, turmas)
    s1 = simulated_annealing(inicial, turmas, salas)
    s2 = busca_tabu(s1, turmas, salas)
    return s2

# ====================================================
# Execução principal
# ====================================================
if __name__ == "__main__":
    random.seed(42)

    # Solução inicial
    inicial = gerar_solucao_inicial(NUM_HORARIOS, salas, turmas)
    print("Avaliação inicial:", avaliar(inicial, turmas, salas))

    # Aplicando algoritmo híbrido
    final = algoritmo_hibrido(turmas, salas)
    print("Avaliação final (híbrido SA+BT):", avaliar(final, turmas, salas))
    print("\nMatriz final de alocação (linha = horário, coluna = sala):")
    print(final.matriz)
