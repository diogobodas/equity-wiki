"""Slide 13 — Direcional vs Riva lançamentos 2022-2025.

Fontes:
- 2022, 2023: full/direcional/4T23/release.md (tabela "VGV Lançado - 100%")
- 2024: structured/direcional/2024/dfp.json :: company_specific.segmentos
- 2025: structured/direcional/2025/dfp.json :: company_specific.segmentos

Inclui "Pode Entrar" dentro do core Direcional (segmento MCMV estadual SP, ~271mm em 2024).
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": "#333",
    "axes.linewidth": 0.8,
    "text.usetex": False,
    "mathtext.default": "regular",
})
# Escape $ so matplotlib doesn't interpret as mathtext
import matplotlib
matplotlib.rcParams["text.parse_math"] = False

anos = ["2022", "2023", "2024", "2025"]
# VGV lançado 100% em R$ mm
core = [2235.6, 3080.1, 3600.0, 3776.0]   # Direcional + Pode Entrar (2024 = 3328,9 + 271,1)
riva = [1400.6, 1777.4, 2154.8, 3081.6]
total = [c + r for c, r in zip(core, riva)]
pct_riva = [r / t * 100 for r, t in zip(riva, total)]

fig, ax = plt.subplots(figsize=(10, 5.8), dpi=180)

BLUE = "#1f4e79"   # Direcional core
ORANGE = "#ed7d31" # Riva
LINE = "#c00000"   # % Riva

x = list(range(len(anos)))
b1 = ax.bar(x, core, color=BLUE, label="Direcional core (MCMV F1/F2 + Pode Entrar)", width=0.6)
b2 = ax.bar(x, riva, bottom=core, color=ORANGE, label="Riva (média renda / F3-F4 / SBPE)", width=0.6)

# Valores dentro das barras
for i, (c, r, t) in enumerate(zip(core, riva, total)):
    ax.text(i, c / 2, f"R$ {c/1000:.1f} bi", ha="center", va="center",
            color="white", fontsize=10, fontweight="bold")
    ax.text(i, c + r / 2, f"R$ {r/1000:.1f} bi", ha="center", va="center",
            color="white", fontsize=10, fontweight="bold")
    # Total acima da linha de % Riva para não brigar com marker
    ax.text(i, max(t, 7000) * 0.07 + t + 600, f"Total: R$ {t/1000:.1f} bi",
            ha="center", va="bottom", color="#333",
            fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#ddd", alpha=0.9))

ax.set_xticks(x)
ax.set_xticklabels(anos, fontsize=12)
ax.set_ylabel("VGV Lançado (R$ milhões, 100%)", fontsize=11)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v/1000:.0f}"))
ax.set_ylim(0, max(total) * 1.32)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Eixo secundário — % Riva
ax2 = ax.twinx()
ax2.plot(x, pct_riva, color=LINE, marker="o", markersize=9, linewidth=2.2,
         label="% Riva no total", zorder=5)
for i, p in enumerate(pct_riva):
    # Labels abaixo do marker para não brigar com os totais das barras
    ax2.annotate(f"{p:.0f}%", (i, p), textcoords="offset points",
                 xytext=(18, -4), ha="left", va="center", color=LINE,
                 fontsize=11, fontweight="bold")
ax2.set_ylim(0, 60)
ax2.set_ylabel("% Riva", color=LINE, fontsize=11)
ax2.tick_params(axis="y", colors=LINE)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_color(LINE)

# Título e legenda
ax.set_title("Direcional — Lançamentos passam de R$ 3,6 bi (2022) para R$ 6,9 bi (2025)\n"
             "Riva responde por ~45% do grupo, vs 39% em 2022",
             fontsize=13, fontweight="bold", loc="left", pad=14)

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False, fontsize=10)

fig.text(0.01, 0.01,
         "Fonte: Direcional — DFP 2024/2025 e release 4T23 (VGV 100%).",
         fontsize=8, color="#666", style="italic")

plt.tight_layout()
out = "slide13_direcional_riva_lancamentos.png"
plt.savefig(out, dpi=220, bbox_inches="tight", facecolor="white")
print(f"saved: {out}")
