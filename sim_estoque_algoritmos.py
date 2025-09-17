
# DYNAMIC_PROGRAMMING_SPRINT
from __future__ import annotations

import argparse
from dataclasses import dataclass
from collections import deque
from typing import Callable, Iterable, List, Optional, Tuple, Any
from datetime import date, timedelta
import random

@dataclass(frozen=True)
class Supply:
    code: str
    name: str
    expiry: date 

@dataclass(frozen=True)
class ConsumptionEvent:
    when: date
    supply_code: str
    quantity: int

class ConsumptionQueue:
    def __init__(self) -> None:
        self._q: deque[ConsumptionEvent] = deque()

    def enqueue(self, ev: ConsumptionEvent) -> None:
        self._q.append(ev)

    def dequeue(self) -> ConsumptionEvent:
        return self._q.popleft()

    def empty(self) -> bool:
        return not self._q

    def __len__(self) -> int:
        return len(self._q)

class ConsumptionStack:
    def __init__(self) -> None:
        self._stack: List[ConsumptionEvent] = []

    def push(self, ev: ConsumptionEvent) -> None:
        self._stack.append(ev)

    def pop(self) -> ConsumptionEvent:
        return self._stack.pop()

    def peek(self) -> Optional[ConsumptionEvent]:
        return self._stack[-1] if self._stack else None

    def empty(self) -> bool:
        return not self._stack

    def __len__(self) -> int:
        return len(self._stack)

def generate_supplies(n: int, start: date, seed: int) -> List[Supply]:
    rnd = random.Random(seed)
    supplies: List[Supply] = []
    for i in range(1, n + 1):
        code = f"INS-{i:03d}"
        name = f"Insumo {i:03d}"
        validity_days = rnd.randint(30, 365)
        supplies.append(Supply(code, name, start + timedelta(days=validity_days)))
    return supplies

def simulate_daily_consumption(
    days: int,
    supplies: List[Supply],
    mean_events_per_day: int,
    max_qty: int,
    seed: int,
) -> ConsumptionQueue:
    rnd = random.Random(seed)
    q = ConsumptionQueue()
    start_day = date.today() - timedelta(days=days)
    for d in range(days):
        when = start_day + timedelta(days=d + 1)
        events_today = max(0, int(rnd.gauss(mean_events_per_day, max(1.0, mean_events_per_day * 0.25))))
        for _ in range(events_today):
            s = rnd.choice(supplies)
            qty = rnd.randint(1, max_qty)
            q.enqueue(ConsumptionEvent(when=when, supply_code=s.code, quantity=qty))
    return q

def process_queue(q: ConsumptionQueue) -> List[ConsumptionEvent]:
    ledger: List[ConsumptionEvent] = []
    while not q.empty():
        ledger.append(q.dequeue())
    return ledger

def build_stack(ledger: List[ConsumptionEvent]) -> ConsumptionStack:
    st = ConsumptionStack()
    for ev in ledger:
        st.push(ev)
    return st

def last_k_events(st: ConsumptionStack, k: int) -> List[ConsumptionEvent]:
    # snapshot sem destruir a pilha
    arr = list(st._stack)  # acesso controlado só para impressão
    return arr[-k:][::-1]

def linear_search(ledger: Iterable[ConsumptionEvent], predicate: Callable[[ConsumptionEvent], bool]) -> List[ConsumptionEvent]:
    return [ev for ev in ledger if predicate(ev)]

def binary_search_leftmost(sorted_list: List[Any], key: Callable[[Any], Any], target: Any) -> int:
    lo, hi = 0, len(sorted_list) - 1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        kv = key(sorted_list[mid])
        if kv < target:
            lo = mid + 1
        else:
            if kv == target:
                ans = mid
            hi = mid - 1
    return ans

def binary_search_events_by_supply(sorted_ledger: List[ConsumptionEvent], supply_code: str) -> List[ConsumptionEvent]:
    key = lambda ev: ev.supply_code
    idx = binary_search_leftmost(sorted_ledger, key, supply_code)
    if idx == -1:
        return []
    out: List[ConsumptionEvent] = []
    i = idx
    while i < len(sorted_ledger) and sorted_ledger[i].supply_code == supply_code:
        out.append(sorted_ledger[i])
        i += 1
    return out

def merge_sort(seq: List[Any], key: Callable[[Any], Any]) -> List[Any]:
    n = len(seq)
    if n <= 1:
        return list(seq)
    mid = n // 2
    left = merge_sort(seq[:mid], key)
    right = merge_sort(seq[mid:], key)
    i = j = 0
    merged: List[Any] = []
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:]); merged.extend(right[j:])
    return merged

def quick_sort(seq: List[Any], key: Callable[[Any], Any]) -> List[Any]:
    n = len(seq)
    if n <= 1:
        return list(seq)
    first, mid, last = seq[0], seq[n // 2], seq[-1]
    pivot = sorted([first, mid, last], key=key)[1]
    pv = key(pivot)
    less = [x for x in seq if key(x) < pv]
    equal = [x for x in seq if key(x) == pv]
    greater = [x for x in seq if key(x) > pv]
    return quick_sort(less, key) + equal + quick_sort(greater, key)

def aggregate_total_by_supply(ledger: Iterable[ConsumptionEvent]) -> List[Tuple[str, int]]:
    totals: dict[str, int] = {}
    for ev in ledger:
        totals[ev.supply_code] = totals.get(ev.supply_code, 0) + ev.quantity
    return list(totals.items())

def print_header(t: str) -> None:
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)

def print_events(evts: List[ConsumptionEvent], limit: int = 10) -> None:
    for ev in evts[:limit]:
        print(f"{ev.when.isoformat()} | {ev.supply_code} | qty={ev.quantity}")
    if len(evts) > limit:
        print(f"... (+{len(evts) - limit} eventos)")

def print_pairs(pairs: List[Tuple[str, int]], limit: int = 10) -> None:
    for code, total in pairs[:limit]:
        print(f"{code} | total_consumido={total}")
    if len(pairs) > limit:
        print(f"... (+{len(pairs) - limit} itens)")

def demo(supplies_n: int, days: int, mean_events: int, max_qty: int, seed: int, k_last: int) -> None:
    print_header("GERANDO DADOS SIMULADOS")
    base = date.today()
    supplies = generate_supplies(supplies_n, base, seed)
    q = simulate_daily_consumption(days, supplies, mean_events, max_qty, seed)
    print(f"Insumos: {len(supplies)} | Eventos gerados na FILA: {len(q)}")

    print_header("PROCESSANDO FILA (FIFO) -> LIVRO CRONOLÓGICO")
    ledger = process_queue(q)
    print_events(ledger, limit=10)

    print_header("PILHA (LIFO): CONSULTA DOS ÚLTIMOS EVENTOS")
    st = build_stack(ledger)
    recent = last_k_events(st, k_last)
    print_events(recent, limit=k_last)

    # Escolhe um insumo existente para buscas
    target_code = supplies[0].code

    print_header("BUSCA SEQUENCIAL (LINEAR)")
    found_linear = linear_search(ledger, lambda ev: ev.supply_code == target_code)
    print(f"Eventos do insumo {target_code} encontrados: {len(found_linear)}")
    print_events(found_linear, limit=5)

    print_header("BUSCA BINÁRIA (sobre ledger ordenado por supply_code)")
    ledger_by_code = merge_sort(ledger, key=lambda ev: ev.supply_code)  # ordena por código
    found_binary = binary_search_events_by_supply(ledger_by_code, target_code)
    print(f"Eventos do insumo {target_code} (binária): {len(found_binary)}")
    print_events(found_binary, limit=5)

    print_header("ORDENAÇÃO – TOP INSUMOS POR CONSUMO (DESC)")
    totals = aggregate_total_by_supply(ledger)
    by_qty_merge = merge_sort(totals, key=lambda p: -p[1])
    by_qty_quick = quick_sort(totals, key=lambda p: -p[1])
    print("Merge Sort:")
    print_pairs(by_qty_merge, limit=10)
    print("\nQuick Sort:")
    print_pairs(by_qty_quick, limit=10)

    print_header("ORDENAÇÃO – INSUMOS POR VALIDADE MAIS PRÓXIMA (FEFO)")
    by_expiry_merge = merge_sort(supplies, key=lambda s: s.expiry)
    by_expiry_quick = quick_sort(supplies, key=lambda s: s.expiry)
    print("Merge Sort (primeiros 10):")
    for s in by_expiry_merge[:10]:
        print(f"{s.code} | {s.name} | validade={s.expiry.isoformat()}")
    print("\nQuick Sort (primeiros 10):")
    for s in by_expiry_quick[:10]:
        print(f"{s.code} | {s.name} | validade={s.expiry.isoformat()}")

    print_header("COMPLEXIDADES (resumo)")
    print("- Fila/Pilha: enfileirar/empilhar e desenfileirar/desempilhar -> O(1) amortizado")
    print("- Busca Linear: O(n)")
    print("- Busca Binária: O(log n) após ordenação O(n log n)")
    print("- Merge Sort: O(n log n) tempo, O(n) espaço, estável")
    print("- Quick Sort: O(n log n) médio, O(n^2) pior caso, in-place lógico (versão funcional não)")

def main() -> None:
    parser = argparse.ArgumentParser(description="Simulador de algoritmos para controle de consumo de insumos.")
    parser.add_argument("--supplies", type=int, default=25, help="Quantidade de insumos simulados")
    parser.add_argument("--days", type=int, default=14, help="Quantidade de dias simulados")
    parser.add_argument("--mean-events", type=int, default=8, help="Média de eventos por dia")
    parser.add_argument("--max-qty", type=int, default=15, help="Quantidade máxima por evento")
    parser.add_argument("--seed", type=int, default=42, help="Seed RNG para reprodutibilidade")
    parser.add_argument("--k-last", type=int, default=5, help="Quantidade de últimos eventos a exibir (pilha)")
    args = parser.parse_args()
    demo(args.supplies, args.days, args.mean_events, args.max_qty, args.seed, args.k_last)

if __name__ == "__main__":
    main()
