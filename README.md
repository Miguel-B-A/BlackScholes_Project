# 📈 BlackScholes_Project

A personal implementation of the **Black–Scholes–Merton (BSM)** model for pricing European-style options, with an interactive Streamlit dashboard.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blackscholes-project-miguel-b-a.streamlit.app)

---

## 🧠 What is the Black–Scholes–Merton Model?

The **Black–Scholes–Merton (BSM)** model is the mathematical framework used to determine the **theoretical fair price of European-style options**. It was introduced by Fischer Black, Myron Scholes, and Robert Merton in 1973, and it revolutionized quantitative finance — Scholes and Merton were awarded the Nobel Prize in Economics in 1997.

### Core Formula

The model prices a **Call** and **Put** option as follows:

```
C = S · N(d₁) - K · e^(-rT) · N(d₂)
P = K · e^(-rT) · N(-d₂) - S · N(-d₁)
```

Where:

```
d₁ = [ ln(S/K) + (r + σ²/2) · T ] / (σ · √T)
d₂ = d₁ - σ · √T
```

| Symbol | Description |
|--------|-------------|
| `S`    | Current spot price of the underlying asset |
| `K`    | Strike price of the option |
| `r`    | Risk-free interest rate (annualized) |
| `T`    | Time to expiration (in years) |
| `σ`    | Implied volatility of the underlying (annualized) |
| `N(x)` | Cumulative standard normal distribution function |

### Key Assumptions

- The underlying asset follows a **log-normal distribution**
- No dividends are paid during the option's life
- Markets are **frictionless** (no transaction costs or taxes)
- The risk-free rate and volatility are **constant** over the option's life
- The option can only be exercised **at expiration** (European-style)

---

## 🔢 The Greeks

The Greeks measure the **sensitivity of the option price** to changes in market parameters:

| Greek | Symbol | Description |
|-------|--------|-------------|
| Delta | Δ | Change in option price per $1 move in spot price |
| Gamma | Γ | Rate of change of Delta per $1 move in spot price |
| Theta | Θ | Daily time decay of the option price |
| Vega  | V | Change in price per 1% change in volatility |
| Rho   | ρ | Change in price per 1% change in interest rate |

---

## 📊 Features

- ✅ Real-time Call & Put pricing
- ✅ Full Greeks calculation (Δ, Γ, Θ, V, ρ)
- ✅ Moneyness indicator (ITM / ATM / OTM)
- ✅ Contract value with multiplier
- ✅ Put-Call parity check
- ✅ Interactive **heatmap** — visualize Call & Put prices across Spot × Volatility ranges
- ✅ Dark-themed professional UI

---

## 🗂️ Project Structure

```
BlackScholes_Project/
├── black_scholes.py   # BSM logic — class BS with all calculations
├── app.py             # Streamlit interface + heatmap
└── README.md
```

The project is intentionally split into two files:

- **`black_scholes.py`** — pure Python/math, no UI dependencies. Contains the `BS` class.
- **`app.py`** — imports `BS` and handles all the Streamlit interface and visualizations.

---

## 🚀 How to Run Locally

### 1. Prerequisites

Make sure you have **Python 3.10+** installed. You can check with:

```bash
python --version
```

> On Windows, if `python` is not recognized, try `py --version`. If neither works, download Python from [python.org](https://python.org/downloads) and make sure to check **"Add Python to PATH"** during installation.

### 2. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/BlackScholes_Project.git
cd BlackScholes_Project
```

### 3. Install dependencies

```bash
pip install streamlit numpy scipy matplotlib seaborn
```

> On Windows, if `pip` is not recognized, use:
> ```bash
> python -m pip install streamlit numpy scipy matplotlib seaborn
> ```

### 4. Run the app

```bash
streamlit run app.py
```

> On Windows, if `streamlit` is not recognized, use:
> ```bash
> python -m streamlit run app.py
> ```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web interface |
| `numpy` | Numerical computations |
| `scipy` | Normal distribution (CDF/PDF) |
| `matplotlib` | Heatmap rendering |
| `seaborn` | Heatmap styling |

---

## 📖 References

- Black, F. & Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities*. Journal of Political Economy.
- Merton, R. C. (1973). *Theory of Rational Option Pricing*. Bell Journal of Economics.
- Hull, J. C. — *Options, Futures, and Other Derivatives*

---

## 🙌 Inspiration

Inspired by [prudhvi-reddy-m/BlackScholes](https://github.com/prudhvi-reddy-m/BlackScholes).
