
# Simulador de Estruturas & Algoritmos — Consumo de Insumos (Python)

**Objetivo:** demonstrar na prática o uso de **Fila (FIFO)**, **Pilha (LIFO)**, **Buscas (Linear/Binária)** e **Ordenações (Merge/Quick)**
no contexto do desafio “baixa visibilidade no consumo de insumos”. O projeto **não** gera relatório; apenas **simula** e **imprime** no terminal.
O relatório (PDF) é documento separado.

> Arquivo único: `sim_estoque_algoritmos.py`

---

## ✨ O que está implementado

- **Fila (Queue)** para registrar eventos de consumo em **ordem cronológica**.
- **Pilha (Stack)** para consultar **últimos _k_ eventos** rapidamente.
- **Busca sequencial (linear)** por insumo.
- **Busca binária** após ordenar o livro por `supply_code`.
- **Ordenação** com **Merge Sort** (estável) e **Quick Sort** (médio O(n log n)):
  - *Top insumos por quantidade consumida (desc)*.
  - *Insumos por validade mais próxima (FEFO)*.
- **Gerador de dados** reprodutível (usa `--seed`).

---

## 🧰 Requisitos
- Python **3.8+** (recomendado 3.10+).
- Nenhuma biblioteca externa.

> Dica: se quiser, crie um venv (opcional):
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

---

## ▶️ Como executar (padrão)

Na pasta do arquivo:

```bash
python sim_estoque_algoritmos.py
```

Isso já:
1) Gera insumos e eventos simulados.
2) Processa a **fila** → livro cronológico.
3) Mostra **últimos k** eventos via **pilha**.
4) Demonstra **busca linear** e **binária**.
5) Ordena por **quantidade** e por **validade** (Merge/Quick).

---

## ⚙️ Parâmetros opcionais (e como passar)

| Flag            | Descrição                                     | Padrão |
|-----------------|-----------------------------------------------|--------|
| `--supplies`    | Quantidade de insumos simulados               | `25`   |
| `--days`        | Número de dias simulados                      | `14`   |
| `--mean-events` | Média de eventos/dia                          | `8`    |
| `--max-qty`     | Máximo de unidades por evento                 | `15`   |
| `--seed`        | Semente do gerador de aleatoriedade           | `42`   |
| `--k-last`      | Quantos últimos eventos exibir (pilha)        | `5`    |

Você pode informar **qualquer combinação** dessas flags. Exemplos por shell/OS:

### Linux/macOS (bash/zsh)
```bash
python sim_estoque_algoritmos.py --supplies 40 --days 20 --mean-events 10 --max-qty 25 --seed 2025 --k-last 8
```

### Windows — PowerShell
```powershell
python .\sim_estoque_algoritmos.py --supplies 40 --days 20 --mean-events 10 --max-qty 25 --seed 2025 --k-last 8
```

### Windows — CMD
```cmd
python sim_estoque_algoritmos.py --supplies 40 --days 20 --mean-events 10 --max-qty 25 --seed 2025 --k-last 8
```

Exemplos rápidos:
```bash
# Só quero ver mais "últimos eventos" na pilha
python sim_estoque_algoritmos.py --k-last 12

# Quero reduzir o dataset (mais rápido)
python sim_estoque_algoritmos.py --supplies 10 --days 7 --mean-events 5 --k-last 5
```

---

## 🧪 Saída esperada (trecho)

```text
========================================================================
GERANDO DADOS SIMULADOS
========================================================================
Insumos: 12 | Eventos gerados na FILA: 52

========================================================================
PROCESSANDO FILA (FIFO) -> LIVRO CRONOLÓGICO
========================================================================
2025-09-08 | INS-005 | qty=4
2025-09-08 | INS-004 | qty=3
...

========================================================================
BUSCA BINÁRIA (sobre ledger ordenado por supply_code)
========================================================================
Eventos do insumo INS-001 (binária): 6
2025-09-10 | INS-001 | qty=9
...
```

> Observação: os valores mudam conforme a `--seed` e os parâmetros.

---

## 🧠 Complexidades (resumo)

- **Fila/Pilha**: operações básicas em **O(1)** (amortizado).
- **Busca Linear**: **O(n)**.
- **Busca Binária**: **O(log n)** (após ordenar em **O(n log n)**).
- **Merge Sort**: **O(n log n)** tempo, **O(n)** espaço, *estável*.
- **Quick Sort**: **O(n log n)** (médio), **O(n²)** (pior caso), normalmente *in-place* (aqui versão funcional).

---

## 🧾 Notas de uso didático

- A validade está simplificada por item (em cenários reais, é por **lote**).
- A simulação usa distribuição aproximada (gaussiana) para volumetria diária.
- **Relatório** exigido pelo desafio é um **PDF separado** (este projeto foca só na simulação/algoritmos).

---

## 📂 Estrutura do projeto
```
.
└── sim_estoque_algoritmos.py
```
