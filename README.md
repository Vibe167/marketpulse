# 📈 MarketPulse — Market Regime Detection System

> Unsupervised deep learning pipeline that identifies hidden market regimes from 30 years of S&P 500 data — Bull, Transition, and Crisis states — validated statistically and backtested against buy-and-hold.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red?style=flat-square&logo=pytorch)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b?style=flat-square&logo=streamlit)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=flat-square&logo=mongodb)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 What This Project Does

Most financial models assume markets behave the same way all the time. They don't. This system automatically detects **which behavioral state the market is currently in** — without any human-defined labels — and recommends portfolio allocation accordingly.

**Three regimes detected:**
- 🟢 **Bull / Calm** — Low volatility, positive drift, stable growth
- 🟡 **Transition** — Rising uncertainty, mixed signals
- 🔴 **Crisis / Bear** — High volatility, negative skew, market stress

---

## ✨ Key Features

- **Live regime detection** — Downloads today's market data and classifies current regime in real time
- **LSTM Autoencoder** — Compresses 30-day market windows into 16-dimensional latent representations
- **Novel VIX Spread feature** — Implied minus realized volatility, spikes *before* crashes (predictive, not reactive)
- **Statistical validation** — ANOVA p < 0.001 across all features
- **Portfolio advisor** — Regime-adaptive allocation for Conservative, Moderate, and Aggressive profiles
- **User authentication** — MongoDB Atlas sign-up / sign-in system
- **Interactive dashboard** — 4-page Streamlit web application

---

## 🏗️ Project Architecture

```
Raw Data (yfinance)
        ↓
Feature Engineering (8 rolling features)
        ↓
StandardScaler normalization
        ↓
Sliding windows → shape (7887, 30, 8)
        ↓
LSTM Autoencoder → 16-dim latent vectors
        ↓
K-Means + GMM Clustering → 3 regime labels
        ↓
Statistical Validation (ANOVA p<0.001)
        ↓
Portfolio Backtest + Live Dashboard
```

---

## 📊 The 8 Features

| Feature | Description | Why It Matters |
|---------|-------------|----------------|
| Rolling Mean Return | 20-day average return | Trend direction |
| Realized Volatility | Annualized std of returns | Strongest regime signal |
| Skewness | Return distribution asymmetry | Crashes = negative skew |
| Kurtosis | Fat tail measurement | Crisis = extreme kurtosis |
| Sharpe Ratio | Risk-adjusted return | Regime quality metric |
| VIX Level | Implied fear gauge | Market stress indicator |
| **VIX Spread** ⭐ | Implied − Realized volatility | **Novel predictive signal** |
| SP500-VIX Correlation | Rolling correlation | Flips sign during crises |

> ⭐ **Novel contribution:** The VIX Spread feature spikes before crashes, not during them — making it a leading indicator unavailable in prior literature.

---

## 🧠 Model Details

### LSTM Autoencoder

```
Input: (batch, 30, 8)  — 30 days, 8 features
         ↓
Encoder LSTM → hidden state (batch, 16)  — latent vector
         ↓
Decoder LSTM → reconstructed sequence (batch, 30, 8)
         ↓
Loss: MSE reconstruction error
```

- **Optimizer:** Adam (lr=0.001)
- **Epochs:** 20
- **Batch size:** 32
- **Latent dimensions:** 16
- **Training windows:** 7,887

### Clustering

- **K-Means** with K=3 (selected via elbow + silhouette score)
- **Gaussian Mixture Model** for soft probabilistic labels
- **UMAP** for 2D visualization of latent space

---

## 📁 Project Structure

```
MarketRegime/
│
├── app.py                          # Streamlit web application
├── setup_db.py                     # MongoDB setup script (run once)
│
├── notebooks/
│   ├── feature_engineering.ipynb   # Feature computation
│   ├── Analysis.ipynb              # EDA and visualizations
│   ├── LSTM_Autoencoder.ipynb      # Model training
│   ├── 06_clustering.ipynb         # Regime clustering
│   └── Portfolio_Backtest.ipynb    # Strategy backtesting
│
├── data/
│   ├── features_20d.csv            # Engineered feature matrix
│   ├── features_60d.csv            # 60-day window features
│   ├── lstm_embeddings.csv         # Latent vectors (7887 × 16)
│   ├── regime_labels.csv           # K-Means + GMM regime labels
│   ├── analysis_with_regimes.csv   # Features joined with labels
│   └── sp500_clean.csv             # Raw cleaned price data
│
├── figures/
│   ├── eda_full.png                # 8-panel EDA figure
│   ├── umap_visualization.png      # UMAP cluster plot
│   ├── regimes_over_time.png       # Regime timeline
│   ├── cluster_selection.png       # Elbow + silhouette plots
│   ├── regime_volatility_comparison.png
│   ├── backtest_returns.png        # Cumulative return comparison
│   ├── strategy_comparison.png     # Adaptive vs static
│   └── drawdown_comparison.png     # Drawdown comparison
│
├── .streamlit/
│   └── secrets.toml                # MongoDB URI (not committed)
│
└── requirements.txt                # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Anaconda or Miniconda
- MongoDB Atlas account (free tier)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/market-regime-detection.git
cd market-regime-detection
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up MongoDB**

Create `.streamlit/secrets.toml`:
```toml
MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
```

Run the database setup script:
```bash
python setup_db.py
```

**4. Run the application**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📦 Requirements

```
streamlit
pandas
numpy
matplotlib
plotly
yfinance
torch
torchvision
scikit-learn
scipy
umap-learn
pymongo
bcrypt
```

Install all at once:
```bash
pip install streamlit pandas numpy matplotlib plotly yfinance torch scikit-learn scipy umap-learn pymongo bcrypt
```

---

## 📈 Results

| Metric | Adaptive Strategy | Static 60/40 |
|--------|------------------|--------------|
| Sharpe Ratio | Higher | Baseline |
| Max Drawdown | Lower | Higher |
| Crisis Protection | ✅ Yes | ❌ No |
| Regime-aware | ✅ Yes | ❌ No |

**Statistical validation:**
- ANOVA p-value < 0.001 across all features
- Three regimes are statistically distinct — not clustering artifacts
- Crisis regime shows significantly higher volatility, kurtosis, and VIX spread

---

## 🌐 Web Application

The Streamlit app has 4 pages:

| Page | Description |
|------|-------------|
| 🏠 Live Dashboard | Real-time regime detection + S&P 500 chart |
| 📊 Historical Analysis | 30-year regime visualization + VIX spread |
| 💼 Portfolio Advisor | Regime-adaptive allocation recommendation |
| 🧠 About the Model | Architecture, pipeline, research contributions |

---

## 🔬 Research Paper

This project is accompanied by a research paper:

> **"Unsupervised Market Regime Detection via LSTM Autoencoder with Novel VIX Spread Features"**
>
> Submitted to arXiv — q-fin.ST (Statistical Finance)

**Key contributions:**
1. VIX Spread as a predictive regime feature
2. LSTM autoencoder for unsupervised temporal representation learning
3. SP500-VIX rolling correlation as a structural breakdown signal
4. Three-way validation: visual (UMAP) + statistical (ANOVA) + economic (backtest)

---

## 👥 Team

| Member | Role |
|--------|------|
| Vaishnavi | Lead — Feature engineering, LSTM model, clustering, backtesting, web app |

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. It is not financial advice. Do not make real investment decisions based on this system.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [yfinance](https://github.com/ranaroussi/yfinance) for market data
- [PyTorch](https://pytorch.org/) for deep learning framework
- [Streamlit](https://streamlit.io/) for the web interface
- [MongoDB Atlas](https://www.mongodb.com/atlas) for database
- Hamilton (1989) for foundational regime-switching theory
