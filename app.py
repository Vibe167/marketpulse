# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# import yfinance as yf
# import torch
# import torch.nn as nn
# from sklearn.preprocessing import StandardScaler
# from scipy.stats import skew, kurtosis
# import warnings
# import os

# warnings.filterwarnings('ignore')

# # Tell app where your data files are
# os.chdir(r"C:\Users\Vaishnavi\OneDrive\Documents\Desktop\MarketRegime")

# # ─────────────────────────────────────────
# # PAGE CONFIG
# # ─────────────────────────────────────────
# st.set_page_config(
#     page_title="Market Regime Intelligence",
#     page_icon="📈",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ─────────────────────────────────────────
# # MODEL DEFINITION — must match your trained model exactly
# # ─────────────────────────────────────────
# class LSTMAutoencoder(nn.Module):
#     def __init__(self, n_features, latent_dim=16):
#         super().__init__()
#         self.encoder = nn.LSTM(
#             input_size=n_features,
#             hidden_size=latent_dim,
#             batch_first=True
#         )
#         self.decoder = nn.LSTM(
#             input_size=latent_dim,
#             hidden_size=n_features,
#             batch_first=True
#         )

#     def forward(self, x):
#         _, (hidden, _) = self.encoder(x)
#         latent = hidden.repeat(x.shape[1], 1, 1).permute(1, 0, 2)
#         out, _ = self.decoder(latent)
#         return out

# # ─────────────────────────────────────────
# # LOAD DATA AND MODEL
# # ─────────────────────────────────────────
# @st.cache_data
# def load_historical_data():
#     regimes  = pd.read_csv('regime_labels.csv',
#                            index_col=0, parse_dates=True)
#     features = pd.read_csv('features_20d.csv',
#                            index_col=0, parse_dates=True)
#     combined = features.join(regimes['kmeans_regime'],
#                              how='inner').dropna()
#     return combined

# @st.cache_data
# def load_live_data():
#     sp500 = yf.download("^GSPC", period="6mo",
#                         progress=False, auto_adjust=True)
#     vix   = yf.download("^VIX",  period="6mo",
#                         progress=False, auto_adjust=True)
    
#     # Fix MultiIndex columns
#     if isinstance(sp500.columns, pd.MultiIndex):
#         sp500.columns = sp500.columns.get_level_values(0)
#     if isinstance(vix.columns, pd.MultiIndex):
#         vix.columns = vix.columns.get_level_values(0)
    
#     # Make sure Close column exists and has data
#     sp500 = sp500[['Close']].dropna()
#     vix   = vix[['Close']].dropna()
    
#     print("SP500 shape:", sp500.shape)
#     print("VIX shape:",   vix.shape)
    
#     return sp500, vix

# def compute_features_live(sp500, vix, W=20):
#     data = pd.DataFrame(index=sp500.index)
#     data['sp500_return'] = np.log(
#         sp500['Close'] / sp500['Close'].shift(1))
#     data['vix_close'] = vix['Close'].reindex(
#         sp500.index).ffill()
#     data = data.dropna()
#     data['rolling_mean']  = data['sp500_return'].rolling(W).mean()
#     data['realized_vol']  = data['sp500_return'].rolling(W).std() \
#                             * np.sqrt(252)
#     data['skewness']      = data['sp500_return'].rolling(W).apply(
#                                 skew, raw=True)
#     data['kurtosis']      = data['sp500_return'].rolling(W).apply(
#                                 kurtosis, raw=True)
#     data['vix_level']     = data['vix_close'].rolling(W).mean()
#     data['vix_change']    = data['vix_close'].pct_change(W)
#     realized              = data['realized_vol']
#     implied               = data['vix_close'] / 100
#     data['vix_spread']    = implied - realized
#     data['corr_sp500_vix']= data['sp500_return'].rolling(W).corr(
#                                 data['vix_close'])
#     feature_cols = ['rolling_mean', 'realized_vol', 'skewness',
#                     'kurtosis', 'vix_level', 'vix_change',
#                     'vix_spread', 'corr_sp500_vix']
#     return data[feature_cols].dropna()

# def detect_regime_live(features_df):
#     from sklearn.cluster import KMeans

#     # Load historical embeddings — convert to float32
#     hist_emb = pd.read_csv('lstm_embeddings.csv',
#                            index_col=0, parse_dates=True)
#     hist_emb_values = hist_emb.values.astype(np.float32)
#     kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
#     kmeans.fit(hist_emb_values)

#     # Normalize live features — convert to float32
#     hist_feat = pd.read_csv('features_20d.csv',
#                             index_col=0, parse_dates=True)
#     scaler = StandardScaler()
#     scaler.fit(hist_feat.values.astype(np.float32))
#     live_scaled = scaler.transform(
#         features_df.values.astype(np.float32))

#     # Create 30-day sequence
#     SEQ_LEN = 30
#     if len(live_scaled) < SEQ_LEN:
#         return None, None
#     seq = live_scaled[-SEQ_LEN:][np.newaxis, :, :]

#     # Run LSTM encoder
#     model = LSTMAutoencoder(n_features=8, latent_dim=16)
#     model.eval()
#     with torch.no_grad():
#         x = torch.tensor(seq, dtype=torch.float32)
#         _, (h, _) = model.encoder(x)
#         embedding = h.squeeze().numpy().astype(np.float32)

#     # Predict regime and confidence
#     regime     = kmeans.predict(embedding.reshape(1, -1))[0]
#     distances  = kmeans.transform(embedding.reshape(1, -1))[0]
#     confidence = 1 - (distances[regime] / distances.sum())

#     return int(regime), float(confidence)

# # ─────────────────────────────────────────
# # SIDEBAR NAVIGATION
# # ─────────────────────────────────────────
# st.sidebar.title("📈 Market Regime Intelligence")
# st.sidebar.markdown("---")
# page = st.sidebar.radio(
#     "Navigate",
#     ["🏠 Live Dashboard",
#      "📊 Historical Analysis",
#      "💼 Portfolio Advisor",
#      "🧠 About the Model"]
# )
# st.sidebar.markdown("---")
# st.sidebar.markdown("**Built by:** Vaishnavi")
# st.sidebar.markdown("**Model:** LSTM Autoencoder")
# st.sidebar.markdown("**Data:** 1993–2024 · S&P 500 + VIX")

# # ─────────────────────────────────────────
# # PAGE 1 — LIVE DASHBOARD
# # ─────────────────────────────────────────
# if page == "🏠 Live Dashboard":
#     st.title("🏠 Live Market Regime Dashboard")
#     st.markdown("Our LSTM model analyzes the last 30 days of "
#                 "market behavior and detects the current regime "
#                 "in real time.")

#     with st.spinner("Downloading live market data..."):
#         sp500, vix = load_live_data()
#         features   = compute_features_live(sp500, vix)

#     col1, col2, col3 = st.columns(3)

#     # Latest values
#     latest_ret = float(
#         np.log(sp500['Close'].iloc[-1] /
#                sp500['Close'].iloc[-2]))
#     latest_vix = float(vix['Close'].iloc[-1])
#     latest_vol = float(features['realized_vol'].iloc[-1])

#     col1.metric("S&P 500 Latest Return",
#                 f"{latest_ret*100:.2f}%",
#                 delta=f"{latest_ret*100:.2f}%")
#     col2.metric("VIX (Fear Index)",
#                 f"{latest_vix:.2f}",
#                 delta=f"{latest_vix - float(vix['Close'].iloc[-2]):.2f}")
#     col3.metric("Realized Volatility (20d)",
#                 f"{latest_vol:.4f}")

#     st.markdown("---")

#     # Regime detection
#     st.subheader("🎯 Current Market Regime")
#     regime, confidence = detect_regime_live(features)

#     regime_info = {
#         0: {"name": "🟢 Bull / Calm Market",
#             "color": "green",
#             "desc": "Low volatility, positive drift. "
#                     "Market is in a stable growth phase.",
#             "advice": "Maintain or increase equity exposure."},
#         1: {"name": "🟡 Transition / Uncertainty",
#             "color": "orange",
#             "desc": "Mixed signals. Volatility rising, "
#                     "direction unclear.",
#             "advice": "Reduce risk slightly. Monitor closely."},
#         2: {"name": "🔴 Crisis / Bear Market",
#             "color": "red",
#             "desc": "High volatility, negative skew. "
#                     "Market stress detected.",
#             "advice": "Reduce equity exposure. "
#                       "Shift to defensive assets."}
#     }

#     if regime is not None:
#         info = regime_info[regime]
#         st.markdown(
#             f"<h2 style='color:{info['color']}'>"
#             f"{info['name']}</h2>",
#             unsafe_allow_html=True)
#         st.markdown(f"**Description:** {info['desc']}")
#         st.markdown(f"**Signal confidence:** "
#                     f"{confidence*100:.1f}%")
#         st.progress(confidence)
#         st.info(f"💡 **Portfolio signal:** {info['advice']}")
#     else:
#         st.warning("Not enough data for regime detection. "
#                    "Need at least 30 trading days.")

#     # Recent market chart
#     st.subheader("📈 Recent S&P 500 Price")
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=sp500.index, y=sp500['Close'],
#         mode='lines', name='S&P 500',
#         line=dict(color='steelblue', width=2)))
#     fig.update_layout(
#         height=300, margin=dict(l=0, r=0, t=20, b=0),
#         xaxis_title="Date", yaxis_title="Price")
#     st.plotly_chart(fig, use_container_width=True)

# # ─────────────────────────────────────────
# # PAGE 2 — HISTORICAL ANALYSIS
# # ─────────────────────────────────────────
# elif page == "📊 Historical Analysis":
#     st.title("📊 Historical Regime Analysis (1993–2024)")

#     data = load_historical_data()

#     regime_colors = {0: 'green', 1: 'orange', 2: 'red'}
#     regime_names  = {0: 'Bull/Calm', 1: 'Transition',
#                      2: 'Crisis/Bear'}

#     # Volatility colored by regime
#     st.subheader("Realized Volatility by Regime")
#     fig = go.Figure()
#     for r in [0, 1, 2]:
#         mask = data['kmeans_regime'] == r
#         fig.add_trace(go.Scatter(
#             x=data.index[mask],
#             y=data['realized_vol'][mask],
#             mode='markers',
#             marker=dict(color=regime_colors[r], size=2),
#             name=regime_names[r]
#         ))
#     # Add crisis lines
#     for date, label in [('2000-03-01', 'Dot-com'),
#                          ('2008-09-15', 'GFC 2008'),
#                          ('2020-03-01', 'COVID')]:
#         fig.add_vline(x=pd.Timestamp(date).timestamp()*1000,
#                       line_dash="dash",
#                       line_color="gray",
#                       annotation_text=label)
#     fig.update_layout(height=400,
#                       xaxis_title="Date",
#                       yaxis_title="Realized Volatility")
#     st.plotly_chart(fig, use_container_width=True)

#     # Regime distribution pie chart
#     st.subheader("Regime Distribution — 30 Years of History")
#     col1, col2 = st.columns(2)

#     counts = data['kmeans_regime'].value_counts().sort_index()
#     fig_pie = go.Figure(go.Pie(
#         labels=[regime_names[i] for i in counts.index],
#         values=counts.values,
#         marker_colors=['green', 'orange', 'red']
#     ))
#     fig_pie.update_layout(height=300)
#     col1.plotly_chart(fig_pie, use_container_width=True)

#     # Key statistics per regime
#     stats = data.groupby('kmeans_regime')['realized_vol'].agg(
#         ['mean', 'std', 'count']).round(4)
#     stats.index = [regime_names[i] for i in stats.index]
#     stats.columns = ['Mean Vol', 'Std Vol', 'Days']
#     col2.markdown("**Regime Statistics**")
#     col2.dataframe(stats, use_container_width=True)

#     # VIX spread over time
#     st.subheader("VIX Spread — Novel Feature (Predictive Signal)")
#     fig2 = go.Figure()
#     fig2.add_trace(go.Scatter(
#         x=data.index, y=data['vix_spread'],
#         mode='lines', name='VIX Spread',
#         line=dict(color='darkorange', width=1)))
#     fig2.add_hline(y=0, line_dash="dash", line_color="gray")
#     for date, label in [('2008-09-15', 'GFC'),
#                          ('2020-03-01', 'COVID')]:
#      fig2.add_vline(x=pd.Timestamp(date).timestamp() * 1000, line_dash="dash",
#                        line_color="red",
#                        annotation_text=label)
#     fig2.update_layout(height=300,
#                        xaxis_title="Date",
#                        yaxis_title="Implied - Realized Vol")
#     st.plotly_chart(fig2, use_container_width=True)
#     st.caption("When VIX spread spikes above zero, a crisis "
#                "regime often follows within weeks.")

# # ─────────────────────────────────────────
# # PAGE 3 — PORTFOLIO ADVISOR
# # ─────────────────────────────────────────
# elif page == "💼 Portfolio Advisor":
#     st.title("💼 Regime-Adaptive Portfolio Advisor")
#     st.markdown("Based on the detected market regime, this system "
#                 "recommends how to allocate your portfolio.")

#     # User input
#     col1, col2 = st.columns(2)
#     portfolio_value = col1.number_input(
#         "Your portfolio value (₹ or $)",
#         min_value=1000, value=100000, step=1000)
#     risk_profile = col2.selectbox(
#         "Your risk profile",
#         ["Conservative", "Moderate", "Aggressive"])

#     st.markdown("---")

#     # Regime-based allocation table
#     allocations = {
#         "Conservative": {
#             0: {"Equity": 50, "Bonds": 40, "Gold": 10},
#             1: {"Equity": 30, "Bonds": 55, "Gold": 15},
#             2: {"Equity": 10, "Bonds": 70, "Gold": 20}
#         },
#         "Moderate": {
#             0: {"Equity": 70, "Bonds": 25, "Gold": 5},
#             1: {"Equity": 50, "Bonds": 40, "Gold": 10},
#             2: {"Equity": 20, "Bonds": 60, "Gold": 20}
#         },
#         "Aggressive": {
#             0: {"Equity": 90, "Bonds": 10, "Gold": 0},
#             1: {"Equity": 65, "Bonds": 30, "Gold": 5},
#             2: {"Equity": 30, "Bonds": 50, "Gold": 20}
#         }
#     }

#     # Get current regime
#     with st.spinner("Detecting current regime..."):
#         sp500, vix = load_live_data()
#         features   = compute_features_live(sp500, vix)
#         regime, confidence = detect_regime_live(features)

#     regime_names = {0: "🟢 Bull/Calm",
#                     1: "🟡 Transition",
#                     2: "🔴 Crisis/Bear"}

#     if regime is not None:
#         st.subheader(f"Current Regime: {regime_names[regime]}")
#         st.markdown(f"Confidence: **{confidence*100:.1f}%**")

#         alloc = allocations[risk_profile][regime]

#         # Show allocation
#         col1, col2, col3 = st.columns(3)
#         col1.metric("📈 Equity", f"{alloc['Equity']}%",
#                     f"₹{portfolio_value * alloc['Equity']//100:,}")
#         col2.metric("📉 Bonds", f"{alloc['Bonds']}%",
#                     f"₹{portfolio_value * alloc['Bonds']//100:,}")
#         col3.metric("🥇 Gold", f"{alloc['Gold']}%",
#                     f"₹{portfolio_value * alloc['Gold']//100:,}")

#         # Pie chart of allocation
#         fig = go.Figure(go.Pie(
#             labels=list(alloc.keys()),
#             values=list(alloc.values()),
#             marker_colors=['steelblue', 'lightgreen', 'gold']
#         ))
#         fig.update_layout(
#             title=f"Recommended Allocation — "
#                   f"{risk_profile} · {regime_names[regime]}",
#             height=350)
#         st.plotly_chart(fig, use_container_width=True)

#         st.info("⚠️ This is for educational purposes only. "
#                 "Not financial advice.")

# # ─────────────────────────────────────────
# # PAGE 4 — ABOUT THE MODEL
# # ─────────────────────────────────────────
# elif page == "🧠 About the Model":
#     st.title("🧠 About the Model")

#     st.markdown("""
#     ## What is market regime detection?

#     Financial markets don't behave the same way all the time.
#     Some periods are calm and predictable. Others are volatile
#     and unpredictable. We call these different **market regimes**.

#     Traditional models assume markets always behave the same way.
#     Our system automatically detects which regime the market is
#     currently in — without any human labels.

#     ## How our model works

#     1. **Download data** — Daily S&P 500 returns and VIX
#        (fear index) from 1993 to 2024
#     2. **Engineer features** — 8 rolling statistical features
#        including our novel VIX spread feature
#     3. **LSTM Autoencoder** — Compresses 30-day windows into
#        16-dimensional latent vectors
#     4. **Clustering** — K-Means groups latent vectors into
#        3 distinct regimes
#     5. **Portfolio strategy** — Adapts allocation based on
#        detected regime

#     ## Our novel contribution

#     Most papers use VIX level as a feature. We use the
#     **VIX spread** — the gap between implied volatility (VIX)
#     and realized volatility. This spread spikes *before* crashes,
#     making it predictive rather than reactive.

#     ## Results
#     """)

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Training data", "7,887 windows")
#     col2.metric("Regimes detected", "3")
#     col3.metric("History covered", "30 years")

#     st.markdown("""
#     ## Research paper
#     This project is accompanied by a research paper submitted
#     to arXiv. The paper includes statistical validation via
#     ANOVA (p<0.001) and portfolio backtesting over 1993–2024.

#     ## Team
#     Built as part of a data science research project.
#     Model: LSTM Autoencoder · Framework: PyTorch · Data: yfinance
#     """)

#     st.markdown("---")
#     st.markdown("**GitHub:** [Your repo link here]")
#     st.markdown("**Paper:** [Your arXiv link here]")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from scipy.stats import skew, kurtosis
import warnings
import os
import pymongo
import bcrypt
# from dotenv import load_dotenv
# import os
# load_dotenv()

GOOGLE_CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_verification_email(to_email, username, token):
    link = f"https://marketpulse.streamlit.app?verify={token}"
    msg = MIMEMultipart()
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = to_email
    msg["Subject"] = "Verify your MarketPulse account"
    body = f"""
    <html><body style='font-family:Arial;background:#050d1a;color:#ffffff;padding:40px;'>
        <h2 style='color:#00d4ff;'>Welcome to MarketPulse, {username}!</h2>
        <p>Click the button below to verify your account:</p>
        <a href='{link}' style='background:#00d4ff;color:#050d1a;padding:12px 24px;
           text-decoration:none;font-weight:bold;border-radius:4px;'>
           VERIFY ACCOUNT
        </a>
        <p style='color:#446688;margin-top:24px;font-size:12px;'>
           If you didn't sign up, ignore this email.
        </p>
    </body></html>
    """
    msg.attach(MIMEText(body, "html"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email sending failed: {e}")
        return False

def get_google_auth_url():
    from urllib.parse import urlencode
    params = {
        "client_id":     GOOGLE_CLIENT_ID,
        "redirect_uri":  "http://localhost:8501",
        "response_type": "code",
        "scope":         "openid email profile",
        "access_type":   "offline"
    }
    return "https://accounts.google.com/o/oauth2/auth?" + urlencode(params)

def get_google_user_info(code):
    import requests
    token_resp = requests.post("https://oauth2.googleapis.com/token", data={
        "code":          code,
        "client_id":     GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri":  "http://localhost:8501",
        "grant_type":    "authorization_code"
    }).json()
    access_token = token_resp.get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}).json()
    return user_info

warnings.filterwarnings('ignore')



import pathlib
os.chdir(pathlib.Path(__file__).parent)

# ── MongoDB connection ──
# @st.cache_resource
# def get_db():
#     client = pymongo.MongoClient(
#         "mongodb://localhost:27017/",
#         serverSelectionTimeoutMS=3000
#     )
#     client.server_info()
#     return client["marketpulse"]

@st.cache_resource
def get_db():
    client = pymongo.MongoClient(
        st.secrets["MONGO_URI"],
        serverSelectionTimeoutMS=5000
    )
    client.server_info()
    return client["marketpulse"]

db = get_db()
print("DB connected:", db.name)


st.set_page_config(
    page_title="MarketPulse — Regime Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PLOTLY THEME — all rgba, zero 8-digit hex ──
PLOTLY_THEME = dict(
    plot_bgcolor='#080f1e',
    paper_bgcolor='#080f1e',
    font=dict(color='#8899aa', family='Rajdhani'),
    xaxis=dict(
        gridcolor='#0d1f35',
        linecolor='rgba(0,212,255,0.13)',
        tickfont=dict(color='#446688', size=11)
    ),
    yaxis=dict(
        gridcolor='#0d1f35',
        linecolor='rgba(0,212,255,0.13)',
        tickfont=dict(color='#446688', size=11)
    ),
    legend=dict(
        bgcolor='rgba(13,31,53,0.53)',
        bordercolor='rgba(0,212,255,0.13)',
        borderwidth=1,
        font=dict(color='#8899aa', size=11)
    )
)

# ── CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&family=Inter:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #050d1a !important; color: #e0e8f0 !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #0a1628 0%, #050d1a 60%) !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080f1e 0%, #0a1628 100%) !important;
    border-right: 1px solid rgba(0,212,255,0.13) !important;
}
[data-testid="stSidebar"] * { color: #c8d8e8 !important; }
h1, h2, h3 { font-family: 'Rajdhani', sans-serif !important; letter-spacing: 2px !important; color: #ffffff !important; }
h1 { font-size: 2.2rem !important; font-weight: 700 !important; text-transform: uppercase !important;
     border-bottom: 2px solid #00d4ff !important; padding-bottom: 12px !important; margin-bottom: 24px !important; }
h2 { font-size: 1.4rem !important; color: #00d4ff !important; font-weight: 600 !important; }
p, li { font-family: 'Inter', sans-serif !important; color: #8899aa !important; font-size: 14px !important; }
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d1f35 0%, #0a1828 100%) !important;
    border: 1px solid rgba(0,212,255,0.13) !important;
    border-radius: 8px !important; padding: 20px !important;
    position: relative !important; overflow: hidden !important;
}
[data-testid="stMetric"]::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 3px; height: 100%; background: #00d4ff;
}
[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace !important; font-size: 10px !important;
    letter-spacing: 2px !important; text-transform: uppercase !important; color: #4477aa !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Rajdhani', sans-serif !important; font-size: 2rem !important;
    font-weight: 700 !important; color: #ffffff !important;
}
.stAlert { background: #0d1f35 !important; border: 1px solid rgba(0,212,255,0.27) !important; border-radius: 6px !important; }
hr { border-color: rgba(0,212,255,0.13) !important; margin: 24px 0 !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #050d1a; }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.27); border-radius: 2px; }
.section-tag {
    font-family: 'Share Tech Mono', monospace; font-size: 10px;
    letter-spacing: 3px; color: #00d4ff; text-transform: uppercase; margin-bottom: 6px;
}
.stat-card {
    background: linear-gradient(135deg, #0d1f35, #0a1525);
    border: 1px solid rgba(0,212,255,0.13);
    border-radius: 8px; padding: 20px 24px; margin: 8px 0; position: relative;
}
.stat-card-label {
    font-family: 'Share Tech Mono', monospace; font-size: 10px;
    letter-spacing: 2px; text-transform: uppercase; color: #446688; margin-bottom: 6px;
}
.page-header {
    background: rgba(13,31,53,0.6); border-left: 3px solid #00d4ff;
    padding: 16px 20px; margin-bottom: 28px; border-radius: 0 6px 6px 0;
}
.page-header p { color: #6688aa !important; font-size: 13px !important; margin: 0 !important; }
.regime-badge {
    display: inline-block; padding: 10px 24px; border-radius: 4px;
    font-family: 'Rajdhani', sans-serif; font-size: 20px; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase; margin: 12px 0;
}
.regime-bull       { background: rgba(0,255,136,0.13); border: 1px solid #00ff88; color: #00ff88; }
.regime-transition { background: rgba(255,170,0,0.13);  border: 1px solid #ffaa00; color: #ffaa00; }
.regime-crisis     { background: rgba(255,51,68,0.13);  border: 1px solid #ff3344; color: #ff3344; }
.stTextInput > div > div {
    background: #080f1e !important; border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 6px !important; color: #c8d8e8 !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stTextInput label {
    font-family: 'Share Tech Mono', monospace !important; font-size: 10px !important;
    letter-spacing: 2px !important; color: #446688 !important; text-transform: uppercase !important;
}
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #00d4ff, #0088ff) !important;
    color: #050d1a !important; font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important; font-weight: 700 !important; letter-spacing: 3px !important;
    text-transform: uppercase !important; border: none !important;
    border-radius: 6px !important; padding: 12px !important; margin-top: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if 'signed_in' not in st.session_state:
    st.session_state.signed_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''

USERS = {
    "admin":     "market123",
    "vaishnavi": "regime2024",
    "team":      "lstm@2024",
}

# ── SIGN-IN PAGE ──
# if not st.session_state.signed_in:
#     st.markdown("""
#     <div style='text-align:center; margin-top:40px;'>
#         <div style='font-family:Share Tech Mono,monospace; font-size:10px;
#                     letter-spacing:4px; color:#00d4ff; margin-bottom:6px;'>
#         </div>
#         <div style='font-family:Rajdhani,sans-serif; font-size:52px;
#                     font-weight:700; color:#ffffff; letter-spacing:4px; line-height:1.1; margin-bottom:4px;'>
#             Market<span style='color:#00d4ff;'>Pulse</span>
#         </div>
#         <div style='font-family:Rajdhani,sans-serif; font-size:18px;
#                     color:#446688; letter-spacing:6px; margin-bottom:48px;'>
#             REGIME INTELLIGENCE SYSTEM
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 1.2, 1])
#     with col2:
#         st.markdown("""
#         <div style='background:linear-gradient(135deg,#0d1f35,#0a1525);
#                     border:1px solid rgba(0,212,255,0.2); border-radius:12px;
#                     padding:40px 36px 24px 36px;
#                     box-shadow:0 24px 80px rgba(0,0,0,0.6);'>
#             <div style='font-family:Share Tech Mono,monospace; font-size:10px;
#                         letter-spacing:3px; color:#446688; text-align:center;
#                         margin-bottom:24px;'>SECURE ACCESS</div>
#         </div>
#         """, unsafe_allow_html=True)

#         username = st.text_input("Username", placeholder="Enter username")
#         password = st.text_input("Password", type="password", placeholder="Enter password")

#         if st.button("SIGN IN  →"):
#             if username in USERS and USERS[username] == password:
#                 st.session_state.signed_in = True
#                 st.session_state.username  = username
#                 st.rerun()
#             else:
#                 st.error("Invalid credentials. Try again.")

#         st.markdown("""
#         <div style='font-family:Share Tech Mono,monospace; font-size:10px;
#                     color:#223344; text-align:center; margin-top:20px; letter-spacing:1px;'>
#             demo → <span style='color:#00d4ff'>admin</span> /
#             <span style='color:#00d4ff'>market123</span>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown("<br><br>", unsafe_allow_html=True)
#     c1, c2, c3, c4 = st.columns(4)
#     for col, val, lbl in [
#         (c1,"7,887","Trading Windows"),
#         (c2,"3","Regimes Detected"),
#         (c3,"16","Latent Dimensions"),
#         (c4,"30yr","Data Coverage")
#     ]:
#         col.markdown(f"""
#         <div class="stat-card" style='text-align:center; padding:20px 8px;'>
#             <div style='font-family:Rajdhani,sans-serif; font-size:32px;
#                          font-weight:700; color:#00d4ff;'>{val}</div>
#             <div class="stat-card-label" style='margin-top:4px;'>{lbl}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     st.stop()

# Handle Google OAuth callback
query_params = st.query_params
if "code" in query_params:
    code = query_params["code"]
    user_info = get_google_user_info(code)
    email   = user_info.get("email")
    name    = user_info.get("name")
    picture = user_info.get("picture")
    if email:
        existing = db["users"].find_one({"email": email})
        if not existing:
            db["users"].insert_one({
                "username": name,
                "email":    email,
                "password": None,
                "role":     "user",
                "verified": True,
                "picture":  picture
            })
        st.session_state.signed_in = True
        st.session_state.username  = name
        st.rerun()

# Handle email verification from link
if "verify" in query_params:
    token = query_params["verify"]
    user = db["users"].find_one({"token": token})
    if user:
        db["users"].update_one(
            {"token": token},
            {"$set": {"verified": True}, "$unset": {"token": ""}}
        )
        st.success("✅ Email verified! You can now sign in.")
        st.query_params.clear()
    else:
        if "code" not in query_params:
            st.error("Invalid or expired verification link.")

if not st.session_state.signed_in:
    

    # ── Hero header ──
    st.markdown("""
    <div style='text-align:center; margin-top:40px;'>
        <div style='font-family:Share Tech Mono,monospace; font-size:10px;
                    letter-spacing:4px; color:#00d4ff; margin-bottom:6px;'>
            // LSTM AUTOENCODER + GMM CLUSTERING
        </div>
        <div style='font-family:Rajdhani,sans-serif; font-size:52px;
                    font-weight:700; color:#ffffff; letter-spacing:4px;
                    line-height:1.1; margin-bottom:4px;'>
            Market<span style='color:#00d4ff;'>Pulse</span>
        </div>
        <div style='font-family:Rajdhani,sans-serif; font-size:18px;
                    color:#446688; letter-spacing:6px; margin-bottom:48px;'>
            REGIME INTELLIGENCE SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tab selector ──
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:

        # Toggle between Sign In and Sign Up
        if 'auth_mode' not in st.session_state:
            st.session_state.auth_mode = 'signin'

        tab1, tab2 = st.tabs(["🔐  Sign In", "📝  Create Account"])

        # ────────────────────────────────
        # SIGN IN TAB
        # ────────────────────────────────
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username",
                                     placeholder="Enter your username",
                                     key="signin_user")
            password = st.text_input("Password",
                                     type="password",
                                     placeholder="Enter your password",
                                     key="signin_pass")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("SIGN IN  →", key="btn_signin"):
                if username and password:
                    user_doc = db["users"].find_one({"username": username})
                    if user_doc and bcrypt.checkpw(
                        password.encode("utf-8"),
                        user_doc["password"]
                    ):
                        st.session_state.signed_in = True
                        st.session_state.username  = username
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.warning("Please enter both username and password.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;font-family:Share Tech Mono,monospace;font-size:10px;color:#446688;letter-spacing:2px;'>── OR ──</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            google_auth_url = get_google_auth_url()
            google_btn = f"<a href='{google_auth_url}' target='_self' style='display:block;text-align:center;padding:12px;background:#ffffff;color:#050d1a;border-radius:6px;font-family:Rajdhani,sans-serif;font-weight:700;font-size:15px;letter-spacing:2px;text-decoration:none;'>🔵 SIGN IN WITH GOOGLE</a>"
            st.markdown(google_btn, unsafe_allow_html=True)
# ────────────────────────────────
        # SIGN UP TAB
        # ────────────────────────────────
    with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            new_username = st.text_input("Choose a username",
                                          placeholder="e.g. john_trader",
                                          key="signup_user")
            new_email = st.text_input("Your Gmail address",
                                       placeholder="e.g. john@gmail.com",
                                       key="signup_email")
            new_password = st.text_input("Choose a password",
                                          type="password",
                                          placeholder="Min 6 characters",
                                          key="signup_pass")
            confirm_pass = st.text_input("Confirm password",
                                          type="password",
                                          placeholder="Re-enter password",
                                          key="signup_confirm")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("CREATE ACCOUNT  →", key="btn_signup"):
                if not new_username or not new_password or not confirm_pass:
                    st.error("Please fill in all fields.")
                elif len(new_username) < 3:
                    st.error("Username must be at least 3 characters.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif new_password != confirm_pass:
                    st.error("Passwords do not match.")
                elif db["users"].find_one({"username": new_username}):
                    st.error(f"Username '{new_username}' is already taken.")
                else:
                    token = secrets.token_urlsafe(32)
                    hashed = bcrypt.hashpw(
                        new_password.encode("utf-8"),
                        bcrypt.gensalt()
                    )
                    db["users"].insert_one({
                        "username": new_username,
                        "email":    new_email,
                        "password": hashed,
                        "role":     "user",
                        "verified": False,
                        "token":    token
                    })
                    if send_verification_email(new_email, new_username, token):
                        st.success("Account created! Check your email to verify.")
                    else:
                        st.error("Account created but email failed. Contact admin.")
    # ── Stats row ──
                st.markdown("<br><br>", unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                for col, val, lbl in [
        (c1, "7,887", "Trading Windows"),
        (c2, "3",     "Regimes Detected"),
        (c3, "16",    "Latent Dimensions"),
        (c4, "30yr",  "Data Coverage")
    ]:
                     col.markdown(f"""
        <div class="stat-card" style='text-align:center; padding:20px 8px;'>
            <div style='font-family:Rajdhani,sans-serif; font-size:32px;
                         font-weight:700; color:#00d4ff;'>{val}</div>
            <div class="stat-card-label" style='margin-top:4px;'>{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

                st.stop()


# ── MODEL ──
class LSTMAutoencoder(nn.Module):
    def __init__(self, n_features, latent_dim=16):
        super().__init__()
        self.encoder = nn.LSTM(input_size=n_features, hidden_size=latent_dim, batch_first=True)
        self.decoder = nn.LSTM(input_size=latent_dim, hidden_size=n_features, batch_first=True)

    def forward(self, x):
        _, (hidden, _) = self.encoder(x)
        latent = hidden.repeat(x.shape[1], 1, 1).permute(1, 0, 2)
        out, _ = self.decoder(latent)
        return out

# ── DATA ──
@st.cache_data
def load_historical_data():
    regimes  = pd.read_csv('regime_labels.csv',  index_col=0, parse_dates=True)
    features = pd.read_csv('features_20d.csv',   index_col=0, parse_dates=True)
    return features.join(regimes['kmeans_regime'], how='inner').dropna()

@st.cache_data
def load_live_data():
    sp500 = yf.download("^GSPC", period="6mo", progress=False, auto_adjust=True)
    vix   = yf.download("^VIX",  period="6mo", progress=False, auto_adjust=True)
    if isinstance(sp500.columns, pd.MultiIndex): sp500.columns = sp500.columns.get_level_values(0)
    if isinstance(vix.columns,   pd.MultiIndex): vix.columns   = vix.columns.get_level_values(0)
    return sp500[['Close']].dropna(), vix[['Close']].dropna()

def compute_features_live(sp500, vix, W=20):
    data = pd.DataFrame(index=sp500.index)
    data['sp500_return'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
    data['vix_close']    = vix['Close'].reindex(sp500.index).ffill()
    data = data.dropna()
    data['rolling_mean']   = data['sp500_return'].rolling(W).mean()
    data['realized_vol']   = data['sp500_return'].rolling(W).std() * np.sqrt(252)
    data['skewness']       = data['sp500_return'].rolling(W).apply(skew,     raw=True)
    data['kurtosis']       = data['sp500_return'].rolling(W).apply(kurtosis, raw=True)
    data['vix_level']      = data['vix_close'].rolling(W).mean()
    data['vix_change']     = data['vix_close'].pct_change(W)
    data['vix_spread']     = data['vix_close']/100 - data['realized_vol']
    data['corr_sp500_vix'] = data['sp500_return'].rolling(W).corr(data['vix_close'])
    cols = ['rolling_mean','realized_vol','skewness','kurtosis',
            'vix_level','vix_change','vix_spread','corr_sp500_vix']
    return data[cols].dropna()

def detect_regime_live(features_df):
    from sklearn.cluster import KMeans
    hist_emb  = pd.read_csv('lstm_embeddings.csv', index_col=0, parse_dates=True)
    kmeans    = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(hist_emb.values.astype(np.float32))
    hist_feat = pd.read_csv('features_20d.csv', index_col=0, parse_dates=True)
    scaler    = StandardScaler()
    scaler.fit(hist_feat.values.astype(np.float32))
    live_scaled = scaler.transform(features_df.values.astype(np.float32))
    if len(live_scaled) < 30: return None, None
    seq   = live_scaled[-30:][np.newaxis, :, :]
    model = LSTMAutoencoder(n_features=8, latent_dim=16)
    model.eval()
    with torch.no_grad():
        x = torch.tensor(seq, dtype=torch.float32)
        _, (h, _) = model.encoder(x)
        emb = h.squeeze().numpy().astype(np.float32)
    regime    = kmeans.predict(emb.reshape(1,-1))[0]
    distances = kmeans.transform(emb.reshape(1,-1))[0]
    return int(regime), float(1 - distances[regime]/distances.sum())

def add_crisis_lines(fig, lc='rgba(255,255,255,0.17)', ac='rgba(255,255,255,0.5)'):
    for date, label in [('2000-03-01','Dot-com 2000'),
                         ('2008-09-15','GFC 2008'),
                         ('2020-03-01','COVID 2020')]:
        fig.add_vline(x=pd.Timestamp(date).timestamp()*1000,
                      line_dash="dash", line_color=lc,
                      annotation_text=label,
                      annotation_font_color=ac,
                      annotation_font_size=10)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown(f"""
    <div style='font-family:Rajdhani,sans-serif;font-size:22px;font-weight:700;
                letter-spacing:3px;color:#ffffff;text-transform:uppercase;'>MarketPulse</div>
    <div style='font-family:Share Tech Mono,monospace;font-size:10px;
                color:#00d4ff;letter-spacing:2px;margin-bottom:12px;'>// REGIME INTELLIGENCE</div>
    <div style='font-family:Share Tech Mono,monospace;font-size:10px;
                color:rgba(0,212,255,0.5);letter-spacing:1px;margin-bottom:16px;'>
        USER: <span style='color:#00d4ff'>{st.session_state.username.upper()}</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("", ["🏠  Live Dashboard","📊  Historical Analysis",
                          "💼  Portfolio Advisor","🧠  About the Model"])
    st.markdown("---")
    st.markdown("""
    <div style='font-family:Share Tech Mono,monospace;font-size:10px;
                color:#446688;letter-spacing:1px;line-height:2.2;'>
        MODEL &nbsp;&nbsp;&nbsp; LSTM Autoencoder<br>
        DATA &nbsp;&nbsp;&nbsp;&nbsp; S&P 500 + VIX<br>
        PERIOD &nbsp;&nbsp; 1993–2024<br>
        REGIMES &nbsp; 3 States<br>
        DIMS &nbsp;&nbsp;&nbsp;&nbsp; 16-dimensional
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Sign Out"):
        st.session_state.signed_in = False
        st.session_state.username  = ''
        st.rerun()

# ── PAGE 1: LIVE DASHBOARD ──
if page == "🏠  Live Dashboard":
    st.markdown('<div class="section-tag">// real-time analysis</div>', unsafe_allow_html=True)
    st.title("Live Market Regime Dashboard")
    st.markdown('<div class="page-header"><p>LSTM Autoencoder analyzes the last 30 days of market behavior and classifies the current regime in real time.</p></div>', unsafe_allow_html=True)

    with st.spinner("Fetching live market data..."):
        sp500, vix = load_live_data()
        features   = compute_features_live(sp500, vix)

  if sp500.empty or vix.empty or features.empty:
        st.error("Unable to fetch live market data. Please try again.")
        st.stop()
    latest_ret = float(np.log(sp500['Close'].iloc[-1]/sp500['Close'].iloc[-2]))
    latest_vix = float(vix['Close'].iloc[-1])
    latest_vol = float(features['realized_vol'].iloc[-1])

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("S&P 500 Return",    f"{latest_ret*100:.2f}%", f"{latest_ret*100:.2f}%")
    c2.metric("VIX Fear Index",    f"{latest_vix:.2f}", f"{latest_vix-float(vix['Close'].iloc[-2]):.2f}")
    c3.metric("Realized Vol (20d)",f"{latest_vol:.4f}")
    c4.metric("Data Points",       f"{len(sp500):,}")

    st.markdown("---")
    st.markdown('<div class="section-tag">// regime classification</div>', unsafe_allow_html=True)
    st.subheader("Current Market Regime")
    regime, confidence = detect_regime_live(features)

    cfg_map = {
        0: ("BULL / CALM MARKET",      "regime-bull",       "#00ff88","▲",
            "Low volatility. Positive drift. Stable growth characteristics.",
            "Maintain or increase equity exposure. Risk-on environment."),
        1: ("TRANSITION / UNCERTAINTY","regime-transition","#ffaa00","◆",
            "Mixed signals. Volatility rising. Market direction unclear.",
            "Reduce risk moderately. Monitor closely."),
        2: ("CRISIS / BEAR MARKET",    "regime-crisis",    "#ff3344","▼",
            "High volatility. Negative skew. Market stress at critical levels.",
            "Reduce equity exposure. Rotate to defensive assets immediately.")
    }

    if regime is not None:
        label, css, color, icon, desc, advice = cfg_map[regime]
        col1, col2 = st.columns([2,1])
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">detected state</div>
                <div class="regime-badge {css}">{icon} &nbsp; {label}</div>
                <p style='color:#8899aa;font-size:13px;margin-top:12px;'>{desc}</p>
                <div style='margin-top:16px;padding:12px 16px;background:#0a1525;
                             border-left:3px solid {color};border-radius:0 4px 4px 0;'>
                    <span style='font-family:Share Tech Mono,monospace;font-size:10px;
                                 color:{color};letter-spacing:2px;'>SIGNAL</span><br>
                    <span style='color:#c8d8e8;font-size:14px;'>{advice}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card" style='text-align:center;padding:32px 20px;'>
                <div class="stat-card-label">model confidence</div>
                <div style='font-family:Rajdhani,sans-serif;font-size:52px;
                             font-weight:700;color:{color};'>
                    {confidence*100:.1f}<span style='font-size:22px;'>%</span>
                </div>
                <div style='margin-top:8px;height:4px;background:#0d1f35;border-radius:2px;overflow:hidden;'>
                    <div style='width:{confidence*100:.1f}%;height:100%;
                                 background:{color};border-radius:2px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Insufficient data. Need at least 30 trading days.")

    st.markdown("---")
    st.markdown('<div class="section-tag">// recent price action</div>', unsafe_allow_html=True)
    st.subheader("S&P 500 — Last 6 Months")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sp500.index, y=sp500['Close'], mode='lines',
                             name='S&P 500', line=dict(color='#00d4ff', width=2),
                             fill='tozeroy', fillcolor='rgba(0,212,255,0.04)'))
    fig.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0),
                      xaxis_title="Date", yaxis_title="Price (USD)", **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ── PAGE 2: HISTORICAL ANALYSIS ──
elif page == "📊  Historical Analysis":
    st.markdown('<div class="section-tag">// 30-year market history</div>', unsafe_allow_html=True)
    st.title("Historical Regime Analysis")
    st.markdown('<div class="page-header"><p>30 years of S&P 500 data classified into 3 structural market regimes using LSTM latent representations and K-Means clustering.</p></div>', unsafe_allow_html=True)

    data = load_historical_data()
    RC   = {0:'#00ff88', 1:'#ffaa00', 2:'#ff3344'}
    RN   = {0:'Bull / Calm', 1:'Transition', 2:'Crisis / Bear'}

    st.markdown('<div class="section-tag">// volatility by regime</div>', unsafe_allow_html=True)
    st.subheader("Realized Volatility — Colored by Regime")
    fig = go.Figure()
    for r in [0,1,2]:
        mask = data['kmeans_regime']==r
        fig.add_trace(go.Scatter(x=data.index[mask], y=data['realized_vol'][mask],
                                 mode='markers', marker=dict(color=RC[r],size=2,opacity=0.7),
                                 name=RN[r]))
    add_crisis_lines(fig)
    fig.update_layout(height=380, xaxis_title="Date", yaxis_title="Realized Volatility", **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-tag">// distribution</div>', unsafe_allow_html=True)
        st.subheader("30-Year Regime Split")
        counts  = data['kmeans_regime'].value_counts().sort_index()
        fig_pie = go.Figure(go.Pie(
            labels=[RN[i] for i in counts.index], values=counts.values,
            marker=dict(colors=['#00ff88','#ffaa00','#ff3344'],
                        line=dict(color='#050d1a',width=2)),
            hole=0.5, textfont=dict(family='Rajdhani',size=13,color='#ffffff')
        ))
        fig_pie.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0), **PLOTLY_THEME)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown('<div class="section-tag">// statistics</div>', unsafe_allow_html=True)
        st.subheader("Key Metrics by Regime")
        stats = data.groupby('kmeans_regime')['realized_vol'].agg(['mean','std','count']).round(4)
        stats.index   = [RN[i] for i in stats.index]
        stats.columns = ['Mean Vol','Std Dev','Days']
        st.dataframe(stats, use_container_width=True)
        for r in [0,1,2]:
            pct = (data['kmeans_regime']==r).sum()/len(data)*100
            st.markdown(f"""
            <div style='display:flex;align-items:center;margin:6px 0;gap:12px;
                         font-family:Share Tech Mono,monospace;font-size:11px;'>
                <span style='color:{RC[r]};width:120px;'>{RN[r]}</span>
                <div style='flex:1;height:4px;background:#0d1f35;border-radius:2px;'>
                    <div style='width:{pct:.1f}%;height:100%;background:{RC[r]};border-radius:2px;'></div>
                </div>
                <span style='color:#446688;width:40px;'>{pct:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-tag">// novel feature</div>', unsafe_allow_html=True)
    st.subheader("VIX Spread — Predictive Regime Signal")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data.index, y=data['vix_spread'], mode='lines',
                              name='VIX Spread', line=dict(color='#ffaa00',width=1.2),
                              fill='tozeroy', fillcolor='rgba(255,170,0,0.04)'))
    fig2.add_hline(y=0, line_dash="dash", line_color='rgba(255,255,255,0.13)')
    add_crisis_lines(fig2, lc='rgba(255,51,68,0.4)', ac='rgba(255,51,68,0.7)')
    fig2.update_layout(height=280, xaxis_title="Date",
                       yaxis_title="Implied − Realized Vol", **PLOTLY_THEME)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("When VIX Spread spikes above zero, a crisis regime typically follows — a leading indicator.")

# ── PAGE 3: PORTFOLIO ADVISOR ──
elif page == "💼  Portfolio Advisor":
    st.markdown('<div class="section-tag">// regime-adaptive allocation</div>', unsafe_allow_html=True)
    st.title("Portfolio Advisor")
    st.markdown('<div class="page-header"><p>Dynamic allocation driven by real-time regime detection. Strategy shifts automatically based on detected market state.</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    portfolio_value = col1.number_input("Portfolio Value (₹ or $)", min_value=1000, value=100000, step=1000)
    risk_profile    = col2.selectbox("Risk Profile", ["Conservative","Moderate","Aggressive"])
    st.markdown("---")

    ALLOC = {
        "Conservative": {0:{"Equity":50,"Bonds":40,"Gold":10}, 1:{"Equity":30,"Bonds":55,"Gold":15}, 2:{"Equity":10,"Bonds":70,"Gold":20}},
        "Moderate":     {0:{"Equity":70,"Bonds":25,"Gold":5},  1:{"Equity":50,"Bonds":40,"Gold":10}, 2:{"Equity":20,"Bonds":60,"Gold":20}},
        "Aggressive":   {0:{"Equity":90,"Bonds":10,"Gold":0},  1:{"Equity":65,"Bonds":30,"Gold":5},  2:{"Equity":30,"Bonds":50,"Gold":20}},
    }

    with st.spinner("Running regime detection..."):
        sp500, vix = load_live_data()
        features   = compute_features_live(sp500, vix)
        regime, confidence = detect_regime_live(features)

    RN = {0:"BULL / CALM", 1:"TRANSITION", 2:"CRISIS / BEAR"}
    RC = {0:"#00ff88", 1:"#ffaa00", 2:"#ff3344"}

    if regime is not None:
        clr = RC[regime]
        st.markdown(f"""
        <div class="stat-card">
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div>
                    <div class="stat-card-label">current regime</div>
                    <div style='font-family:Rajdhani,sans-serif;font-size:26px;
                                 font-weight:700;color:{clr};letter-spacing:3px;'>{RN[regime]}</div>
                </div>
                <div style='text-align:right;'>
                    <div class="stat-card-label">confidence</div>
                    <div style='font-family:Rajdhani,sans-serif;font-size:34px;
                                 font-weight:700;color:{clr};'>{confidence*100:.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        alloc = ALLOC[risk_profile][regime]
        c1,c2,c3 = st.columns(3)
        icons = {"Equity":"📈","Bonds":"📉","Gold":"🥇"}
        for col, (asset, pct) in zip([c1,c2,c3], alloc.items()):
            col.metric(f"{icons[asset]}  {asset}", f"{pct}%", f"₹{portfolio_value*pct//100:,}")
        ACLR = {"Equity":"#00d4ff","Bonds":"#00ff88","Gold":"#ffaa00"}
        fig  = go.Figure(go.Pie(
            labels=list(alloc.keys()), values=list(alloc.values()),
            marker=dict(colors=[ACLR[k] for k in alloc], line=dict(color='#050d1a',width=3)),
            hole=0.6, textfont=dict(family='Rajdhani',size=14,color='#ffffff')
        ))
        fig.update_layout(
            title=dict(text=f"{risk_profile} · {RN[regime]}",
                       font=dict(family='Rajdhani',size=15,color='#8899aa'),x=0.5),
            height=360, margin=dict(l=0,r=0,t=40,b=0), **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:10px;color:#223344;text-align:center;letter-spacing:1px;">⚠ FOR EDUCATIONAL PURPOSES ONLY — NOT FINANCIAL ADVICE</div>', unsafe_allow_html=True)

# ── PAGE 4: ABOUT ──
elif page == "🧠  About the Model":
    st.markdown('<div class="section-tag">// system architecture</div>', unsafe_allow_html=True)
    st.title("About the Model")
    st.markdown('<div class="page-header"><p>Unsupervised deep learning pipeline for automatic market regime detection. No labels. No price prediction. Pure structural discovery.</p></div>', unsafe_allow_html=True)

    for col, val, lbl in zip(st.columns(6),
        ["7,887","8","16","3","30yr","<0.001"],
        ["Training Windows","Input Features","Latent Dims","Regimes","Coverage","ANOVA p-value"]):
        col.markdown(f"""
        <div class="stat-card" style='text-align:center;padding:16px 8px;'>
            <div style='font-family:Rajdhani,sans-serif;font-size:24px;font-weight:700;color:#00d4ff;'>{val}</div>
            <div class="stat-card-label" style='margin-top:4px;'>{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-tag">// pipeline</div>', unsafe_allow_html=True)
        st.subheader("How It Works")
        for num, title, desc in [
            ("01","Data Collection",    "Daily S&P 500 + VIX 1993–2024 via yfinance"),
            ("02","Feature Engineering","8 rolling features incl. novel VIX Spread"),
            ("03","Normalization",      "StandardScaler for stable LSTM training"),
            ("04","Sliding Windows",    "30-day windows → shape (7887, 30, 8)"),
            ("05","LSTM Encoder",       "Compresses each window to 16-dim latent vector"),
            ("06","Clustering",         "K-Means + GMM on embedding matrix"),
            ("07","Validation",         "ANOVA p<0.001 · Portfolio backtest"),
        ]:
            st.markdown(f"""
            <div style='display:flex;gap:16px;margin:10px 0;align-items:flex-start;'>
                <div style='font-family:Share Tech Mono,monospace;font-size:12px;color:#00d4ff;min-width:28px;padding-top:2px;'>{num}</div>
                <div>
                    <div style='font-family:Rajdhani,sans-serif;font-size:15px;font-weight:600;color:#c8d8e8;letter-spacing:1px;'>{title}</div>
                    <div style='font-family:Inter,sans-serif;font-size:12px;color:#556677;margin-top:2px;'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-tag">// novelty</div>', unsafe_allow_html=True)
        st.subheader("Research Contributions")
        for color, title, desc in [
            ("#00ff88","VIX Spread Feature",     "Implied minus realized vol — spikes before crashes. Predictive not reactive."),
            ("#00d4ff","LSTM Autoencoder",        "Temporal compression of 30-day windows into 16-dim latent space."),
            ("#ffaa00","SP500-VIX Corr Flip",     "Changes sign during crises. Structural breakdown signal."),
            ("#ff3344","Three-way Validation",    "UMAP visual + ANOVA (p<0.001) + portfolio economic validation."),
        ]:
            st.markdown(f"""
            <div class="stat-card" style='margin:10px 0;border-left:3px solid {color};padding:14px 16px;'>
                <div style='font-family:Rajdhani,sans-serif;font-size:15px;font-weight:600;color:{color};letter-spacing:1px;'>{title}</div>
                <div style='font-family:Inter,sans-serif;font-size:12px;color:#556677;margin-top:6px;line-height:1.6;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='display:flex;gap:16px;flex-wrap:wrap;'>
        <a href='#' style='font-family:Share Tech Mono,monospace;font-size:11px;color:#00d4ff;
                            letter-spacing:2px;text-decoration:none;padding:8px 16px;
                            border:1px solid rgba(0,212,255,0.27);border-radius:4px;'>↗ GITHUB REPO</a>
        <a href='#' style='font-family:Share Tech Mono,monospace;font-size:11px;color:#00d4ff;
                            letter-spacing:2px;text-decoration:none;padding:8px 16px;
                            border:1px solid rgba(0,212,255,0.27);border-radius:4px;'>↗ ARXIV PAPER</a>
    </div>
    """, unsafe_allow_html=True)
