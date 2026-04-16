"""Quick chart: Direcional lucro líquido & margem líquida por trimestre (dados de sources/structured/direcional)."""
import json, os
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'sources', 'structured', 'direcional')
PERIODS = ['1T23','2T23','3T23','4T23','1T24','2T24','3T24','4T24','1T25','2T25','3T25','4T25']

lucros, margens = [], []
for p in PERIODS:
    with open(os.path.join(BASE, p, 'release.json'), encoding='utf-8') as f:
        dre = json.load(f)['canonical']['dre']
    lucros.append(dre['lucro_liquido'])
    margens.append(dre['margem_liquida'] * 100)

fig, ax1 = plt.subplots(figsize=(12, 6))
bars = ax1.bar(PERIODS, lucros, color='#1f4e79', alpha=0.85, label='Lucro líquido (R$ mi)')
ax1.set_ylabel('Lucro líquido (R$ mi)', color='#1f4e79', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#1f4e79')
ax1.set_ylim(0, max(lucros) * 1.2)

for bar, v in zip(bars, lucros):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
             f'{v:.0f}', ha='center', va='bottom', fontsize=9, color='#1f4e79')

ax2 = ax1.twinx()
ax2.plot(PERIODS, margens, color='#c0504d', marker='o', linewidth=2.2, label='Margem líquida (%)')
ax2.set_ylabel('Margem líquida (%)', color='#c0504d', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#c0504d')
ax2.set_ylim(0, max(margens) * 1.4)

for i, m in enumerate(margens):
    ax2.text(i, m + 0.6, f'{m:.1f}%', ha='center', va='bottom', fontsize=9, color='#c0504d')

plt.title('Direcional (DIRR3) — Lucro Líquido & Margem Líquida por Trimestre (1T23–4T25)',
          fontsize=13, pad=15)
ax1.set_xlabel('Trimestre', fontsize=11)
ax1.grid(axis='y', linestyle='--', alpha=0.3)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

plt.figtext(0.5, 0.01, 'Fonte: sources/structured/direcional/{periodo}/release.json',
            ha='center', fontsize=8, style='italic', color='gray')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), '..', '..', 'direcional_lucro_margem.png')
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f'Saved: {out}')
