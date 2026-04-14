#!/usr/bin/env python
"""Test hypothesis: is backlog margin a good predictor of future gross margin for low-income homebuilders?"""

import re
import numpy as np

FILE = "sources/full/generic/HB_historical series_4Q25.md"
TARGETS = ["Tenda", "Cury", "Direcional", "MRV", "Plano & Plano"]

# Known company names to distinguish from metric headers
COMPANIES = {
    "EZTec", "Even", "Helbor", "Lavvi", "Melnick", "Mitre", "Trisul",
    "Tecnisa", "PDG", "Cyrela", "Moura Dubeux", "Rossi", "Gafisa",
    "Tenda", "Cury", "Direcional", "MRV", "Plano & Plano", "Total",
}


def period_sort_key(p):
    q = int(p[0])
    y = int(p[2:])
    return (y, q)


def parse_metric(lines, metric_label, target_companies):
    """Parse a single metric block. Stops at next metric header or section break."""
    data = {}
    col_to_period = {}
    found_header = False

    for i, line in enumerate(lines):
        # Find the metric header line
        if not found_header:
            if metric_label in line and line.startswith('|'):
                found_header = True
                cols = [c.strip() for c in line.split('|')]
                for j, c in enumerate(cols):
                    c = c.strip()
                    if re.match(r'^[1-4]Q\d{2}$', c):
                        col_to_period[j] = c
            continue

        # We're past the header — reading company rows
        if not line.startswith('|'):
            continue

        # Section break
        if line.startswith('## '):
            break

        cols = [c.strip() for c in line.split('|')]
        if len(cols) < 3:
            continue

        company = cols[1].strip()

        # If we hit another metric header (all-caps label, not a company name)
        if company not in COMPANIES and company != 'NaN' and company != '---':
            # It's a new metric header — stop
            break

        if company not in target_companies:
            continue

        values = {}
        for j, period in col_to_period.items():
            if j < len(cols):
                val = cols[j].strip()
                try:
                    v = float(val)
                    if not np.isnan(v):
                        values[period] = v
                except (ValueError, TypeError):
                    pass

        if values:
            data[company] = values

    return data


with open(FILE, encoding='utf-8') as f:
    lines = f.readlines()

backlog_data = parse_metric(lines, "BACKLOG MARGIN (%)", TARGETS)
gross_data = parse_metric(lines, "GROSS MARGIN ex-interest (%)", TARGETS)

print("=" * 70)
print("HIPOTESE: Backlog Margin prediz Gross Margin futura?")
print("Low-income: Tenda, Cury, Direcional, MRV, Plano & Plano")
print("=" * 70)

# Data availability
print("\nDados disponiveis (trimestres):")
for company in TARGETS:
    bm_n = len(backlog_data.get(company, {}))
    gm_n = len(gross_data.get(company, {}))
    bm_range = gm_range = ""
    if bm_n > 0:
        ps = sorted(backlog_data[company].keys(), key=period_sort_key)
        bm_range = f" ({ps[0]}..{ps[-1]})"
    if gm_n > 0:
        ps = sorted(gross_data[company].keys(), key=period_sort_key)
        gm_range = f" ({ps[0]}..{ps[-1]})"
    print(f"  {company:15s}: backlog={bm_n:2d}{bm_range}, gross_margin={gm_n:2d}{gm_range}")

# Correlation at different lags
print("\n" + "=" * 70)
print("CORRELACOES POR LAG")
print("=" * 70)

best_lag = None
best_r2_pooled = -1

for lag in [1, 2, 3, 4]:
    print(f"\n--- Lag = {lag} tri: backlog(t) -> gross_margin(t+{lag}) ---")

    all_x, all_y = [], []

    for company in TARGETS:
        if company not in backlog_data or company not in gross_data:
            print(f"  {company:15s}: sem dados")
            continue

        bm = backlog_data[company]
        gm = gross_data[company]
        all_periods = sorted(set(list(bm.keys()) + list(gm.keys())), key=period_sort_key)

        x_vals, y_vals = [], []
        for i, p in enumerate(all_periods):
            if p not in bm:
                continue
            if i + lag < len(all_periods):
                future_p = all_periods[i + lag]
                if future_p in gm:
                    x_vals.append(bm[p])
                    y_vals.append(gm[future_p])

        if len(x_vals) >= 5:
            corr = np.corrcoef(x_vals, y_vals)[0, 1]
            print(f"  {company:15s}: r = {corr:+.3f}  R2 = {corr**2:.3f}  (n={len(x_vals)})")
            all_x.extend(x_vals)
            all_y.extend(y_vals)
        else:
            print(f"  {company:15s}: insuficiente (n={len(x_vals)})")

    if len(all_x) >= 10:
        pool_corr = np.corrcoef(all_x, all_y)[0, 1]
        pool_r2 = pool_corr ** 2
        print(f"  {'POOLED':15s}: r = {pool_corr:+.3f}  R2 = {pool_r2:.3f}  (n={len(all_x)})")
        if pool_r2 > best_r2_pooled:
            best_r2_pooled = pool_r2
            best_lag = lag

if best_lag:
    print(f"\n  >> Melhor lag pooled: {best_lag} tri (R2 = {best_r2_pooled:.3f})")

# Detailed view for lag=2
print("\n" + "=" * 70)
print("TABELA DETALHADA — Lag = 2 tri (ultimos 8 por empresa)")
print("=" * 70)

for company in TARGETS:
    if company not in backlog_data or company not in gross_data:
        continue
    bm = backlog_data[company]
    gm = gross_data[company]
    all_periods = sorted(set(list(bm.keys()) + list(gm.keys())), key=period_sort_key)

    pairs = []
    for i, p in enumerate(all_periods):
        if p not in bm:
            continue
        if i + 2 < len(all_periods):
            fp = all_periods[i + 2]
            if fp in gm:
                pairs.append((p, bm[p], gm[fp], gm[fp] - bm[p], fp))

    if not pairs:
        continue

    x = np.array([b for _, b, _, _, _ in pairs])
    y = np.array([g for _, _, g, _, _ in pairs])
    r = np.corrcoef(x, y)[0, 1] if len(x) >= 3 else float('nan')

    print(f"\n{company} (r={r:+.3f}, R2={r**2:.3f}, n={len(pairs)}):")
    print(f"  {'Periodo':>8s}  {'Backlog%':>10s}  {'GM(t+2)':>10s}  {'Delta':>8s}")
    for p, b, g, d, fp in pairs[-8:]:
        print(f"  {p:>8s}  {b*100:>9.1f}%  {g*100:>9.1f}%  {d*100:>+7.1f}pp  (->{fp})")

# Pooled regression lag=2
print("\n" + "=" * 70)
print("REGRESSAO POOLED — backlog(t) -> gross_margin(t+2)")
print("=" * 70)

all_x, all_y = [], []
for company in TARGETS:
    if company not in backlog_data or company not in gross_data:
        continue
    bm = backlog_data[company]
    gm = gross_data[company]
    all_periods = sorted(set(list(bm.keys()) + list(gm.keys())), key=period_sort_key)
    for i, p in enumerate(all_periods):
        if p not in bm:
            continue
        if i + 2 < len(all_periods):
            fp = all_periods[i + 2]
            if fp in gm:
                all_x.append(bm[p])
                all_y.append(gm[fp])

if len(all_x) >= 5:
    all_x = np.array(all_x)
    all_y = np.array(all_y)
    slope, intercept = np.polyfit(all_x, all_y, 1)
    r = np.corrcoef(all_x, all_y)[0, 1]
    r2 = r ** 2
    mae = np.mean(np.abs(all_y - (slope * all_x + intercept)))

    print(f"  y = {slope:.3f}x + {intercept:.4f}")
    print(f"  R2 = {r2:.3f}")
    print(f"  r  = {r:+.3f}")
    print(f"  MAE = {mae*100:.1f}pp")
    print(f"  n  = {len(all_x)} observacoes")

    if r2 > 0.7:
        verdict = "FORTE PREDITOR"
    elif r2 > 0.4:
        verdict = "PREDITOR MODERADO"
    elif r2 > 0.2:
        verdict = "PREDITOR FRACO"
    else:
        verdict = "NAO EH BOM PREDITOR"

    print(f"\n  >> VEREDICTO: {verdict}")
    print(f"     Backlog margin explica {r2*100:.0f}% da variancia da gross margin")
    print(f"     2 trimestres a frente (MAE = {mae*100:.1f}pp)")
else:
    print("  Dados insuficientes para regressao pooled")

# Contemporaneous correlation (lag=0)
print("\n" + "=" * 70)
print("REFERENCIA: correlacao contemporanea (lag=0)")
print("=" * 70)
all_x0, all_y0 = [], []
for company in TARGETS:
    if company not in backlog_data or company not in gross_data:
        continue
    bm = backlog_data[company]
    gm = gross_data[company]
    common = sorted(set(bm.keys()) & set(gm.keys()))
    if len(common) >= 5:
        cx = [bm[p] for p in common]
        cy = [gm[p] for p in common]
        cr = np.corrcoef(cx, cy)[0, 1]
        print(f"  {company:15s}: r = {cr:+.3f}  R2 = {cr**2:.3f}  (n={len(common)})")
        all_x0.extend(cx)
        all_y0.extend(cy)

if len(all_x0) >= 10:
    pr = np.corrcoef(all_x0, all_y0)[0, 1]
    print(f"  {'POOLED':15s}: r = {pr:+.3f}  R2 = {pr**2:.3f}  (n={len(all_x0)})")
