"""Render portfolio figures from aggregate values printed in the source notebook.

The values below were transcribed from saved text outputs in cells 3–7 of
test_v2.ipynb (zero-based cell indices). This script needs neither the notebook
nor the private workbook and does not rerun the underlying business analysis.
See docs/figure_source_notes.md for precision and interpretation limits.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, FancyBboxPatch
from matplotlib.ticker import MultipleLocator, FuncFormatter


OUT = Path(__file__).resolve().parents[1] / "assets"
INK = "#142E49"
TEAL = "#168F93"
CORAL = "#E67C68"
GRAY = "#65788B"
PALE = "#E4EBF1"
BG = "#F7F9FC"

LABELS = {
    "Distribution Transf": "Distribution transformers",
    "EV Equip & Services": "EV equipment & services",
    "Electrical Component": "Electrical components",
    "IT": "IT",
    "MRO-Gen Indus/Safety": "MRO / industrial & safety",
    "Meters": "Meters",
    "Oth Gen Stn Equip": "Other generation equipment",
    "Protect/ControlEquip": "Protection & control",
    "Switchgear": "Switchgear",
    "Telecom Equip": "Telecommunications equipment",
    "Wire And Cable": "Wire & cable",
}

# Cell 4: category, printed CVS, source risk-tolerance label.
PRIORITIES = [
    ("Meters", 0.663832, "Med"),
    ("Distribution Transf", 0.617481, "Low"),
    ("Electrical Component", 0.565659, "Low"),
    ("Switchgear", 0.564693, "Low"),
    ("Protect/ControlEquip", 0.542492, "Low"),
    ("Wire And Cable", 0.431518, "Low"),
    ("Oth Gen Stn Equip", 0.381675, "Low"),
    ("Telecom Equip", 0.321338, "Med"),
    ("EV Equip & Services", 0.255150, "High"),
    ("IT", 0.215453, "Med"),
    ("MRO-Gen Indus/Safety", 0.134669, "High"),
]

# Cell 5: category, anonymous display suffix, lead time, days of supply.
# Only the two measures needed for the plot are retained; source row IDs omitted.
COVERAGE = [
    ("Switchgear", "A", 897, 684.0),
    ("Electrical Component", "", 210, 86.3),
    ("Switchgear", "B", 766, 663.0),
    ("Distribution Transf", "A", 299, 258.5),
    ("Distribution Transf", "B", 355, 350.0),
    ("Meters", "", 184, 180.0),
]

# Cell 3: category, item count, U.S.-origin item count, printed annual spend.
# Spend is already rounded by the original pandas scientific-notation display.
EXPOSURE = [
    ("Distribution Transf", 6, 3, 7.980565e7),
    ("EV Equip & Services", 3, 2, 1.507802e7),
    ("Electrical Component", 8, 3, 2.167737e7),
    ("IT", 46, 6, 3.737730e7),
    ("MRO-Gen Indus/Safety", 7, 1, 1.166851e7),
    ("Meters", 1, 1, 2.894197e7),
    ("Oth Gen Stn Equip", 2, 1, 8.268662e7),
    ("Protect/ControlEquip", 1, 1, 4.058744e7),
    ("Switchgear", 14, 2, 4.667357e7),
    ("Telecom Equip", 8, 3, 2.310972e7),
    ("Wire And Cable", 2, 1, 2.237980e7),
]

# Cell 7: HS code, printed U.S. share of Canadian imports in 2021 and 2024 (%).
IMPORTS = [
    ("850164", 33.6, 53.6), ("850213", 86.2, 88.9),
    ("850422", 63.0, 44.2), ("850423", 8.5, 12.0),
    ("850433", 22.9, 28.6), ("850434", 53.2, 35.9),
    ("850490", 41.0, 26.1), ("850760", 43.5, 55.8),
    ("853590", 49.1, 53.5), ("853720", 59.3, 40.7),
]

# Cell 11: aliases used in the original notebook, not new HS classifications.
HS_LABELS = {
    "850213": "Generators", "853720": "Switchgear Panels",
    "850422": "Transf<10MVA", "850760": "BESS/Li-ion",
    "853590": "SG Parts", "850164": "AC Generators",
    "850490": "Transf Parts", "850434": "Transf>500kVA",
    "850433": "Transf 16-500", "850423": "Transf>10MVA",
}

# Cell 6: source column order is Average, Developing, Excellent, Good, Poor.
PERFORMANCE = {
    "Distribution Transf": (3, 1, 4, 2, 2),
    "EV Equip & Services": (2, 0, 2, 3, 5),
    "Electrical Component": (9, 1, 10, 9, 5),
    "IT": (25, 9, 51, 47, 25),
    "MRO-Gen Indus/Safety": (14, 3, 11, 8, 5),
    "Meters": (0, 0, 0, 0, 2),
    "Oth Gen Stn Equip": (0, 0, 2, 0, 2),
    "Protect/ControlEquip": (1, 0, 0, 1, 0),
    "Switchgear": (6, 2, 10, 13, 4),
    "Telecom Equip": (5, 3, 5, 4, 6),
    "Wire And Cable": (2, 0, 3, 0, 3),
}


def page(number, title, subtitle, size=(14, 9.5)):
    fig = plt.figure(figsize=size, facecolor=BG)
    fig.text(.06, .964, f"UTILITY SUPPLY CHAIN  /  CASE STUDY  /  {number:02d}",
             color=TEAL, fontsize=10, weight="bold", va="top")
    fig.text(.06, .918, title, color=INK, fontsize=25, weight="bold", va="top")
    fig.text(.06, .865, subtitle, color=GRAY, fontsize=11, va="top")
    return fig


def axes(fig, rect):
    ax = fig.add_axes(rect, facecolor=BG)
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.tick_params(axis="both", length=0, colors=GRAY, labelsize=10, pad=10)
    ax.xaxis.grid(True, color=PALE, linewidth=.8)
    ax.set_axisbelow(True)
    return ax


def footer(fig, line1, line2):
    fig.add_artist(Line2D([.06, .94], [.102, .102], color=PALE, linewidth=1,
                         transform=fig.transFigure))
    fig.text(.06, .079, line1, fontsize=9.3, color=GRAY, va="top")
    fig.text(.06, .052, line2, fontsize=9.3, color=GRAY, va="top")


def save(fig, filename):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / filename, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(filename)


def priority_scores():
    fig = page(1, "Where to prioritize supply risk",
               "11 U.S.-exposed inventory categories | Historical case snapshot")
    colors = {"Low": CORAL, "Med": INK, "High": TEAL}
    fig.text(.06, .808, "SOURCE RISK TOLERANCE", color=GRAY, fontsize=9, weight="bold")
    fig.legend(handles=[Patch(color=colors[k], label=k) for k in ("Low", "Med", "High")],
               loc="center left", bbox_to_anchor=(.255, .812), frameon=False,
               ncol=3, fontsize=10, handlelength=1.2, columnspacing=2)
    ax = axes(fig, [.295, .197, .63, .565])
    ax.barh(range(11), [p[1] for p in PRIORITIES], height=.62,
            color=[colors[p[2]] for p in PRIORITIES])
    ax.set_yticks(range(11), [LABELS[p[0]] for p in PRIORITIES], color=INK)
    for i, (_, value, _) in enumerate(PRIORITIES):
        ax.text(value + .012, i, f"{value:.3f}", va="center", color=INK,
                fontsize=10, weight="bold")
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_locator(MultipleLocator(.2))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.1f}"))
    ax.set_xlabel("Composite vulnerability score (0–1 index)", labelpad=15, color=GRAY)
    footer(fig,
           "A weighted prioritization index, not a failure probability. Risk tolerance is an input, not a score band.",
           "Source: saved notebook output, cell 4. Index values shown to 3 decimals; weights and category aggregation affect rankings.")
    save(fig, "01_priority_scores.png")


def coverage_gaps():
    fig = page(2, "Inventory coverage falls short in six records",
               "U.S.-origin inventory | Days of supply compared with average replenishment lead time")
    fig.legend(handles=[Line2D([], [], marker="o", linestyle="none", color=TEAL,
                               markersize=8, label="Days of supply"),
                        Line2D([], [], marker="o", linestyle="none", color=INK,
                               markersize=8, label="Average lead time")],
               loc="center left", bbox_to_anchor=(.055, .81), frameon=False,
               ncol=2, fontsize=10, columnspacing=2)
    ax = axes(fig, [.295, .205, .63, .54])
    for i, (_, _, lead, supply) in enumerate(COVERAGE):
        ax.plot([supply, lead], [i, i], color=CORAL, linewidth=5,
                solid_capstyle="round", alpha=.75, zorder=2)
        ax.scatter([supply, lead], [i, i], color=[TEAL, INK], s=70, zorder=3,
                   edgecolor=BG, linewidth=1.4)
        # Small gaps receive one combined label so endpoint values cannot overlap.
        if lead - supply < 50:
            text = f"{supply:g} / {lead:g}"
            ax.text((supply + lead) / 2, i - .24, text, ha="center", color=INK, fontsize=10)
        else:
            ax.text(supply, i - .24, f"{supply:g}", ha="center", color=TEAL, fontsize=10)
            ax.text(lead, i - .24, f"{lead:g}", ha="center", color=INK, fontsize=10)
        ax.text(1090, i, f"{supply-lead:g} d", ha="right", va="center",
                color=CORAL, weight="bold", fontsize=12)
    ax.text(1090, -.74, "COVERAGE GAP", ha="right", color=GRAY, fontsize=9, weight="bold")
    labels = [LABELS[cat] + (f" · {suffix}" if suffix else "") for cat, suffix, _, _ in COVERAGE]
    ax.set_yticks(range(6), labels, color=INK)
    ax.set_ylim(5.6, -.7)
    ax.set_xlim(0, 1120)
    ax.set_xticks(range(0, 1001, 200))
    ax.set_xlabel("Days", labelpad=15, color=GRAY)
    footer(fig,
           "Coverage gap = days of supply − average lead time. A shortfall is a screening signal, not a forecast stockout date.",
           "Source: saved notebook output, cell 5. A/B distinguish anonymous records within a category; endpoint labels follow the legend order.")
    save(fig, "02_coverage_gaps.png")


def tariff_scenario():
    fig = page(3, "Tariff exposure under a 35% scenario",
               "Historical case assumption | An item-count allocation proxy, not a current tariff forecast",
               size=(14, 10))
    impacts = sorted([(cat, spend * us / count * .35 / 1e6)
                      for cat, count, us, spend in EXPOSURE], key=lambda row: -row[1])
    total = sum(value for _, value in impacts)
    fig.text(.06, .803, f"CAD {total:.1f}M", fontsize=32, color=INK, weight="bold", va="top")
    fig.text(.355, .799, "Illustrative annual cost increase", fontsize=13, color=INK, weight="bold", va="top")
    fig.text(.355, .767, "35% × category annual spend × U.S.-origin item share", fontsize=10.5, color=GRAY, va="top")
    ax = axes(fig, [.295, .185, .63, .51])
    ax.barh(range(11), [value for _, value in impacts], height=.63,
            color=[TEAL if i < 3 else INK for i in range(11)])
    ax.set_yticks(range(11), [LABELS[cat] for cat, _ in impacts], color=INK)
    for i, (_, value) in enumerate(impacts):
        ax.text(value + .2, i, f"${value:.1f}M", va="center", color=INK, fontsize=10, weight="bold")
    ax.invert_yaxis()
    ax.set_xlim(0, 17)
    ax.set_xticks(range(0, 16, 3))
    ax.set_xlabel("Scenario cost increase (CAD millions)", labelpad=15, color=GRAY, fontsize=10)
    footer(fig,
           "Item share substitutes for spend share. Actual sourcing, tariff eligibility, pass-through and category mappings may change the estimate.",
           "Source: saved notebook output, cell 3. Rounded inputs; total ≈ CAD 70.7M. Currency follows the original case report.")
    save(fig, "03_tariff_scenario.png")


def import_dependence():
    fig = page(4, "U.S. import share shifted unevenly",
               "Canada | Selected HS codes | 2021 versus 2024 | Historical trade aggregates")
    fig.legend(handles=[Line2D([], [], marker="o", linestyle="none", color=INK, markersize=8, label="2021"),
                        Line2D([], [], marker="o", linestyle="none", color=TEAL, markersize=8, label="2024")],
               loc="center left", bbox_to_anchor=(.055, .812), frameon=False, ncol=2, fontsize=10, columnspacing=2)
    rows = sorted(IMPORTS, key=lambda row: -row[2])
    ax = axes(fig, [.30, .2, .625, .555])
    for i, (_, first, last) in enumerate(rows):
        ax.plot([first, last], [i, i], color="#B9C9D4", linewidth=3, zorder=1)
        ax.scatter([first, last], [i, i], color=[INK, TEAL], s=65, edgecolor=BG, linewidth=1.2, zorder=2)
        # Values flank the pair, so close observations remain legible.
        ax.text(first, i - .18, f"{first:.1f}", color=INK, fontsize=10, ha="center")
        ax.text(last, i + .30, f"{last:.1f}", color=TEAL, fontsize=10, ha="center")
        ax.text(110, i, f"{last-first:+.1f} pp", color=INK, fontsize=10, ha="right", va="center")
    ax.text(110, -.7, "CHANGE", ha="right", color=GRAY, fontsize=9, weight="bold")
    ax.set_yticks(range(10), [f"{HS_LABELS[code]} · {code}" for code, _, _ in rows], color=INK)
    ax.set_ylim(9.65, -.65)
    ax.set_xlim(0, 113)
    ax.set_xticks(range(0, 101, 20))
    ax.set_xlabel("U.S. share of Canadian imports in each HS group (%)", labelpad=15, color=GRAY)
    footer(fig,
           "Share = imports from the U.S. / imports from the world. These trade aggregates provide context, not supplier-level exposure.",
           "Source: saved output, cell 7; category aliases from cell 11. Shares retain 0.1% precision; changes are percentage points (pp).")
    save(fig, "04_import_dependence.png")


def supplier_screen():
    fig = page(5, "Supplier records need a second screen",
               "Vendor records without U.S. restriction flag | Selected categories | Counts by recorded performance",
               size=(14, 10))
    fig.text(.06, .809, "All five performance bands retained; counts do not establish supplier suitability.", color=GRAY, fontsize=11)
    ax = fig.add_axes([.055, .172, .89, .582])
    ax.set_xlim(0, 11.4)
    ax.set_ylim(11.65, -1.05)
    ax.axis("off")
    columns = [("Excellent", 2, INK), ("Good", 3, TEAL), ("Average", 0, GRAY),
               ("Developing", 1, "#9B8156"), ("Poor", 4, CORAL)]
    xs = [5.0 + i * 1.1 for i in range(5)]
    for x, (name, _, color) in zip(xs, columns):
        ax.text(x, -.63, name, ha="center", color=color, fontsize=11, weight="bold")
    ax.text(11.08, -.63, "Total", ha="center", color=INK, fontsize=11, weight="bold")
    # Match the priority figure's order so readers can connect risk and screening.
    for row, (cat, _, _) in enumerate(PRIORITIES):
        values = PERFORMANCE[cat]
        ax.text(.06, row, LABELS[cat], ha="left", va="center", color=INK, fontsize=11)
        for x, (_, source_column, color) in zip(xs, columns):
            value = values[source_column]
            alpha = .06 if value == 0 else .13 + .32 * (value / 51)
            patch = FancyBboxPatch((x-.48, row-.35), .96, .70,
                                   boxstyle="round,pad=0.02,rounding_size=0.06",
                                   facecolor=color, edgecolor="none", alpha=alpha)
            ax.add_patch(patch)
            ax.text(x, row, str(value), ha="center", va="center", color=INK,
                    fontsize=12, weight="bold" if value else "normal", alpha=1 if value else .55)
        ax.text(11.08, row, str(sum(values)), ha="center", va="center", color=INK, fontsize=11, weight="bold")
    footer(fig,
           "Source filter: RestrictedUSVendor ≠ Y. This is not proof of non-U.S. origin, qualification or available capacity.",
           "Source: saved notebook output, cell 6. Counts are vendor records and may not represent unique suppliers; no vendor identities are shown.")
    save(fig, "05_supplier_screen.png")


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.unicode_minus": True, "savefig.bbox": None})
    assert len(PRIORITIES) == len(EXPOSURE) == len(PERFORMANCE) == 11
    assert sum(us for _, _, us, _ in EXPOSURE) == 24
    assert all(supply < lead for _, _, lead, supply in COVERAGE)
    assert len(IMPORTS) == 10 and all(0 <= value <= 100 for _, *values in IMPORTS for value in values)
    priority_scores()
    coverage_gaps()
    tariff_scenario()
    import_dependence()
    supplier_screen()


if __name__ == "__main__":
    main()
