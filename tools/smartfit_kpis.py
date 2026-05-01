"""
SmartFit Brasil Próprias — KPIs operacionais.

KPIs principais (Smart Fit Brasil próprias — exclui Bio Ritmo, Studios, franquias):
  1. Receita / Loja Média Brasil    (R$ mm/loja, anualizado)
  2. Ticket médio mensal Brasil     (R$/mês, base disclosed que exclui TotalPass)
  3. Alunos médios por Loja Média Brasil   (mil/loja)

KPIs ajustados por TotalPass:
  4. Alunos médios INCLUINDO TotalPass    (alunos_disclosed / (1 - tp_freq_pct))
  5. Ticket médio mensal EX-TotalPass    (receita × (1 - tp_rev_pct) / 3 / alunos_disclosed)

Uso:

    # Mostrar a série histórica completa
    python tools/smartfit_kpis.py --show

    # Quando o release do novo trimestre for ingerido em sources/structured/smart/<P>/:
    python tools/smartfit_kpis.py --periodo 1T26 --auto

    # OU passar manualmente:
    python tools/smartfit_kpis.py --periodo 1T26 \
      --receita_brasil 660.0 \
      --academias_brasil_eop 720 \
      --alunos_brasil_eop 1700

REGRA: NUNCA estimar # academias. Se a empresa não publicar EoP, ir buscar — não preencher por proxy.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass

# TotalPass MAU Brasil mensal (Sensor Tower, fonte: Modelo SmartFit 4T25, sheet "Dados SensorTower MS").
# IMPORTANTE: NÃO usamos SF MAU porque Smart Fit balcão não exige abrir o app pra entrar na academia
# (Sensor Tower não captura balcão). TP MAU é o único sinal real de atividade, usado pra fatiar a freq% anual
# disclosed entre os 4 trimestres do ano.
TP_MAU_BR = {
    # ano-mes: TP MAU
    "2022-01":  56_016, "2022-02":  60_420, "2022-03":  64_964,
    "2022-04":  62_770, "2022-05":  71_017, "2022-06":  71_105,
    "2022-07":  84_632, "2022-08": 104_021, "2022-09": 115_686,
    "2022-10": 119_422, "2022-11": 124_851, "2022-12": 120_108,
    "2023-01": 162_563, "2023-02": 158_209, "2023-03": 170_654,
    "2023-04": 169_716, "2023-05": 188_580, "2023-06": 195_697,
    "2023-07": 214_422, "2023-08": 243_411, "2023-09": 620_953,
    "2023-10": 655_143, "2023-11": 635_367, "2023-12": 649_056,
    "2024-01": 914_783, "2024-02": 919_313, "2024-03": 943_212,
    "2024-04": 1_011_408, "2024-05": 1_112_143, "2024-06": 1_270_681,
    "2024-07": 1_317_651, "2024-08": 1_332_291, "2024-09": 1_350_567,
    "2024-10": 1_570_178, "2024-11": 1_453_835, "2024-12": 1_450_829,
    "2025-01": 1_865_022, "2025-02": 1_831_584, "2025-03": 1_944_460,
    "2025-04": 1_925_001, "2025-05": 1_928_034, "2025-06": 2_089_796,
    "2025-07": 2_138_221, "2025-08": 2_189_000, "2025-09": 2_677_354,
    "2025-10": 2_957_492, "2025-11": 2_876_594, "2025-12": 2_889_637,
    "2026-01": 3_732_000, "2026-02": 3_712_000, "2026-03": 4_110_000,
}

# Disclosed anual TP freq/rev % (do release 4T do ano respectivo) — usados como ANCHORS.
TP_ANNUAL_DISCLOSED = {
    2024: (11.0, 8.0),   # freq, rev (revisado pós-controle antifraude no release 4T25)
    2025: (15.0, 12.0),  # do release 4T25
    # 2026: (?, ?)        # TBD until 4T26 release; pode passar via --tp_freq_2026 e --tp_rev_2026
}


def quarter_of(ym: str) -> str:
    y, m = ym.split("-")
    q = (int(m) - 1) // 3 + 1
    return f"{q}T{y[2:]}"


def derive_tp_quarterly(year_anchors: dict | None = None) -> dict:
    """
    Para cada trimestre, deriva tp_freq_pct e tp_rev_pct via:
      tp_freq_q = anual_disclosed × (TP_MAU_q / quarterly_avg_TP_MAU_year)

    Onde quarterly_avg = sum(TP_MAU_year) / 4. Resultado: a média dos 4 tris bate exatamente no
    anual disclosed, e a sazonalidade do TP MAU distribui o peso entre os 4 trimestres.

    year_anchors override default TP_ANNUAL_DISCLOSED (útil pra estimar 2026 antes do release).
    Para anos sem anchor (2022, 2023, 2026+ se não passado), retorna (None, None) → deixa n/d.
    """
    anchors = {**TP_ANNUAL_DISCLOSED, **(year_anchors or {})}
    # Agrega TP MAU mensal em trimestral
    by_q = {}
    by_year = {}
    for ym, tp in TP_MAU_BR.items():
        q = quarter_of(ym)
        year = int("20" + q[2:])
        by_q[q] = by_q.get(q, 0) + tp
        by_year.setdefault(year, []).append(tp)
    # Para cada trimestre, calcula peso vs avg do ano (3-month avg)
    out = {}
    for q, tp_q in by_q.items():
        year = int("20" + q[2:])
        if year not in anchors:
            out[q] = (None, None)
            continue
        annual_total = sum(by_year[year])
        if len(by_year[year]) < 12:
            # ano parcial → não calibra (avg incompleto)
            out[q] = (None, None)
            continue
        avg_q = annual_total / 4
        weight = tp_q / avg_q
        freq_disc, rev_disc = anchors[year]
        out[q] = (freq_disc * weight, rev_disc * weight)
    return out


_TP_DERIVED = derive_tp_quarterly()


def tp_for(periodo: str):
    """Retorna (tp_freq_pct, tp_rev_pct) trimestral fatiado do anual disclosed via TP MAU sazonal."""
    return _TP_DERIVED.get(periodo, (None, None))


# Histórico Smart Fit Brasil próprias — fonte 4T25 release (mais recente, corrige restatements).
# tp_freq_pct/tp_rev_pct: derivados de MAU trimestral × calibração anual disclosed.
def _build_hist():
    raw = [
        # periodo,  receita,  acad_eop,  alunos_eop
        ("4T22",  None,     429,       1_165),
        ("1T23",  383.5,    431,       1_307),
        ("2T23",  405.7,    431,       1_277),
        ("3T23",  413.0,    448,       1_316),
        ("4T23",  425.1,    486,       1_353),
        ("1T24",  464.8,    493,       1_525),
        ("2T24",  482.0,    506,       1_515),
        ("3T24",  503.7,    525,       1_559),
        ("4T24",  524.0,    569,       1_560),
        ("1T25",  577.5,    573,       1_715),
        ("2T25",  595.7,    587,       1_635),
        ("3T25",  605.3,    605,       1_620),
        ("4T25",  611.7,    693,       1_595),
    ]
    return [(p, r, a, al, *tp_for(p)) for p, r, a, al in raw]


HIST = _build_hist()


@dataclass
class QuarterKPIs:
    periodo: str
    receita: float | None
    acad_eop: int | None
    alunos_eop: int | None
    tp_freq_pct: float | None
    tp_rev_pct: float | None
    acad_med: float | None
    alunos_med: float | None
    rec_por_loja: float | None
    ticket_mensal: float | None
    alunos_por_loja: float | None
    alunos_med_inc_tp: float | None
    ticket_ex_tp: float | None


def yoy(curr, prior):
    if curr is None or prior is None or prior == 0:
        return "n/a"
    return f"{(curr / prior - 1) * 100:+.1f}%"


def compute_kpis(rows):
    out = []
    for i, (per, rec, ac_eop, al_eop, tp_freq, tp_rev) in enumerate(rows):
        prev_ac = rows[i - 1][2] if i > 0 else None
        prev_al = rows[i - 1][3] if i > 0 else None
        ac_med = (ac_eop + prev_ac) / 2 if (ac_eop is not None and prev_ac is not None) else None
        al_med = (al_eop + prev_al) / 2 if (al_eop is not None and prev_al is not None) else None
        rec_por_loja = (rec * 4 / ac_med) if (rec is not None and ac_med) else None
        ticket = (rec * 1000 / 3 / al_med) if (rec is not None and al_med) else None
        al_por_loja = (al_med / ac_med) if (al_med and ac_med) else None
        # Adjusted by TotalPass — assume TP users have similar usage frequency to balcão
        al_med_inc_tp = (al_med / (1 - tp_freq / 100)) if (al_med and tp_freq is not None) else None
        # Ticket ex-TP: receita do balcão / alunos balcão (que é o disclosed)
        ticket_ex_tp = (rec * (1 - tp_rev / 100) * 1000 / 3 / al_med) if (rec is not None and al_med and tp_rev is not None) else None
        out.append(QuarterKPIs(
            periodo=per, receita=rec, acad_eop=ac_eop, alunos_eop=al_eop,
            tp_freq_pct=tp_freq, tp_rev_pct=tp_rev, acad_med=ac_med, alunos_med=al_med,
            rec_por_loja=rec_por_loja, ticket_mensal=ticket, alunos_por_loja=al_por_loja,
            alunos_med_inc_tp=al_med_inc_tp, ticket_ex_tp=ticket_ex_tp,
        ))
    return out


def fmt(v, fmt_str="{:.1f}"):
    return fmt_str.format(v) if v is not None else "n/d"


def show(kpis):
    print()
    headers = ["Per", "Rec BR", "#acad", "alunos", "Rec/loja(an)", "YoY", "Ticket/mês", "YoY",
               "Alunos/loja", "YoY", "Alunos/loja(c/TP)", "YoY", "Ticket ex-TP", "YoY"]
    print(f"{headers[0]:<6}{headers[1]:>9}{headers[2]:>7}{headers[3]:>8}"
          f"{headers[4]:>14}{headers[5]:>8}{headers[6]:>12}{headers[7]:>8}"
          f"{headers[8]:>13}{headers[9]:>8}{headers[10]:>20}{headers[11]:>8}"
          f"{headers[12]:>14}{headers[13]:>8}")
    print("-" * 153)
    for i, k in enumerate(kpis):
        prior = kpis[i - 4] if i >= 4 else None
        rl_y = yoy(k.rec_por_loja, prior.rec_por_loja) if prior else "—"
        tk_y = yoy(k.ticket_mensal, prior.ticket_mensal) if prior else "—"
        al_y = yoy(k.alunos_por_loja, prior.alunos_por_loja) if prior else "—"
        al_tp_y = yoy(k.alunos_med_inc_tp, prior.alunos_med_inc_tp) if prior else "—"
        tk_ex_y = yoy(k.ticket_ex_tp, prior.ticket_ex_tp) if prior else "—"
        # alunos/loja c/TP = alunos_med_inc_tp / acad_med (mil)
        al_loja_tp = (k.alunos_med_inc_tp / k.acad_med) if (k.alunos_med_inc_tp and k.acad_med) else None
        prior_al_loja_tp = (prior.alunos_med_inc_tp / prior.acad_med) if (prior and prior.alunos_med_inc_tp and prior.acad_med) else None
        al_loja_tp_y = yoy(al_loja_tp, prior_al_loja_tp) if prior else "—"
        print(f"{k.periodo:<6}{fmt(k.receita):>9}{fmt(k.acad_eop, '{:.0f}'):>7}{fmt(k.alunos_eop, '{:.0f}'):>8}"
              f"{fmt(k.rec_por_loja, '{:.2f}'):>14}{rl_y:>8}{fmt(k.ticket_mensal, '{:.1f}'):>12}{tk_y:>8}"
              f"{fmt(k.alunos_por_loja, '{:.2f}'):>13}{al_y:>8}"
              f"{fmt(al_loja_tp, '{:.2f}'):>20}{al_loja_tp_y:>8}"
              f"{fmt(k.ticket_ex_tp, '{:.1f}'):>14}{tk_ex_y:>8}")
    print()
    print("Notas:")
    print("- Medias = (EoP_q + EoP_{q-1}) / 2 (proxy - empresa nao publica media absoluta)")
    print("- 'Alunos/loja(c/TP)' = (alunos_med / (1 - tp_freq_pct)) / acad_med - assume freq de uso TP user = freq balcao")
    print("- 'Ticket ex-TP' = receita * (1 - tp_rev_pct) * 1000 / 3 / alunos_med (R$/mes do balcao puro)")
    print("- tp_freq_pct e tp_rev_pct: anual disclosed FATIADO entre os 4 trimestres pelo peso de TP MAU (Sensor Tower).")
    print("  Formula: tp_freq_q = freq_anual * (TP_MAU_q / TP_MAU_q_avg_anual). Media dos 4 tris bate o anual disclosed.")
    print("  Sazonalidade clara: 1T < anual, 4T > anual (TP MAU cresce ao longo do ano).")
    print("- SF MAU NAO usado: balcao Smart Fit nao precisa abrir o app pra entrar, Sensor Tower nao captura.")
    print("- Anos sem disclosure (2022-2023, 2026+): KPIs TP-ajustados ficam n/d. Pra estimar 1T26, ver --tp_freq_2026.")


def auto_load(periodo: str):
    """Tenta extrair receita_brasil, academias_brasil_eop, alunos_brasil_eop do structured/."""
    base = f"sources/structured/smart/{periodo}"
    if not os.path.isdir(base):
        return None
    rec, acad, alunos = None, None, None
    for fname in ("release.json", "itr.json"):
        fpath = os.path.join(base, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            s = f.read()
        # Receita Brasil próprias (R$ mm) — busca chaves com receita+brasil+smart
        for m in re.finditer(r'"([^"]*)":\s*([0-9]+(?:\.[0-9]+)?)', s):
            key, val_s = m.group(1).lower(), float(m.group(2))
            # Receita Smart Fit Brasil rmm
            if rec is None and "receita" in key and "brasil" in key and ("smart" in key or "propria" in key) and 100 < val_s < 1500:
                rec = val_s
            # # Academias Smart Fit Brasil próprias EoP
            if acad is None and ("smart_fit_proprias_brasil" in key or ("academia" in key and "brasil" in key and "propri" in key) or ("club" in key and "brasil" in key and "propri" in key)) and 300 < val_s < 1200:
                acad = int(val_s)
            # Alunos Smart Fit Brasil próprias mil
            if alunos is None and ("smart_fit_proprias_brasil" in key or ("clientes" in key and "brasil" in key and "propri" in key) or ("base" in key and "brasil" in key and "propri" in key)) and 1000 < val_s < 5000:
                alunos = int(val_s)
    return (rec, acad, alunos) if any((rec, acad, alunos)) else None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--show", action="store_true")
    p.add_argument("--periodo", help="período do novo trimestre (ex: 1T26)")
    p.add_argument("--auto", action="store_true", help="auto-load do sources/structured/smart/<P>/")
    p.add_argument("--receita_brasil", type=float)
    p.add_argument("--academias_brasil_eop", type=int)
    p.add_argument("--alunos_brasil_eop", type=int)
    p.add_argument("--tp_freq_pct", type=float, help="% check-ins TotalPass do ano (default: usa último ano disclosed)")
    p.add_argument("--tp_rev_pct", type=float, help="% receita TotalPass do ano (default: idem)")
    args = p.parse_args()

    rows = list(HIST)
    if args.periodo:
        rec, acad, alunos = args.receita_brasil, args.academias_brasil_eop, args.alunos_brasil_eop
        if args.auto:
            loaded = auto_load(args.periodo)
            if loaded:
                ar, aa, aal = loaded
                rec = rec or ar
                acad = acad or aa
                alunos = alunos or aal
                print(f"[auto-load {args.periodo}] receita={ar} acad={aa} alunos={aal}")
            else:
                print(f"[auto-load {args.periodo}] structured/ não encontrado", file=sys.stderr)
        if not all([rec, acad, alunos]):
            print(f"ERRO: período {args.periodo} requer receita_brasil, academias_brasil_eop, alunos_brasil_eop", file=sys.stderr)
            print(f"  carregado: receita={rec} acad={acad} alunos={alunos}", file=sys.stderr)
            sys.exit(1)
        # TP defaults: usa último ano disclosed (4T25 → 15/12)
        tp_freq = args.tp_freq_pct if args.tp_freq_pct is not None else HIST[-1][4]
        tp_rev = args.tp_rev_pct if args.tp_rev_pct is not None else HIST[-1][5]
        rows.append((args.periodo, rec, acad, alunos, tp_freq, tp_rev))

    kpis = compute_kpis(rows)
    if args.show or args.periodo:
        show(kpis)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
