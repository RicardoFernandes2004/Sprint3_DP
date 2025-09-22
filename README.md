
# Relatório Técnico — Estruturas e Algoritmos aplicados ao controle de consumo de insumos

**Curso/Disciplina**: Dynamic Programming <br>
**Tema**: Baixa visibilidade no apontamento de consumo nas unidades de diagnóstico  
**Linguagem**: Python 3 <br>
**Autores**: Ricardo Fernandes de Aquino (RM 554597), Kauã Soares Guimarães(RM 559044), Ana Clara Melo de Sousa (RM 559021), Gustavo Jun Irizawa Ikeda (RM 554718), Yasmin Bezerra Sobral (RM 558757)  

---

## 1. Contexto e Problema
Nas unidades de diagnóstico, o consumo diário de insumos (reagentes e descartáveis) não é registrado com precisão,
dificultando o controle de estoque e a previsão de reposição. O objetivo desta entrega é **demonstrar** — via simulação —
estruturas de dados e algoritmos clássicos que ajudam a **organizar** e **consultar** rapidamente esses dados de consumo.

> Este relatório descreve **como** cada estrutura/algoritmo foi aplicada ao problema. O código-fonte está em um único arquivo (`sim_estoque_algoritmos.py`).

---

## 2. Objetivos de Aprendizado
- Aplicar **Fila (FIFO)** para registrar eventos em **ordem cronológica** (chegada → saída).
- Aplicar **Pilha (LIFO)** para consultar os **últimos eventos** (ex.: incidentes mais recentes).
- Comparar **Buscas**: **Linear** (varredura completa) vs **Binária** (após ordenação).
- Comparar **Ordenações**: **Merge Sort** (estável) vs **Quick Sort** (rápido em média).
- Discutir **complexidades** e impactos práticos no cenário de estoque/consumo.

---

## 3. Metodologia de Simulação
1. **Geração de insumos**: cria-se uma lista de `N` insumos com códigos `INS-001..N` e **validade** (apenas para fins didáticos,
   real seria por lote).
2. **Simulação de consumo diário** por `D` dias: gera **eventos** (insumo + quantidade) aproximando
   um volume médio diário (`--mean-events`). Os eventos entram em uma **Fila** em ordem temporal.
3. **Processamento**: a fila é esvaziada em um **livro cronológico** (lista ordenada por data).
4. **Consultas**: constroem-se **Pilhas** para visualização dos últimos `k` eventos;
   **Buscas** para localizar eventos de um insumo; **Ordenações** para listar **top consumo** e **validade mais próxima**.

Parâmetros de simulação são **opcionais** e passados via CLI (ver <a href="https://github.com/RicardoFernandes2004/Sprint3_DP/blob/master/README.md">README</a>).

---

## 4. Estruturas e Algoritmos — uso no contexto do problema

### 4.1 Fila (Queue – FIFO)
- **Uso**: registrar o **fluxo diário** de consumo em ordem de ocorrência. Cada evento (data, código do insumo, quantidade)
  entra ao final da fila e sai pela frente, preservando a **cronologia**.
- **Benefício**: evita misturar eventos, permitindo **reconstruir o dia** e consolidar consumo por período.
- **Custo**: `enqueue`/`dequeue` em **O(1)** amortizado (deque).

### 4.2 Pilha (Stack – LIFO)
- **Uso**: visualizar rapidamente **o que aconteceu por último** (ex.: verificação de consumo recente, auditoria).
- **Operações**: `push` ao carregar o livro; `peek/pop` para acessar/remover **mais recente**.
- **Custo**: `push`/`pop`/`peek` em **O(1)** amortizado.

### 4.3 Buscas (Linear vs Binária)
- **Linear**: varre todo o livro, útil quando **dados não estão ordenados** ou o conjunto é pequeno.
  - **Custo**: **O(n)**.
- **Binária**: após ordenar o livro por `supply_code`, encontra **intervalos** de eventos do insumo alvo com **O(log n)** para localizar o início,
  e iteração sequencial sobre os vizinhos iguais.
  - **Custo**: **O(log n)** (localização) **+** tempo linear no número de ocorrências. Requer ordenação prévia em **O(n log n)**.

### 4.4 Ordenações (Merge Sort vs Quick Sort)
- **Merge Sort**: **estável**, **O(n log n)**, **O(n)** espaço extra. Bom para **relatórios** onde estabilidade importa.
- **Quick Sort**: **médio O(n log n)** e pouca memória, mas **pior caso O(n²)**. Bom para ordenar **in-memory** com médias boas.

**Aplicações no problema:**
- **Top consumo por insumo (desc)** → ordenar pares `(supply_code, total_consumido)` por `-total`.
- **Validade mais próxima (FEFO)** → ordenar insumos por `expiry` ascendente (consumir antes o que vence antes).

---

## 5. Resultados de uma execução de exemplo
Trecho do terminal ao executar:
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
2025-09-08 | INS-012 | qty=2
2025-09-08 | INS-011 | qty=12
2025-09-08 | INS-009 | qty=2
2025-09-09 | INS-010 | qty=7
2025-09-09 | INS-001 | qty=1
2025-09-09 | INS-002 | qty=4
2025-09-09 | INS-004 | qty=9
2025-09-09 | INS-010 | qty=1
... (+42 eventos)

========================================================================
PILHA (LIFO): CONSULTA DOS ÚLTIMOS EVENTOS
========================================================================
2025-09-17 | INS-006 | qty=7
2025-09-17 | INS-001 | qty=13
2025-09-17 | INS-001 | qty=4
2025-09-17 | INS-011 | qty=6
2025-09-17 | INS-009 | qty=4

========================================================================
BUSCA SEQUENCIAL (LINEAR)
========================================================================
Eventos do insumo INS-001 encontrados: 5
2025-09-09 | INS-001 | qty=1
2025-09-11 | INS-001 | qty=13
2025-09-12 | INS-001 | qty=12
2025-09-17 | INS-001 | qty=4
2025-09-17 | INS-001 | qty=13

========================================================================
BUSCA BINÁRIA (sobre ledger ordenado por supply_code)
========================================================================
Eventos do insumo INS-001 (binária): 5
2025-09-09 | INS-001 | qty=1
2025-09-11 | INS-001 | qty=13
2025-09-12 | INS-001 | qty=12
2025-09-17 | INS-001 | qty=4
2025-09-17 | INS-001 | qty=13

========================================================================
ORDENAÇÃO – TOP INSUMOS POR CONSUMO (DESC)
========================================================================
Merge Sort:
INS-011 | total_consumido=68
INS-005 | total_consumido=56
INS-002 | total_consumido=53
INS-006 | total_consumido=50
INS-001 | total_consumido=43
INS-004 | total_consumido=41
```

### 5.1 Top 10 — consumo por insumo (desc) — (Merge Sort)
| # | Código | Total consumido |
|---:|:------|-----------------:|
| 1 | INS-009 | 91 |
| 2 | INS-008 | 62 |
| 3 | INS-004 | 53 |
| 4 | INS-018 | 44 |
| 5 | INS-019 | 41 |
| 6 | INS-002 | 40 |
| 7 | INS-011 | 34 |
| 8 | INS-012 | 33 |
| 9 | INS-006 | 30 |
| 10 | INS-003 | 28 |


### 5.2 Validade mais próxima — Top 10 — (Merge Sort)
| # | Código | Nome | Validade |
|---:|:------|:-----|:---------|
| 1 | INS-003 | Insumo 003 | 2025-10-29 |
| 2 | INS-020 | Insumo 020 | 2025-10-30 |
| 3 | INS-014 | Insumo 014 | 2025-11-01 |
| 4 | INS-013 | Insumo 013 | 2025-11-02 |
| 5 | INS-010 | Insumo 010 | 2025-11-30 |
| 6 | INS-015 | Insumo 015 | 2025-12-03 |
| 7 | INS-008 | Insumo 008 | 2025-12-08 |
| 8 | INS-002 | Insumo 002 | 2025-12-13 |
| 9 | INS-007 | Insumo 007 | 2025-12-27 |
| 10 | INS-016 | Insumo 016 | 2026-02-05 |


> Observação: os valores variam conforme semente (`--seed`) e parâmetros.  
> A tabela usa `Merge Sort` para facilitar a reprodutibilidade, mas **Quick Sort** também está disponível no código.

---

## 6. Discussão e Limitações
- **Simplicações propositalmente didáticas**: validade por item (não por lote), ausência de cadastro de movimentos por usuário,
  e dados simulados.
- **Busca binária** exige **ordenação** prévia — ótima para muitas consultas de leitura.
- **Quick Sort** é rápido em média, porém instável; **Merge Sort** é estável e previsível.
- **Próximos passos** (caso fosse produto real):
  1. **Persistência** (ex.: banco relacional) e auditoria por usuário.
  2. Entradas **via leitor de código de barras/QR** por lote.
  3. **Alertas FEFO** e níveis mínimos por insumo.
  4. **Dashboards** com séries temporais e previsão de reposição.

---

## 7. Conclusão
A combinação de **Fila**, **Pilha**, **Buscas** e **Ordenações** resolve o problema de **visibilidade** no consumo sob a ótica
de **registro correto**, **consulta rápida** e **priorização** (FEFO). Mesmo sem persistência/banco, a prática evidencia
a relação entre as estruturas e as tarefas reais do almoxarifado/unidade de diagnóstico.

---

## 8. Evidências e Repositório
- Código-fonte (arquivo único): `sim_estoque_algoritmos.py` (Python 3).
- README com instruções e parâmetros de execução.
- Repositório GitHub: **<a href="https://github.com/RicardoFernandes2004/Sprint3_DP">Sprint3_DP</a>**.

