# Alocação de Salas com Simulated Annealing + Busca Tabu

Este repositório contém a implementação de técnicas de **Simulated Annealing (SA)** e **Busca Tabu (BT)** para resolver o problema de **alocação de turmas em salas e horários** em uma instituição de ensino.

> **Autores:**  
> 👤 Willian Bortolini  
> 👤 Kaiky Cunha

---

## 🎯 Objetivo

Alocar turmas com diferentes demandas e horários em salas disponíveis, respeitando:

- Capacidade das salas
- Indisponibilidade de horários
- Redução de conflitos e sobreposição
- Eficiência no uso de espaço

---

## 🧠 Técnicas utilizadas

- **Simulated Annealing (SA):** Permite explorar soluções não ótimas temporariamente, escapando de ótimos locais.
- **Busca Tabu (BT):** Utiliza uma lista tabu para evitar ciclos e aprimora a solução local.
- **Híbrido SA + BT:** Primeiro aplica SA para escapar de ótimos locais, depois refina com BT.

---

## 🧪 Exemplo de execução

```bash
python alocacao_salas.py
```

Exemplo de saída:

```
Avaliação inicial: 343.23
Avaliação final (híbrido SA+BT): 108.12

Matriz final de alocação (linha = horário, coluna = sala):
[[-1 -1 -1]
 [-1  1  4]
 [ 2  1 -1]
 [-1  2  3]
 [-1  4  3]]
```

---

## 🛠️ Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/TP2-AlocacaoSalas.git
cd TP2-AlocacaoSalas
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install numpy
```

### 4. Executar

```bash
python alocacao_salas.py
```

---

## 📁 Estrutura do projeto

- `alocacao_salas.py` — Código principal com a lógica de solução
- `.gitignore` — Ignora a pasta `venv/`
- `README.md` — Este arquivo

---

## 📄 Licença

Este projeto é de uso exclusivamente acadêmico.
