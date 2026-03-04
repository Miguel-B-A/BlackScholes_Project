import numpy as np
from scipy.stats import norm
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BSM Options Calculator",
    page_icon="📈",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Mono', monospace; }

.stApp { background-color: #0a0c0f; color: #e8edf5; }

h1, h2, h3 { font-family: 'IBM Plex Mono', monospace !important; }

.price-box {
    border-radius: 4px;
    padding: 24px;
    text-align: center;
    margin-bottom: 8px;
}
.call-box {
    background: rgba(0,212,170,0.08);
    border: 1px solid rgba(0,212,170,0.3);
}
.put-box {
    background: rgba(255,77,109,0.08);
    border: 1px solid rgba(255,77,109,0.3);
}
.price-label { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 8px; }
.call-label { color: #00d4aa; }
.put-label  { color: #ff4d6d; }
.price-value { font-size: 40px; font-weight: 600; }
.call-value { color: #00d4aa; }
.put-value  { color: #ff4d6d; }
.price-sub  { font-size: 12px; color: #6b7a94; margin-top: 4px; }

.greek-box {
    background: #111318;
    border: 1px solid #1e2530;
    border-radius: 4px;
    padding: 14px 16px;
    margin-bottom: 8px;
}
.greek-name { font-size: 10px; color: #6b7a94; letter-spacing: 1px; text-transform: uppercase; }
.greek-sym  { color: #00d4aa; }
.greek-val  { font-size: 20px; font-weight: 500; color: #e8edf5; margin-top: 4px; }

.info-box {
    background: #111318;
    border: 1px solid #1e2530;
    border-radius: 4px;
    padding: 14px 16px;
    margin-bottom: 8px;
}
.info-key { font-size: 10px; color: #6b7a94; letter-spacing: 2px; text-transform: uppercase; }
.info-val { font-size: 16px; color: #00d4aa; margin-top: 4px; }

.section-label {
    font-size: 10px;
    letter-spacing: 3px;
    color: #6b7a94;
    text-transform: uppercase;
    border-bottom: 1px solid #1e2530;
    padding-bottom: 8px;
    margin-bottom: 16px;
    margin-top: 8px;
}

.badge-itm { background: rgba(0,212,170,0.15); color:#00d4aa; padding:3px 10px; border-radius:3px; font-size:11px; letter-spacing:2px; }
.badge-otm { background: rgba(255,77,109,0.15); color:#ff4d6d; padding:3px 10px; border-radius:3px; font-size:11px; letter-spacing:2px; }
.badge-atm { background: rgba(255,165,0,0.15);  color:orange;  padding:3px 10px; border-radius:3px; font-size:11px; letter-spacing:2px; }

div[data-testid="stSlider"] > div { padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── BSM Functions ─────────────────────────────────────────────────────────────
class BS:
    def __init__(self, spot, strike, rate, days, volatility, multiplier=100):
        self.S = spot
        self.K = strike
        self.r = rate / 100
        self.T = days / 365
        self.sigma = volatility / 100
        self.mult = multiplier

        self.d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) \
                  / (self.sigma * np.sqrt(self.T))
        self.d2 = self.d1 - self.sigma * np.sqrt(self.T)

    @property
    def call_price(self):
        return self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)

    @property
    def put_price(self):
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)

    @property
    def delta(self):
        return norm.cdf(self.d1), norm.cdf(self.d1) - 1  # call, put

    @property
    def gamma(self):
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))

    @property
    def theta(self):
        call = (-(self.S * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T))
                - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)) / 365
        return call

    @property
    def vega(self):
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) / 100

    @property
    def rho(self):
        return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) / 100

    @property
    def moneyness(self):
        ratio = self.S / self.K
        pct = (ratio - 1) * 100
        if abs(pct) < 1:
            return "ATM", pct
        elif self.S > self.K:
            return "ITM", pct
        else:
            return "OTM", pct


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-left:3px solid #00d4aa; padding-left:16px; margin-bottom:32px">
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

# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1.2], gap="large")

# ── Inputs ────────────────────────────────────────────────────────────────────
with left:
    st.markdown('<div class="section-label">Parameters</div>', unsafe_allow_html=True)

    spot   = st.slider("Spot Price ($)",    min_value=1.0,   max_value=1000.0, value=100.0, step=0.5,  format="$%.2f")
    strike = st.slider("Strike Price ($)",  min_value=1.0,   max_value=1000.0, value=100.0, step=0.5,  format="$%.2f")
    rate   = st.slider("Risk-free Rate (%)",min_value=0.0,   max_value=30.0,   value=5.0,   step=0.1,  format="%.1f%%")
    days   = st.slider("Days to Expiry",    min_value=1,     max_value=730,    value=30,    step=1)
    vol    = st.slider("Volatility σ (%)",  min_value=1.0,   max_value=200.0,  value=20.0,  step=0.5,  format="%.1f%%")

    c1, c2 = st.columns(2)
    with c1:
        mult = st.number_input("Contract Multiplier", min_value=1, value=100, step=1)

# ── Calculate ─────────────────────────────────────────────────────────────────
bs = BS(spot, strike, rate, days, vol, mult)

# ── Results ───────────────────────────────────────────────────────────────────
with right:
    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

    # Prices
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

    # Greeks
    st.markdown('<div class="section-label" style="margin-top:20px">Greeks</div>', unsafe_allow_html=True)
    delta_c, delta_p = bs.delta
    g1, g2, g3 = st.columns(3)
    g4, g5, g6 = st.columns(3)

    with g1:
        st.markdown(f'<div class="greek-box"><div class="greek-name">Delta <span class="greek-sym">Δ</span></div><div class="greek-val">{delta_c:.4f} / {delta_p:.4f}</div></div>', unsafe_allow_html=True)
    with g2:
        st.markdown(f'<div class="greek-box"><div class="greek-name">Gamma <span class="greek-sym">Γ</span></div><div class="greek-val">{bs.gamma:.4f}</div></div>', unsafe_allow_html=True)
    with g3:
        st.markdown(f'<div class="greek-box"><div class="greek-name">Theta <span class="greek-sym">Θ</span></div><div class="greek-val">{bs.theta:.4f}</div></div>', unsafe_allow_html=True)
    with g4:
        st.markdown(f'<div class="greek-box"><div class="greek-name">Vega <span class="greek-sym">V</span></div><div class="greek-val">{bs.vega:.4f}</div></div>', unsafe_allow_html=True)
    with g5:
        st.markdown(f'<div class="greek-box"><div class="greek-name">Rho <span class="greek-sym">ρ</span></div><div class="greek-val">{bs.rho:.4f}</div></div>', unsafe_allow_html=True)
    with g6:
        st.markdown(f'<div class="greek-box"><div class="greek-name">d₁ / d₂</div><div class="greek-val" style="font-size:14px">{bs.d1:.3f} / {bs.d2:.3f}</div></div>', unsafe_allow_html=True)

    # Moneyness
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
    if bar_pct > mid:
        left_pos, width = mid, bar_pct - mid
    else:
        left_pos, width = bar_pct, mid - bar_pct

    st.markdown(f"""
    <div style="position:relative;height:6px;background:#1e2530;border-radius:3px;margin-bottom:24px">
        <div style="position:absolute;left:{left_pos}%;width:{width}%;height:100%;background:{fill_color};border-radius:3px"></div>
        <div style="position:absolute;left:{bar_pct}%;transform:translateX(-50%);top:-4px;width:3px;height:14px;background:#e8edf5;border-radius:1px"></div>
    </div>""", unsafe_allow_html=True)

# ── Info bar ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Contract Summary</div>', unsafe_allow_html=True)
i1, i2, i3, i4, i5 = st.columns(5)

parity = bs.call_price - bs.put_price
intrinsic = max(0, spot - strike)
weeks = (days / 365) * 52

items = [
    ("Call Contract Value", f"${bs.call_price * mult:,.2f}"),
    ("Put Contract Value",  f"${bs.put_price * mult:,.2f}"),
    ("Put-Call Parity",     f"${parity:.4f}"),
    ("Time to Expiry",      f"{days}d ≈ {weeks:.1f}w"),
    ("Intrinsic Value (C)", f"${intrinsic:.2f}"),
]

for col, (key, val) in zip([i1, i2, i3, i4, i5], items):
    with col:
        st.markdown(f'<div class="info-box"><div class="info-key">{key}</div><div class="info-val">{val}</div></div>', unsafe_allow_html=True)
