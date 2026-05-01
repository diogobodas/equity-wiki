"""
SmartFit Brasil Próprias — KPIs operacionais.

Os 3 KPIs principais:
  1. Receita / Loja Média Brasil  (R$ mm/loja, anualizado)
  2. Ticket médio mensal Brasil   (R$/mês)
  3. Alunos médios por Loja Média Brasil  (mil/loja)

Todas as bases são "Smart Fit Brasil Próprias" — exclui Bio Ritmo, Studios,
franquias e regional Mexico/Outros. Médias trimestrais são proxy = (EoP_q + EoP_{q-1}) / 2
salvo quando a empresa publica a média explícita (caso, comparar).

Uso:

    # Mostrar a série histórica com os 3 KPIs (todos os tris já publicados)
    python tools/smartfit_kpis.py --show

    # Plug-and-play quando o 1T26 sair: passe os inputs do release
    python tools/smartfit_kpis.py --periodo 1T26 \
      --receita_brasil 660.0 \
      --academias_brasil_eop 720 \
      --alunos_brasil_eop 1700

A regra de ouro: NUNCA estimar # academias. Se a empresa não divulgar o EoP,
deixar n/d e ir buscar — não preencher por proxy.
"""

import argparse
import sys
from dataclasses import dataclass

# Histórico Smart Fit Brasil próprias — fonte 4T25 release (mais recente, corrige
# eventuais restatements). Para cada período, EoP = end-of-period.
# Receita em R$ mm. Academias em # unidades. Alunos em milhares.
HIST = [
    #         receita,  academias_eop,  alunos_eop
    ("4T22",  None,     429,            1_165),
    ("1T23",  383.5,    431,            1_307),
    ("2T23",  405.7,    431,            1_277),
    ("3T23",  413.0,    448,            1_316),
    ("4T23",  425.1,    486,            1_353),
    ("1T24",  464.8,    493,            1_525),
    ("2T24",  482.0,    506,            1_515),
    ("3T24",  503.7,    525,            1_559),
    ("4T24",  524.0,    569,            1_560),
    ("1T25",  577.5,    573,            1_715),
    ("2T25",  595.7,    587,            1_635),
    ("3T25",  605.3,    605,            1_620),
    ("4T25",  611.7,    693,            1_595),
]


@dataclass
class QuarterKPIs:
    periodo: str
    receita_brasil: float | None
    acad_brasil_eop: int | None
    alunos_brasil_eop: int | None
    acad_media: float | None
    alunos_media: float | None
    receita_por_loja: float | None     # R$ mm / loja (anualizado: receita_q × 4 / acad_média)
    ticket_mensal: float | None         # R$ / mês
    alunos_por_loja: float | None       # mil alunos / loja


def yoy(curr: float | None, prior: float | None) -> str:
    if curr is None or prior is None or prior == 0:
        return "n/a"
    return f"{(curr / prior - 1) * 100:+.1f}%"


def compute_kpis(rows: list[tuple]) -> list[QuarterKPIs]:
    out = []
    for i, (per, rec, ac_eop, al_eop) in enumerate(rows):
        ac_med = (ac_eop + rows[i - 1][2]) / 2 if i > 0 and ac_eop is not None and rows[i - 1][2] is not None else None
        al_med = (al_eop + rows[i - 1][3]) / 2 if i > 0 and al_eop is not None and rows[i - 1][3] is not None else None
        rec_por_loja = (rec * 4 / ac_med) if (rec is not None and ac_med) else None
        ticket = (rec * 1000 / 3 / al_med) if (rec is not None and al_med) else None
        al_por_loja = (al_med / ac_med) if (al_med and ac_med) else None
        out.append(QuarterKPIs(
            periodo=per, receita_brasil=rec, acad_brasil_eop=ac_eop,
            alunos_brasil_eop=al_eop, acad_media=ac_med, alunos_media=al_med,
            receita_por_loja=rec_por_loja, ticket_mensal=ticket, alunos_por_loja=al_por_loja,
        ))
    return out


def fmt(v, fmt_str="{:.1f}"):
    return fmt_str.format(v) if v is not None else "n/d"


def show(kpis: list[QuarterKPIs]):
    print()
    print(f"{'Per':<6}{'Rec BR':>9}{'#acad EoP':>11}{'alunos EoP':>12}{'#acad méd':>11}{'alunos méd':>12}"
          f"{'R/loja anu':>12}{'YoY':>8}{'ticket/mês':>12}{'YoY':>8}{'alunos/loja':>13}{'YoY':>8}")
    print("-" * 122)
    for i, k in enumerate(kpis):
        prior = kpis[i - 4] if i >= 4 else None
        rl_yoy = yoy(k.receita_por_loja, prior.receita_por_loja) if prior else "—"
        tk_yoy = yoy(k.ticket_mensal, prior.ticket_mensal) if prior else "—"
        al_yoy = yoy(k.alunos_por_loja, prior.alunos_por_loja) if prior else "—"
        print(f"{k.periodo:<6}{fmt(k.receita_brasil):>9}{fmt(k.acad_brasil_eop, '{:.0f}'):>11}"
              f"{fmt(k.alunos_brasil_eop, '{:.0f}'):>12}{fmt(k.acad_media, '{:.1f}'):>11}"
              f"{fmt(k.alunos_media, '{:.0f}'):>12}{fmt(k.receita_por_loja, '{:.2f}'):>12}{rl_yoy:>8}"
              f"{fmt(k.ticket_mensal, '{:.1f}'):>12}{tk_yoy:>8}{fmt(k.alunos_por_loja, '{:.2f}'):>13}{al_yoy:>8}")
    print()
    print("Notas:")
    print("- 'R/loja anu' = receita_q × 4 / # acad média (anualizado, em R$ mm)")
    print("- 'ticket/mês' = receita_q × 1.000 / 3 / alunos média (em R$ por aluno por mês)")
    print("- 'alunos/loja' = alunos média (mil) / # acad média")
    print("- Médias = (EoP_q + EoP_{q-1}) / 2 — proxy. Empresa não publica média absoluta.")
    print("- YoY: comparação trimestre vs mesmo trimestre ano anterior.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--show", action="store_true", help="mostrar série histórica completa")
    p.add_argument("--periodo", help="período do novo trimestre (ex: 1T26)")
    p.add_argument("--receita_brasil", type=float, help="receita Smart Fit Brasil próprias do tri (R$ mm)")
    p.add_argument("--academias_brasil_eop", type=int, help="# academias Smart Fit próprias Brasil EoP")
    p.add_argument("--alunos_brasil_eop", type=int, help="# alunos Smart Fit próprias Brasil EoP (mil)")
    args = p.parse_args()

    rows = list(HIST)
    if args.periodo:
        if not all([args.receita_brasil, args.academias_brasil_eop, args.alunos_brasil_eop]):
            print("ERRO: --periodo requer --receita_brasil, --academias_brasil_eop e --alunos_brasil_eop", file=sys.stderr)
            sys.exit(1)
        rows.append((args.periodo, args.receita_brasil, args.academias_brasil_eop, args.alunos_brasil_eop))

    kpis = compute_kpis(rows)
    if args.show or args.periodo:
        show(kpis)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
