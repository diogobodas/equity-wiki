#!/usr/bin/env python
"""Generate data for slides 10 and 13: Distratos + VSO + Riva rentabilidade."""

import re
import numpy as np

FILE_HB = "sources/full/generic/HB_historical series_4Q25.md"
FILE_DIR = "sources/undigested/Planilha interativa (11)_extracted.md"

COMPANIES_ALL = {"EZTec", "Even", "Helbor", "Lavvi", "Melnick", "Mitre", "Trisul",
    "Tecnisa", "PDG", "Cyrela", "Moura Dubeux", "Rossi", "Gafisa",
    "Tenda", "Cury", "Direcional", "MRV", "Plano & Plano", "Total"}


def parse_hb_block(lines, metric_label, targets, start=0):
    data = {}
    col_map = {}
    found = False
    for i in range(start, min(start + 500, len(lines))):
        line = lines[i]
        if metric_label in line and line.startswith('|'):
            found = True
            cols = [c.strip() for c in line.split('|')]
            for j, c in enumerate(cols):
                if re.match(r'^[1-4]Q\d{2}$', c.strip()):
                    col_map[j] = c.strip()
            continue
        if not found:
            continue
        if not line.startswith('|'):
            continue
        cols = [c.strip() for c in line.split('|')]
        if len(cols) < 3:
            continue
        co = cols[1].strip()
        if co in targets:
            vals = {}
            for j, p in col_map.items():
                if j < len(cols):
                    try:
                        v = float(cols[j].strip())
                        if not np.isnan(v):
                            vals[p] = v
                    except (ValueError, TypeError):
                        pass
            data[co] = vals
        elif co not in COMPANIES_ALL and co != 'NaN' and not co.startswith('---') and found and len(data) >= len(targets):
            break
    return data


with open(FILE_HB, encoding='utf-8') as f:
    hb_lines = f.readlines()
with open(FILE_DIR, encoding='utf-8') as f:
    dir_lines = f.readlines()

# ===================================================================
# SLIDE 10: Distratos como % de vendas brutas
# ===================================================================
print("=" * 70)
print("SLIDE 10: Distratos/Vendas Brutas - Cury vs Direcional")
print("Distratos = |Cancelamentos| / (Vendas Liquidas + |Cancelamentos|)")
print("=" * 70)

targets = {"Cury", "Direcional"}
cancellations = parse_hb_block(hb_lines, "| CANCELLATIONS |", targets, start=100)
net_sales = parse_hb_block(hb_lines, "# NET SALES (CO%)", targets, start=100)

for co in ["Direcional", "Cury"]:
    c = cancellations.get(co, {})
    n = net_sales.get(co, {})
    common = sorted(set(c.keys()) & set(n.keys()), key=lambda p: (int(p[2:]), int(p[0])))
    recent = [p for p in common if int(p[2:]) >= 19]

    print(f"\n{co}:")
    print(f"  {'Tri':>6s}  {'Cancel':>10s}  {'VL':>10s}  {'VB':>10s}  {'Dist%':>7s}")
    for p in recent:
        cancel = abs(c[p])
        ns = n[p]
        gross = ns + cancel
        pct = cancel / gross * 100 if gross > 0 else 0
        print(f"  {p:>6s}  {cancel/1000:>9.0f}k  {ns/1000:>9.0f}k  {gross/1000:>9.0f}k  {pct:>6.1f}%")

# ===================================================================
# SLIDE 13a: VSO Direcional MCMV vs Consolidada
# ===================================================================
print("\n\n" + "=" * 70)
print("SLIDE 13a: VSO Trimestral - MCMV vs Consolidada (inclui Riva)")
print("=" * 70)

# Parse header from Dados Operacionais
header = [c.strip() for c in dir_lines[9].split('|')]
col_periods = {}
for j, h in enumerate(header):
    if re.match(r'^[1-4]T\d{2}$', h):
        col_periods[j] = h

for line in dir_lines[30:40]:
    cols = [c.strip() for c in line.split('|')]
    if len(cols) < 3:
        continue
    label = cols[1].strip() if len(cols) > 1 else ""
    if "VSO" in label:
        vals = {}
        for j, p in col_periods.items():
            if j < len(cols):
                try:
                    v = float(cols[j].strip())
                    if not np.isnan(v):
                        vals[p] = v
                except (ValueError, TypeError):
                    pass

        recent = sorted(vals.keys(), key=lambda p: (int(p[2:]), int(p[0])))
        recent = [p for p in recent if int(p[2:]) >= 19]
        short_label = "MCMV" if "MCMV" in label else "Consolidada"
        print(f"\n  {short_label}:")
        print(f"  {'Tri':>6s}  {'VSO':>8s}")
        for p in recent:
            print(f"  {p:>6s}  {vals[p]*100:>7.1f}%")

print(f"\n  1T26 (previa operacional): VSO Consolidada recorde ~24%")
print(f"  Nota: diferenca MCMV vs Consolidada = efeito Riva (VSO mais baixa)")

# ===================================================================
# SLIDE 13b: Rentabilidade Direcional Consolidada vs Riva
# ===================================================================
print("\n\n" + "=" * 70)
print("SLIDE 13b: Rentabilidade - Direcional Consolidada vs Riva")
print("=" * 70)

# RIVA DRE (from lines 162-174)
# Indices: [0]=2025, [1]=4T25, [2]=3T25, [3]=2T25, [4]=1T25, [5]=2024, [6]=4T24, [7]=3T24, [8]=2T24, [9]=1T24
riva_receita =     [1678076, 499877, 487159, 365306, 325734, 1192444, 345642, 323832, 279665, 243305]
riva_lb =          [681014, 204351, 203345, 142403, 130916, 427806, 122862, 121079, 96385, 87480]
riva_ll =          [457723, 142441, 140509, 90625, 84148, 279271, 75033, 80237, 55180, 68821]
riva_pl =          [800457, 800457, 788718, 795868, 714445, 774145, 774145, 695681, 666825, 602751]

# Parse Direcional Consolidada DRE (lines 57-78)
dir_dre = {}
for line in dir_lines[57:78]:
    cols = [c.strip() for c in line.split('|')]
    if len(cols) < 8:
        continue
    label = cols[1].strip() if len(cols) > 1 else ""
    if label in ["RECEITA OPERACIONAL LIQUIDA", "LUCRO BRUTO", "RESULTADO LIQUIDO DO PERIODO",
                  "RECEITA OPERACIONAL L\u00cdQUIDA", "LUCRO BRUTO", "RESULTADO L\u00cdQUIDO DO PER\u00cdODO"]:
        vals = []
        for j in range(2, min(12, len(cols))):
            try:
                vals.append(float(cols[j].strip()))
            except (ValueError, TypeError):
                vals.append(None)
        dir_dre[label] = vals

# Let me just print labels to debug
print("\nDRE labels found:", list(dir_dre.keys()))

qi = [1, 2, 3, 4, 6, 7]  # quarterly indices: 4T25, 3T25, 2T25, 1T25, 4T24, 3T24
qs = ["4T25", "3T25", "2T25", "1T25", "4T24", "3T24"]

# Find the right keys
rec_key = None
lb_key = None
ll_key = None
for k in dir_dre:
    if "RECEITA" in k:
        rec_key = k
    elif "LUCRO BRUTO" in k:
        lb_key = k
    elif "RESULTADO" in k and "QUIDO" in k:
        ll_key = k

header_str = "  " + "".join(f"  {q:>8s}" for q in qs)
print(f"\n{header_str}")
print("  " + "-" * 60)

print(f"\n  RECEITA (R$ mm):")
print(f"    {'Riva':14s}", end="")
for i in qi:
    print(f"  {riva_receita[i]/1000:>8.0f}", end="")
print()

if rec_key:
    dr = dir_dre[rec_key]
    print(f"    {'Consolidada':14s}", end="")
    for i in qi:
        if i < len(dr) and dr[i]:
            print(f"  {dr[i]/1000:>8.0f}", end="")
        else:
            print(f"  {'N/A':>8s}", end="")
    print()
    print(f"    {'Dir ex-Riva':14s}", end="")
    for i in qi:
        if i < len(dr) and dr[i]:
            print(f"  {(dr[i]-riva_receita[i])/1000:>8.0f}", end="")
        else:
            print(f"  {'N/A':>8s}", end="")
    print()
    print(f"    {'Riva % Consol':14s}", end="")
    for i in qi:
        if i < len(dr) and dr[i]:
            print(f"  {riva_receita[i]/dr[i]*100:>7.1f}%", end="")
        else:
            print(f"  {'N/A':>8s}", end="")
    print()

print(f"\n  MARGEM BRUTA (%):")
print(f"    {'Riva':14s}", end="")
for i in qi:
    print(f"  {riva_lb[i]/riva_receita[i]*100:>7.1f}%", end="")
print()
if lb_key and rec_key:
    lb = dir_dre[lb_key]
    rec = dir_dre[rec_key]
    print(f"    {'Consolidada':14s}", end="")
    for i in qi:
        if i < len(lb) and lb[i] and rec[i]:
            print(f"  {lb[i]/rec[i]*100:>7.1f}%", end="")
        else:
            print(f"  {'N/A':>8s}", end="")
    print()
    print(f"    {'Dir ex-Riva':14s}", end="")
    for i in qi:
        if i < len(lb) and lb[i] and rec[i]:
            d_lb = lb[i] - riva_lb[i]
            d_rec = rec[i] - riva_receita[i]
            if d_rec > 0:
                print(f"  {d_lb/d_rec*100:>7.1f}%", end="")
            else:
                print(f"  {'N/A':>8s}", end="")
        else:
            print(f"  {'N/A':>8s}", end="")
    print()

print(f"\n  MARGEM LIQUIDA (%):")
print(f"    {'Riva':14s}", end="")
for i in qi:
    print(f"  {riva_ll[i]/riva_receita[i]*100:>7.1f}%", end="")
print()
if ll_key and rec_key:
    ll = dir_dre[ll_key]
    rec = dir_dre[rec_key]
    print(f"    {'Consolidada':14s}", end="")
    for i in qi:
        if i < len(ll) and ll[i] and rec[i]:
            print(f"  {ll[i]/rec[i]*100:>7.1f}%", end="")
        else:
            print(f"  {'N/A':>8s}", end="")
    print()

print(f"\n  LUCRO LIQUIDO (R$ mm):")
print(f"    {'Riva':14s}", end="")
for i in qi:
    print(f"  {riva_ll[i]/1000:>8.0f}", end="")
print()
if ll_key:
    ll = dir_dre[ll_key]
    print(f"    {'Consolidada':14s}", end="")
    for i in qi:
        if i < len(ll) and ll[i]:
            print(f"  {ll[i]/1000:>8.0f}", end="")
        else:
            print(f"  {'N/A':>8s}", end="")
    print()
    print(f"    {'Riva % Consol':14s}", end="")
    for i in qi:
        if i < len(ll) and ll[i]:
            print(f"  {riva_ll[i]/ll[i]*100:>7.1f}%", end="")
        else:
            print(f"  {'N/A':>8s}", end="")
    print()

print(f"\n  ROE ANUALIZADO (%):")
print(f"    {'Riva':14s}", end="")
for i in qi:
    roe = riva_ll[i] * 4 / riva_pl[i] * 100
    print(f"  {roe:>7.1f}%", end="")
print()

print(f"\n  {header_str}")
