import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

from black_scholes import BS  # solo necesita la clase BS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="BSM Options Calculator", page_icon="📈", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Mono', monospace; }
.stApp { background-color: #0a0c0f; color: #e8edf5; }
h1,h2,h3 { font-family: 'IBM Plex Mono', monospace !important; }

.price-box  { border-radius:4px; padding:24px; text-align:center; margin-bottom:8px; }
.call-box   { background:rgba(0,212,170,0.08); border:1px solid rgba(0,212,170,0.3); }
.put-box    { background:rgba(255,77,109,0.08); border:1px solid rgba(255,77,109,0.3); }
.price-label{ font-size:11px; letter-spacing:3px; text-transform:uppercase; margin-bottom:8px; }
.call-label { color:#00d4aa; }
.put-label  { color:#ff4d6d; }
.price-value{ font-size:40px; font-weight:600; }
.call-value { color:#00d4aa; }
.put-value  { color:#ff4d6d; }
.price-sub  { font-size:12px; color:#6b7a94; margin-top:4px; }

.greek-box  { background:#111318; border:1px solid #1e2530; border-radius:4px; padding:14px 16px; margin-bottom:8px; }
.greek-name { font-size:10px; color:#6b7a94; letter-spacing:1px; text-transform:uppercase; }
.greek-sym  { color:#00d4aa; }
.greek-val  { font-size:20px; font-weight:500; color:#e8edf5; margin-top:4px; }

.info-box   { background:#111318; border:1px solid #1e2530; border-radius:4px; padding:14px 16px; margin-bottom:8px; }
.info-key   { font-size:10px; color:#6b7a94; letter-spacing:2px; text-transform:uppercase; }
.info-val   { font-size:16px; color:#00d4aa; margin-top:4px; }

.section-label { font-size:10px; letter-spacing:3px; color:#6b7a94; text-transform:uppercase;
                 border-bottom:1px solid #1e2530; padding-bottom:8px; margin-bottom:16px; margin-top:8px; }

.badge-itm { background:rgba(0,212,170,0.15); color:#00d4aa; padding:3px 10px; border-radius:3px; font-size:11px; letter-spacing:2px; }
.badge-otm { background:rgba(255,77,109,0.15); color:#ff4d6d; padding:3px 10px; border-radius:3px; font-size:11px; letter-spacing:2px; }
.badge-atm { background:rgba(255,165,0,0.15);  color:orange;  padding:3px 10px; border-radius:3px; font-size:11px; letter-spacing:2px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-left:3px solid #00d4aa;padding-left:16px;margin-bottom:32px">
    <div style="font-size:10px;letter-spacing:3px;color:#00d4aa;text-transform:uppercase;margin-bottom:6px">
        Black–Scholes–Merton Model
    </div>
    <h1 style="font-size:36px;font-weight:600;letter-spacing:-1px;margin:0;color:#e8edf5">
        Options <span style="color:#00d4aa">Pricer</span>
    </h1>
    <div style="font-size:12px;color:#6b7a94;margin-top:6px">
        // European-style options calculator · BSM framework
    </div>
</div>
""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1.2], gap="large")

with left:
    st.markdown('<div class="section-label">Parameters</div>', unsafe_allow_html=True)
    spot   = st.slider("Spot Price ($)",     1.0,  1000.0, 100.0, 0.5,  format="$%.2f")
    strike = st.slider("Strike Price ($)",   1.0,  1000.0, 100.0, 0.5,  format="$%.2f")
    rate   = st.slider("Risk-free Rate (%)", 0.0,  30.0,   5.0,   0.1,  format="%.1f%%")
    days   = st.slider("Days to Expiry",     1,    730,    30,    1)
    vol    = st.slider("Volatility σ (%)",   1.0,  200.0,  20.0,  0.5,  format="%.1f%%")
    mult   = st.number_input("Contract Multiplier", min_value=1, value=100, step=1)

# ── Model ─────────────────────────────────────────────────────────────────────
bs = BS(spot, strike, rate, days, vol, mult)

# ── Results ───────────────────────────────────────────────────────────────────
with right:
    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        st.markdown(f"""
        <div class="price-box call-box">
            <div class="price-label call-label">Call Option</div>
            <div class="price-value call-value">${bs.call_price:.2f}</div>
            <div class="price-sub">per share</div>
        </div>""", unsafe_allow_html=True)
    with pc2:
        st.markdown(f"""
        <div class="price-box put-box">
            <div class="price-label put-label">Put Option</div>
            <div class="price-value put-value">${bs.put_price:.2f}</div>
            <div class="price-sub">per share</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:20px">Greeks</div>', unsafe_allow_html=True)
    delta_c, delta_p = bs.delta
    g1, g2, g3 = st.columns(3)
    g4, g5, g6 = st.columns(3)
    with g1: st.markdown(f'<div class="greek-box"><div class="greek-name">Delta <span class="greek-sym">Δ</span></div><div class="greek-val">{delta_c:.4f} / {delta_p:.4f}</div></div>', unsafe_allow_html=True)
    with g2: st.markdown(f'<div class="greek-box"><div class="greek-name">Gamma <span class="greek-sym">Γ</span></div><div class="greek-val">{bs.gamma:.4f}</div></div>', unsafe_allow_html=True)
    with g3: st.markdown(f'<div class="greek-box"><div class="greek-name">Theta <span class="greek-sym">Θ</span></div><div class="greek-val">{bs.theta:.4f}</div></div>', unsafe_allow_html=True)
    with g4: st.markdown(f'<div class="greek-box"><div class="greek-name">Vega <span class="greek-sym">V</span></div><div class="greek-val">{bs.vega:.4f}</div></div>', unsafe_allow_html=True)
    with g5: st.markdown(f'<div class="greek-box"><div class="greek-name">Rho <span class="greek-sym">ρ</span></div><div class="greek-val">{bs.rho:.4f}</div></div>', unsafe_allow_html=True)
    with g6: st.markdown(f'<div class="greek-box"><div class="greek-name">d₁ / d₂</div><div class="greek-val" style="font-size:14px">{bs.d1:.3f} / {bs.d2:.3f}</div></div>', unsafe_allow_html=True)

    status, pct = bs.moneyness
    badge_class = {"ITM": "badge-itm", "OTM": "badge-otm", "ATM": "badge-atm"}[status]
    pct_str = f"+{pct:.2f}%" if pct >= 0 else f"{pct:.2f}%"
    st.markdown(f"""
    <div style="margin-top:16px">
        <div class="section-label" style="display:flex;justify-content:space-between;align-items:center">
            <span>Moneyness <span class="{badge_class}">{status}</span></span>
            <span style="color:#e8edf5">{pct_str}</span>
        </div>
    </div>""", unsafe_allow_html=True)
    bar_pct = min(max((spot / strike - 0.5) / 1.0 * 100, 0), 100)
    mid = 50
    fill_color = "#00d4aa" if status == "ITM" else ("#ff4d6d" if status == "OTM" else "orange")
    lp, w = (mid, bar_pct - mid) if bar_pct > mid else (bar_pct, mid - bar_pct)
    st.markdown(f"""
    <div style="position:relative;height:6px;background:#1e2530;border-radius:3px;margin-bottom:24px">
        <div style="position:absolute;left:{lp}%;width:{w}%;height:100%;background:{fill_color};border-radius:3px"></div>
        <div style="position:absolute;left:{bar_pct}%;transform:translateX(-50%);top:-4px;width:3px;height:14px;background:#e8edf5;border-radius:1px"></div>
    </div>""", unsafe_allow_html=True)

# ── Contract Summary ──────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Contract Summary</div>', unsafe_allow_html=True)
i1, i2, i3, i4, i5 = st.columns(5)
weeks = (days / 365) * 52
for col, (key, val) in zip([i1, i2, i3, i4, i5], [
    ("Call Contract Value", f"${bs.call_price * bs.mult:,.2f}"),
    ("Put Contract Value",  f"${bs.put_price  * bs.mult:,.2f}"),
    ("Put-Call Parity",     f"${bs.put_call_parity:.4f}"),
    ("Time to Expiry",      f"{days}d ≈ {weeks:.1f}w"),
    ("Intrinsic Value (C)", f"${bs.intrinsic_value:.2f}"),
]):
    with col:
        st.markdown(f'<div class="info-box"><div class="info-key">{key}</div><div class="info-val">{val}</div></div>', unsafe_allow_html=True)

# ── Heatmap Section ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-label">Heatmap Explorer · Spot Price vs Volatility</div>', unsafe_allow_html=True)
st.info("🟢 Verde = precio más alto  ·  🔴 Rojo = precio más bajo  ·  El recuadro blanco marca los parámetros actuales.")

hc1, hc2, hc3, hc4 = st.columns(4)
with hc1:
    spot_min = st.number_input("Min Spot Price", min_value=0.01, value=round(spot * 0.8, 2), step=1.0)
with hc2:
    spot_max = st.number_input("Max Spot Price", min_value=0.01, value=round(spot * 1.2, 2), step=1.0)
with hc3:
    vol_min = st.slider("Min Volatility", min_value=0.01, max_value=1.0, value=round(min((vol / 100) * 0.5, 0.99), 2), step=0.01)
with hc4:
    vol_max = st.slider("Max Volatility", min_value=0.01, max_value=2.0, value=round((vol / 100) * 1.5, 2), step=0.01)

if spot_min >= spot_max:
    st.warning("Min Spot debe ser menor que Max Spot.")
elif vol_min >= vol_max:
    st.warning("Min Volatility debe ser menor que Max Volatility.")
else:
    with st.spinner("Calculando heatmap..."):
        n = 15
        spot_range = np.linspace(spot_min, spot_max, n)
        vol_range  = np.linspace(vol_min,  vol_max,  n)

        call_grid = np.zeros((n, n))
        put_grid  = np.zeros((n, n))

        # Iterar sobre cada combinación de Spot y Volatilidad
        for i, v in enumerate(vol_range):
            for j, s in enumerate(spot_range):
                model = BS(s, strike, rate, days, v * 100, mult)
                call_grid[i, j] = model.call_price
                put_grid[i, j]  = model.put_price

    # Colormap rojo → amarillo → verde
    rg_cmap = mcolors.LinearSegmentedColormap.from_list(
        "rg", ["#7f0000", "#c0392b", "#e74c3c", "#f39c12", "#f1c40f", "#2ecc71", "#006400"]
    )

    x_labels = [f"{v:.1f}"  for v in spot_range]
    y_labels  = [f"{v:.2f}" for v in vol_range]

    # Posición actual en el grid
    cx = int(np.argmin(np.abs(spot_range - spot)))
    cy = int(np.argmin(np.abs(vol_range  - (vol / 100))))

    fig, (ax_call, ax_put) = plt.subplots(1, 2, figsize=(18, 7))
    fig.patch.set_facecolor("#0a0c0f")

    for ax, grid, title in [
        (ax_call, call_grid, "CALL"),
        (ax_put,  put_grid,  "PUT"),
    ]:
        ax.set_facecolor("#111318")
        sns.heatmap(
            grid,
            xticklabels=x_labels,
            yticklabels=y_labels,
            annot=True,
            fmt=".2f",
            cmap=rg_cmap,
            linewidths=0.4,
            linecolor="#1e2530",
            ax=ax,
            cbar_kws={"shrink": 0.8},
            annot_kws={"size": 8, "color": "white", "fontfamily": "monospace"},
        )

        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color="white", labelsize=8)
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#aab0c0", fontfamily="monospace")
        cbar.outline.set_edgecolor("#1e2530")

        # Marcar posición actual
        ax.add_patch(plt.Rectangle((cx, cy), 1, 1, fill=False,
                                    edgecolor="white", lw=2.5, zorder=5))
        ax.plot(cx + 0.5, cy + 0.5, marker="+", markersize=14,
                color="white", markeredgewidth=2.5, zorder=6)

        ax.set_title(title, color="#e8edf5", fontsize=14, fontweight="bold",
                     fontfamily="monospace", pad=14)
        ax.set_xlabel("Spot Price ($)", color="#6b7a94", fontsize=10,
                      fontfamily="monospace", labelpad=8)
        ax.set_ylabel("Volatility",     color="#6b7a94", fontsize=10,
                      fontfamily="monospace", labelpad=8)
        ax.tick_params(colors="#6b7a94", labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#1e2530")

    plt.tight_layout(pad=3)
    st.pyplot(fig)
    plt.close(fig)
    st.caption("✚ El recuadro blanco indica la posición de los parámetros actuales.")
