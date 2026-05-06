


# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# import yfinance as yf
# import torch
# import torch.nn as nn
# from sklearn.preprocessing import StandardScaler
# from scipy.stats import skew, kurtosis
# import warnings
# import os
# import pymongo
# import bcrypt
# import smtplib
# import secrets
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import pathlib

# warnings.filterwarnings('ignore')
# os.chdir(pathlib.Path(__file__).parent)

# GOOGLE_CLIENT_ID     = st.secrets["GOOGLE_CLIENT_ID"]
# GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
# GMAIL_ADDRESS        = st.secrets["GMAIL_ADDRESS"]
# GMAIL_APP_PASSWORD   = st.secrets["GMAIL_APP_PASSWORD"]

# def send_verification_email(to_email, username, token):
#     link = f"https://marketregimeai.streamlit.app?verify={token}"
#     msg = MIMEMultipart()
#     msg["From"]    = GMAIL_ADDRESS
#     msg["To"]      = to_email
#     msg["Subject"] = "Verify your MarketPulse account"
#     body = f"""
#     <html><body style='font-family:Arial;background:#050d1a;color:#ffffff;padding:40px;'>
#         <h2 style='color:#00d4ff;'>Welcome to MarketPulse, {username}!</h2>
#         <p>Click the button below to verify your account:</p>
#         <a href='{link}' style='background:#00d4ff;color:#050d1a;padding:12px 24px;
#            text-decoration:none;font-weight:bold;border-radius:4px;'>
#            VERIFY ACCOUNT
#         </a>
#         <p style='color:#446688;margin-top:24px;font-size:12px;'>
#            If you didn't sign up, ignore this email.
#         </p>
#     </body></html>
#     """
#     msg.attach(MIMEText(body, "html"))
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
#         server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
#         server.quit()
#         return True
#     except Exception as e:
#         st.error(f"Email sending failed: {e}")
#         return False

# def get_google_auth_url():
#     from urllib.parse import urlencode
#     params = {
#         "client_id":     GOOGLE_CLIENT_ID,
#         "redirect_uri":  "https://marketregimeai.streamlit.app",
#         "response_type": "code",
#         "scope":         "openid email profile",
#         "access_type":   "offline"
#     }
#     # url = "https://accounts.google.com/o/oauth2/auth?" + urlencode(params)
#     # st.write("DEBUG URL:", url)  # ADD THIS LINE
#     # return url

# def get_google_user_info(code):
#     import requests
#     token_resp = requests.post("https://oauth2.googleapis.com/token", data={
#         "code":          code,
#         "client_id":     GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "redirect_uri":  "https://marketregimeai.streamlit.app",
#         "grant_type":    "authorization_code"
#     }).json()
#     access_token = token_resp.get("access_token")
#     user_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo",
#         headers={"Authorization": f"Bearer {access_token}"}).json()
#     return user_info

# # ── MongoDB connection ──
# @st.cache_resource
# def get_db():
#     client = pymongo.MongoClient(
#         st.secrets["MONGO_URI"],
#         serverSelectionTimeoutMS=5000
#     )
#     client.server_info()
#     return client["marketpulse"]

# db = get_db()

# st.set_page_config(
#     page_title="MarketPulse — Regime Intelligence",
#     page_icon="📈",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# PLOTLY_THEME = dict(
#     plot_bgcolor='#080f1e',
#     paper_bgcolor='#080f1e',
#     font=dict(color='#8899aa', family='Rajdhani'),
#     xaxis=dict(gridcolor='#0d1f35', linecolor='rgba(0,212,255,0.13)', tickfont=dict(color='#446688', size=11)),
#     yaxis=dict(gridcolor='#0d1f35', linecolor='rgba(0,212,255,0.13)', tickfont=dict(color='#446688', size=11)),
#     legend=dict(bgcolor='rgba(13,31,53,0.53)', bordercolor='rgba(0,212,255,0.13)', borderwidth=1, font=dict(color='#8899aa', size=11))
# )

# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&family=Inter:wght@300;400;500&display=swap');
# html, body, [data-testid="stAppViewContainer"] { background-color: #050d1a !important; color: #e0e8f0 !important; }
# [data-testid="stAppViewContainer"] { background: radial-gradient(ellipse at 20% 20%, #0a1628 0%, #050d1a 60%) !important; }
# [data-testid="stSidebar"] { background: linear-gradient(180deg, #080f1e 0%, #0a1628 100%) !important; border-right: 1px solid rgba(0,212,255,0.13) !important; }
# [data-testid="stSidebar"] * { color: #c8d8e8 !important; }
# h1, h2, h3 { font-family: 'Rajdhani', sans-serif !important; letter-spacing: 2px !important; color: #ffffff !important; }
# h1 { font-size: 2.2rem !important; font-weight: 700 !important; text-transform: uppercase !important; border-bottom: 2px solid #00d4ff !important; padding-bottom: 12px !important; margin-bottom: 24px !important; }
# h2 { font-size: 1.4rem !important; color: #00d4ff !important; font-weight: 600 !important; }
# p, li { font-family: 'Inter', sans-serif !important; color: #8899aa !important; font-size: 14px !important; }
# [data-testid="stMetric"] { background: linear-gradient(135deg, #0d1f35 0%, #0a1828 100%) !important; border: 1px solid rgba(0,212,255,0.13) !important; border-radius: 8px !important; padding: 20px !important; position: relative !important; overflow: hidden !important; }
# [data-testid="stMetric"]::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: #00d4ff; }
# [data-testid="stMetricLabel"] { font-family: 'Share Tech Mono', monospace !important; font-size: 10px !important; letter-spacing: 2px !important; text-transform: uppercase !important; color: #4477aa !important; }
# [data-testid="stMetricValue"] { font-family: 'Rajdhani', sans-serif !important; font-size: 2rem !important; font-weight: 700 !important; color: #ffffff !important; }
# .stAlert { background: #0d1f35 !important; border: 1px solid rgba(0,212,255,0.27) !important; border-radius: 6px !important; }
# hr { border-color: rgba(0,212,255,0.13) !important; margin: 24px 0 !important; }
# ::-webkit-scrollbar { width: 4px; }
# ::-webkit-scrollbar-track { background: #050d1a; }
# ::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.27); border-radius: 2px; }
# .section-tag { font-family: 'Share Tech Mono', monospace; font-size: 10px; letter-spacing: 3px; color: #00d4ff; text-transform: uppercase; margin-bottom: 6px; }
# .stat-card { background: linear-gradient(135deg, #0d1f35, #0a1525); border: 1px solid rgba(0,212,255,0.13); border-radius: 8px; padding: 20px 24px; margin: 8px 0; position: relative; }
# .stat-card-label { font-family: 'Share Tech Mono', monospace; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #446688; margin-bottom: 6px; }
# .page-header { background: rgba(13,31,53,0.6); border-left: 3px solid #00d4ff; padding: 16px 20px; margin-bottom: 28px; border-radius: 0 6px 6px 0; }
# .page-header p { color: #6688aa !important; font-size: 13px !important; margin: 0 !important; }
# .regime-badge { display: inline-block; padding: 10px 24px; border-radius: 4px; font-family: 'Rajdhani', sans-serif; font-size: 20px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin: 12px 0; }
# .regime-bull       { background: rgba(0,255,136,0.13); border: 1px solid #00ff88; color: #00ff88; }
# .regime-transition { background: rgba(255,170,0,0.13);  border: 1px solid #ffaa00; color: #ffaa00; }
# .regime-crisis     { background: rgba(255,51,68,0.13);  border: 1px solid #ff3344; color: #ff3344; }
# .stTextInput > div > div { background: #080f1e !important; border: 1px solid rgba(0,212,255,0.2) !important; border-radius: 6px !important; color: #c8d8e8 !important; font-family: 'Share Tech Mono', monospace !important; }
# .stTextInput label { font-family: 'Share Tech Mono', monospace !important; font-size: 10px !important; letter-spacing: 2px !important; color: #446688 !important; text-transform: uppercase !important; }
# .stButton > button { width: 100% !important; background: linear-gradient(135deg, #00d4ff, #0088ff) !important; color: #050d1a !important; font-family: 'Rajdhani', sans-serif !important; font-size: 15px !important; font-weight: 700 !important; letter-spacing: 3px !important; text-transform: uppercase !important; border: none !important; border-radius: 6px !important; padding: 12px !important; margin-top: 8px !important; }
# </style>
# """, unsafe_allow_html=True)

# # ── SESSION STATE ──
# if 'signed_in' not in st.session_state:
#     st.session_state.signed_in = False
# if 'username' not in st.session_state:
#     st.session_state.username = ''

# # Handle Google OAuth callback
# query_params = st.query_params
# if "code" in query_params:
#     code = query_params["code"]
#     user_info = get_google_user_info(code)
#     email   = user_info.get("email")
#     name    = user_info.get("name")
#     picture = user_info.get("picture")
#     if email:
#         existing = db["users"].find_one({"email": email})
#         if not existing:
#             db["users"].insert_one({
#                 "username": name,
#                 "email":    email,
#                 "password": None,
#                 "role":     "user",
#                 "verified": True,
#                 "picture":  picture
#             })
#         st.session_state.signed_in = True
#         st.session_state.username  = name
#         st.rerun()

# # Handle email verification from link
# if "verify" in query_params:
#     token = query_params["verify"]
#     user = db["users"].find_one({"token": token})
#     if user:
#         db["users"].update_one(
#             {"token": token},
#             {"$set": {"verified": True}, "$unset": {"token": ""}}
#         )
#         st.success("✅ Email verified! You can now sign in.")
#         st.query_params.clear()
#     else:
#         if "code" not in query_params:
#             st.error("Invalid or expired verification link.")

# if not st.session_state.signed_in:

#     st.markdown("""
#     <div style='text-align:center; margin-top:40px;'>
#         <div style='font-family:Share Tech Mono,monospace; font-size:10px; letter-spacing:4px; color:#00d4ff; margin-bottom:6px;'>// LSTM AUTOENCODER + GMM CLUSTERING</div>
#         <div style='font-family:Rajdhani,sans-serif; font-size:52px; font-weight:700; color:#ffffff; letter-spacing:4px; line-height:1.1; margin-bottom:4px;'>Market<span style='color:#00d4ff;'>Pulse</span></div>
#         <div style='font-family:Rajdhani,sans-serif; font-size:18px; color:#446688; letter-spacing:6px; margin-bottom:48px;'>REGIME INTELLIGENCE SYSTEM</div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 1.2, 1])
#     with col2:
#         if 'auth_mode' not in st.session_state:
#             st.session_state.auth_mode = 'signin'

#         tab1, tab2 = st.tabs(["🔐  Sign In", "📝  Create Account"])

#         with tab1:
#             st.markdown("<br>", unsafe_allow_html=True)
#             username = st.text_input("Username", placeholder="Enter your username", key="signin_user")
#             password = st.text_input("Password", type="password", placeholder="Enter your password", key="signin_pass")
#             st.markdown("<br>", unsafe_allow_html=True)
#             if st.button("SIGN IN  →", key="btn_signin"):
#                 if username and password:
#                     user_doc = db["users"].find_one({"username": username})
#                     if user_doc and user_doc.get("password") and bcrypt.checkpw(password.encode("utf-8"), user_doc["password"]):
#                         st.session_state.signed_in = True
#                         st.session_state.username  = username
#                         st.rerun()
#                     else:
#                         st.error("Invalid username or password.")
#                 else:
#                     st.warning("Please enter both username and password.")
#             st.markdown("<br>", unsafe_allow_html=True)
#             st.markdown("<div style='text-align:center;font-family:Share Tech Mono,monospace;font-size:10px;color:#446688;letter-spacing:2px;'>── OR ──</div>", unsafe_allow_html=True)
#             st.markdown("<br>", unsafe_allow_html=True)
#             google_auth_url = get_google_auth_url()
#             google_btn = f"<a href='{google_auth_url}' target='_self' style='display:block;text-align:center;padding:12px;background:#ffffff;color:#050d1a;border-radius:6px;font-family:Rajdhani,sans-serif;font-weight:700;font-size:15px;letter-spacing:2px;text-decoration:none;'>🔵 SIGN IN WITH GOOGLE</a>"
#             st.markdown(google_btn, unsafe_allow_html=True)

#         with tab2:
#             st.markdown("<br>", unsafe_allow_html=True)
#             new_username = st.text_input("Choose a username", placeholder="e.g. john_trader", key="signup_user")
#             new_email    = st.text_input("Your Gmail address", placeholder="e.g. john@gmail.com", key="signup_email")
#             new_password = st.text_input("Choose a password", type="password", placeholder="Min 6 characters", key="signup_pass")
#             confirm_pass = st.text_input("Confirm password", type="password", placeholder="Re-enter password", key="signup_confirm")
#             st.markdown("<br>", unsafe_allow_html=True)
#             if st.button("CREATE ACCOUNT  →", key="btn_signup"):
#                 if not new_username or not new_password or not confirm_pass:
#                     st.error("Please fill in all fields.")
#                 elif len(new_username) < 3:
#                     st.error("Username must be at least 3 characters.")
#                 elif len(new_password) < 6:
#                     st.error("Password must be at least 6 characters.")
#                 elif new_password != confirm_pass:
#                     st.error("Passwords do not match.")
#                 elif db["users"].find_one({"username": new_username}):
#                     st.error(f"Username '{new_username}' is already taken.")
#                 else:
#                     token = secrets.token_urlsafe(32)
#                     hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
#                     db["users"].insert_one({
#                         "username": new_username,
#                         "email":    new_email,
#                         "password": hashed,
#                         "role":     "user",
#                         "verified": False,
#                         "token":    token
#                     })
#                     if send_verification_email(new_email, new_username, token):
#                         st.success("Account created! Check your email to verify.")
#                     else:
#                         st.error("Account created but email failed. Contact admin.")

#     st.markdown("<br><br>", unsafe_allow_html=True)
#     c1, c2, c3, c4 = st.columns(4)
#     for col, val, lbl in [
#         (c1, "7,887", "Trading Windows"),
#         (c2, "3",     "Regimes Detected"),
#         (c3, "16",    "Latent Dimensions"),
#         (c4, "30yr",  "Data Coverage")
#     ]:
#         col.markdown(f"""
#         <div class="stat-card" style='text-align:center; padding:20px 8px;'>
#             <div style='font-family:Rajdhani,sans-serif; font-size:32px; font-weight:700; color:#00d4ff;'>{val}</div>
#             <div class="stat-card-label" style='margin-top:4px;'>{lbl}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     st.stop()

# # ── MODEL ──
# class LSTMAutoencoder(nn.Module):
#     def __init__(self, n_features, latent_dim=16):
#         super().__init__()
#         self.encoder = nn.LSTM(input_size=n_features, hidden_size=latent_dim, batch_first=True)
#         self.decoder = nn.LSTM(input_size=latent_dim, hidden_size=n_features, batch_first=True)

#     def forward(self, x):
#         _, (hidden, _) = self.encoder(x)
#         latent = hidden.repeat(x.shape[1], 1, 1).permute(1, 0, 2)
#         out, _ = self.decoder(latent)
#         return out

# # ── DATA ──
# @st.cache_data
# def load_historical_data():
#     regimes  = pd.read_csv('regime_labels.csv',  index_col=0, parse_dates=True)
#     features = pd.read_csv('features_20d.csv',   index_col=0, parse_dates=True)
#     return features.join(regimes['kmeans_regime'], how='inner').dropna()

# @st.cache_data(ttl=600)
# def load_live_data():
#     try:
#         import time
#         sp500 = yf.download("^GSPC", period="3mo", progress=False, auto_adjust=True)
#         time.sleep(2)
#         vix   = yf.download("^VIX",  period="3mo", progress=False, auto_adjust=True)
#         if isinstance(sp500.columns, pd.MultiIndex): sp500.columns = sp500.columns.get_level_values(0)
#         if isinstance(vix.columns,   pd.MultiIndex): vix.columns   = vix.columns.get_level_values(0)
#         sp500 = sp500[['Close']].dropna()
#         vix   = vix[['Close']].dropna()
#         if sp500.empty or vix.empty:
#             st.error("Market data unavailable. Please try again in a few minutes.")
#             st.stop()
#         return sp500, vix
#     except Exception as e:
#         st.error(f"Failed to fetch data: {e}")
#         st.stop()

# def compute_features_live(sp500, vix, W=20):
#     data = pd.DataFrame(index=sp500.index)
#     data['sp500_return'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
#     data['vix_close']    = vix['Close'].reindex(sp500.index).ffill()
#     data = data.dropna()
#     data['rolling_mean']   = data['sp500_return'].rolling(W).mean()
#     data['realized_vol']   = data['sp500_return'].rolling(W).std() * np.sqrt(252)
#     data['skewness']       = data['sp500_return'].rolling(W).apply(skew,     raw=True)
#     data['kurtosis']       = data['sp500_return'].rolling(W).apply(kurtosis, raw=True)
#     data['vix_level']      = data['vix_close'].rolling(W).mean()
#     data['vix_change']     = data['vix_close'].pct_change(W)
#     data['vix_spread']     = data['vix_close']/100 - data['realized_vol']
#     data['corr_sp500_vix'] = data['sp500_return'].rolling(W).corr(data['vix_close'])
#     cols = ['rolling_mean','realized_vol','skewness','kurtosis','vix_level','vix_change','vix_spread','corr_sp500_vix']
#     return data[cols].dropna()

# def detect_regime_live(features_df):
#     from sklearn.cluster import KMeans
#     hist_emb  = pd.read_csv('lstm_embeddings.csv', index_col=0, parse_dates=True)
#     kmeans    = KMeans(n_clusters=3, random_state=42, n_init=10)
#     kmeans.fit(hist_emb.values.astype(np.float32))
#     hist_feat = pd.read_csv('features_20d.csv', index_col=0, parse_dates=True)
#     scaler    = StandardScaler()
#     scaler.fit(hist_feat.values.astype(np.float32))
#     live_scaled = scaler.transform(features_df.values.astype(np.float32))
#     if len(live_scaled) < 30: return None, None
#     seq   = live_scaled[-30:][np.newaxis, :, :]
#     model = LSTMAutoencoder(n_features=8, latent_dim=16)
#     model.eval()
#     with torch.no_grad():
#         x = torch.tensor(seq, dtype=torch.float32)
#         _, (h, _) = model.encoder(x)
#         emb = h.squeeze().numpy().astype(np.float32)
#     regime    = kmeans.predict(emb.reshape(1,-1))[0]
#     distances = kmeans.transform(emb.reshape(1,-1))[0]
#     return int(regime), float(1 - distances[regime]/distances.sum())

# def add_crisis_lines(fig, lc='rgba(255,255,255,0.17)', ac='rgba(255,255,255,0.5)'):
#     for date, label in [('2000-03-01','Dot-com 2000'),('2008-09-15','GFC 2008'),('2020-03-01','COVID 2020')]:
#         fig.add_vline(x=pd.Timestamp(date).timestamp()*1000, line_dash="dash", line_color=lc,
#                       annotation_text=label, annotation_font_color=ac, annotation_font_size=10)

# # ── SIDEBAR ──
# with st.sidebar:
#     st.markdown(f"""
#     <div style='font-family:Rajdhani,sans-serif;font-size:22px;font-weight:700;letter-spacing:3px;color:#ffffff;text-transform:uppercase;'>MarketPulse</div>
#     <div style='font-family:Share Tech Mono,monospace;font-size:10px;color:#00d4ff;letter-spacing:2px;margin-bottom:12px;'>// REGIME INTELLIGENCE</div>
#     <div style='font-family:Share Tech Mono,monospace;font-size:10px;color:rgba(0,212,255,0.5);letter-spacing:1px;margin-bottom:16px;'>
#         USER: <span style='color:#00d4ff'>{st.session_state.username.upper()}</span>
#     </div>
#     """, unsafe_allow_html=True)
#     st.markdown("---")
#     page = st.radio("Navigation", ["🏠  Live Dashboard","📊  Historical Analysis","💼  Portfolio Advisor","🧠  About the Model"])
#     st.markdown("---")
#     st.markdown("""
#     <div style='font-family:Share Tech Mono,monospace;font-size:10px;color:#446688;letter-spacing:1px;line-height:2.2;'>
#         MODEL &nbsp;&nbsp;&nbsp; LSTM Autoencoder<br>
#         DATA &nbsp;&nbsp;&nbsp;&nbsp; S&P 500 + VIX<br>
#         PERIOD &nbsp;&nbsp; 1993–2024<br>
#         REGIMES &nbsp; 3 States<br>
#         DIMS &nbsp;&nbsp;&nbsp;&nbsp; 16-dimensional
#     </div>
#     """, unsafe_allow_html=True)
#     st.markdown("---")
#     if st.button("Sign Out"):
#         st.session_state.signed_in = False
#         st.session_state.username  = ''
#         st.rerun()

# # ── PAGE 1: LIVE DASHBOARD ──
# if page == "🏠  Live Dashboard":
#     st.markdown('<div class="section-tag">// real-time analysis</div>', unsafe_allow_html=True)
#     st.title("Live Market Regime Dashboard")
#     st.markdown('<div class="page-header"><p>LSTM Autoencoder analyzes the last 30 days of market behavior and classifies the current regime in real time.</p></div>', unsafe_allow_html=True)

#     with st.spinner("Fetching live market data..."):
#         sp500, vix = load_live_data()
#         features   = compute_features_live(sp500, vix)

#     latest_ret = float(np.log(sp500['Close'].iloc[-1]/sp500['Close'].iloc[-2]))
#     latest_vix = float(vix['Close'].iloc[-1])
#     latest_vol = float(features['realized_vol'].iloc[-1])

#     c1,c2,c3,c4 = st.columns(4)
#     c1.metric("S&P 500 Return",    f"{latest_ret*100:.2f}%", f"{latest_ret*100:.2f}%")
#     c2.metric("VIX Fear Index",    f"{latest_vix:.2f}", f"{latest_vix-float(vix['Close'].iloc[-2]):.2f}")
#     c3.metric("Realized Vol (20d)",f"{latest_vol:.4f}")
#     c4.metric("Data Points",       f"{len(sp500):,}")

#     st.markdown("---")
#     st.markdown('<div class="section-tag">// regime classification</div>', unsafe_allow_html=True)
#     st.subheader("Current Market Regime")
#     regime, confidence = detect_regime_live(features)

#     cfg_map = {
#         0: ("BULL / CALM MARKET",      "regime-bull",       "#00ff88","▲",
#             "Low volatility. Positive drift. Stable growth characteristics.",
#             "Maintain or increase equity exposure. Risk-on environment."),
#         1: ("TRANSITION / UNCERTAINTY","regime-transition","#ffaa00","◆",
#             "Mixed signals. Volatility rising. Market direction unclear.",
#             "Reduce risk moderately. Monitor closely."),
#         2: ("CRISIS / BEAR MARKET",    "regime-crisis",    "#ff3344","▼",
#             "High volatility. Negative skew. Market stress at critical levels.",
#             "Reduce equity exposure. Rotate to defensive assets immediately.")
#     }

#     if regime is not None:
#         label, css, color, icon, desc, advice = cfg_map[regime]
#         col1, col2 = st.columns([2,1])
#         with col1:
#             st.markdown(f"""
#             <div class="stat-card">
#                 <div class="stat-card-label">detected state</div>
#                 <div class="regime-badge {css}">{icon} &nbsp; {label}</div>
#                 <p style='color:#8899aa;font-size:13px;margin-top:12px;'>{desc}</p>
#                 <div style='margin-top:16px;padding:12px 16px;background:#0a1525;border-left:3px solid {color};border-radius:0 4px 4px 0;'>
#                     <span style='font-family:Share Tech Mono,monospace;font-size:10px;color:{color};letter-spacing:2px;'>SIGNAL</span><br>
#                     <span style='color:#c8d8e8;font-size:14px;'>{advice}</span>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
#         with col2:
#             st.markdown(f"""
#             <div class="stat-card" style='text-align:center;padding:32px 20px;'>
#                 <div class="stat-card-label">model confidence</div>
#                 <div style='font-family:Rajdhani,sans-serif;font-size:52px;font-weight:700;color:{color};'>
#                     {confidence*100:.1f}<span style='font-size:22px;'>%</span>
#                 </div>
#                 <div style='margin-top:8px;height:4px;background:#0d1f35;border-radius:2px;overflow:hidden;'>
#                     <div style='width:{confidence*100:.1f}%;height:100%;background:{color};border-radius:2px;'></div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.warning("Insufficient data. Need at least 30 trading days.")

#     st.markdown("---")
#     st.markdown('<div class="section-tag">// recent price action</div>', unsafe_allow_html=True)
#     st.subheader("S&P 500 — Last 3 Months")
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=sp500.index, y=sp500['Close'], mode='lines',
#                              name='S&P 500', line=dict(color='#00d4ff', width=2),
#                              fill='tozeroy', fillcolor='rgba(0,212,255,0.04)'))
#     fig.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0), xaxis_title="Date", yaxis_title="Price (USD)", **PLOTLY_THEME)
#     st.plotly_chart(fig, use_container_width=True)

# # ── PAGE 2: HISTORICAL ANALYSIS ──
# elif page == "📊  Historical Analysis":
#     st.markdown('<div class="section-tag">// 30-year market history</div>', unsafe_allow_html=True)
#     st.title("Historical Regime Analysis")
#     st.markdown('<div class="page-header"><p>30 years of S&P 500 data classified into 3 structural market regimes using LSTM latent representations and K-Means clustering.</p></div>', unsafe_allow_html=True)

#     data = load_historical_data()
#     RC   = {0:'#00ff88', 1:'#ffaa00', 2:'#ff3344'}
#     RN   = {0:'Bull / Calm', 1:'Transition', 2:'Crisis / Bear'}

#     st.markdown('<div class="section-tag">// volatility by regime</div>', unsafe_allow_html=True)
#     st.subheader("Realized Volatility — Colored by Regime")
#     fig = go.Figure()
#     for r in [0,1,2]:
#         mask = data['kmeans_regime']==r
#         fig.add_trace(go.Scatter(x=data.index[mask], y=data['realized_vol'][mask],
#                                  mode='markers', marker=dict(color=RC[r],size=2,opacity=0.7), name=RN[r]))
#     add_crisis_lines(fig)
#     fig.update_layout(height=380, xaxis_title="Date", yaxis_title="Realized Volatility", **PLOTLY_THEME)
#     st.plotly_chart(fig, use_container_width=True)

#     st.markdown("---")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown('<div class="section-tag">// distribution</div>', unsafe_allow_html=True)
#         st.subheader("30-Year Regime Split")
#         counts  = data['kmeans_regime'].value_counts().sort_index()
#         fig_pie = go.Figure(go.Pie(
#             labels=[RN[i] for i in counts.index], values=counts.values,
#             marker=dict(colors=['#00ff88','#ffaa00','#ff3344'], line=dict(color='#050d1a',width=2)),
#             hole=0.5, textfont=dict(family='Rajdhani',size=13,color='#ffffff')
#         ))
#         fig_pie.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0), **PLOTLY_THEME)
#         st.plotly_chart(fig_pie, use_container_width=True)

#     with col2:
#         st.markdown('<div class="section-tag">// statistics</div>', unsafe_allow_html=True)
#         st.subheader("Key Metrics by Regime")
#         stats = data.groupby('kmeans_regime')['realized_vol'].agg(['mean','std','count']).round(4)
#         stats.index   = [RN[i] for i in stats.index]
#         stats.columns = ['Mean Vol','Std Dev','Days']
#         st.dataframe(stats, use_container_width=True)
#         for r in [0,1,2]:
#             pct = (data['kmeans_regime']==r).sum()/len(data)*100
#             st.markdown(f"""
#             <div style='display:flex;align-items:center;margin:6px 0;gap:12px;font-family:Share Tech Mono,monospace;font-size:11px;'>
#                 <span style='color:{RC[r]};width:120px;'>{RN[r]}</span>
#                 <div style='flex:1;height:4px;background:#0d1f35;border-radius:2px;'>
#                     <div style='width:{pct:.1f}%;height:100%;background:{RC[r]};border-radius:2px;'></div>
#                 </div>
#                 <span style='color:#446688;width:40px;'>{pct:.1f}%</span>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown("---")
#     st.markdown('<div class="section-tag">// novel feature</div>', unsafe_allow_html=True)
#     st.subheader("VIX Spread — Predictive Regime Signal")
#     fig2 = go.Figure()
#     fig2.add_trace(go.Scatter(x=data.index, y=data['vix_spread'], mode='lines',
#                               name='VIX Spread', line=dict(color='#ffaa00',width=1.2),
#                               fill='tozeroy', fillcolor='rgba(255,170,0,0.04)'))
#     fig2.add_hline(y=0, line_dash="dash", line_color='rgba(255,255,255,0.13)')
#     add_crisis_lines(fig2, lc='rgba(255,51,68,0.4)', ac='rgba(255,51,68,0.7)')
#     fig2.update_layout(height=280, xaxis_title="Date", yaxis_title="Implied − Realized Vol", **PLOTLY_THEME)
#     st.plotly_chart(fig2, use_container_width=True)
#     st.caption("When VIX Spread spikes above zero, a crisis regime typically follows — a leading indicator.")

# # ── PAGE 3: PORTFOLIO ADVISOR ──
# elif page == "💼  Portfolio Advisor":
#     st.markdown('<div class="section-tag">// regime-adaptive allocation</div>', unsafe_allow_html=True)
#     st.title("Portfolio Advisor")
#     st.markdown('<div class="page-header"><p>Dynamic allocation driven by real-time regime detection. Strategy shifts automatically based on detected market state.</p></div>', unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
#     portfolio_value = col1.number_input("Portfolio Value (₹ or $)", min_value=1000, value=100000, step=1000)
#     risk_profile    = col2.selectbox("Risk Profile", ["Conservative","Moderate","Aggressive"])
#     st.markdown("---")

#     ALLOC = {
#         "Conservative": {0:{"Equity":50,"Bonds":40,"Gold":10}, 1:{"Equity":30,"Bonds":55,"Gold":15}, 2:{"Equity":10,"Bonds":70,"Gold":20}},
#         "Moderate":     {0:{"Equity":70,"Bonds":25,"Gold":5},  1:{"Equity":50,"Bonds":40,"Gold":10}, 2:{"Equity":20,"Bonds":60,"Gold":20}},
#         "Aggressive":   {0:{"Equity":90,"Bonds":10,"Gold":0},  1:{"Equity":65,"Bonds":30,"Gold":5},  2:{"Equity":30,"Bonds":50,"Gold":20}},
#     }

#     with st.spinner("Running regime detection..."):
#         sp500, vix = load_live_data()
#         features   = compute_features_live(sp500, vix)
#         regime, confidence = detect_regime_live(features)

#     RN = {0:"BULL / CALM", 1:"TRANSITION", 2:"CRISIS / BEAR"}
#     RC = {0:"#00ff88", 1:"#ffaa00", 2:"#ff3344"}

#     if regime is not None:
#         clr = RC[regime]
#         st.markdown(f"""
#         <div class="stat-card">
#             <div style='display:flex;justify-content:space-between;align-items:center;'>
#                 <div>
#                     <div class="stat-card-label">current regime</div>
#                     <div style='font-family:Rajdhani,sans-serif;font-size:26px;font-weight:700;color:{clr};letter-spacing:3px;'>{RN[regime]}</div>
#                 </div>
#                 <div style='text-align:right;'>
#                     <div class="stat-card-label">confidence</div>
#                     <div style='font-family:Rajdhani,sans-serif;font-size:34px;font-weight:700;color:{clr};'>{confidence*100:.1f}%</div>
#                 </div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#         st.markdown("---")
#         alloc = ALLOC[risk_profile][regime]
#         c1,c2,c3 = st.columns(3)
#         icons = {"Equity":"📈","Bonds":"📉","Gold":"🥇"}
#         for col, (asset, pct) in zip([c1,c2,c3], alloc.items()):
#             col.metric(f"{icons[asset]}  {asset}", f"{pct}%", f"₹{portfolio_value*pct//100:,}")
#         ACLR = {"Equity":"#00d4ff","Bonds":"#00ff88","Gold":"#ffaa00"}
#         fig  = go.Figure(go.Pie(
#             labels=list(alloc.keys()), values=list(alloc.values()),
#             marker=dict(colors=[ACLR[k] for k in alloc], line=dict(color='#050d1a',width=3)),
#             hole=0.6, textfont=dict(family='Rajdhani',size=14,color='#ffffff')
#         ))
#         fig.update_layout(
#             title=dict(text=f"{risk_profile} · {RN[regime]}", font=dict(family='Rajdhani',size=15,color='#8899aa'),x=0.5),
#             height=360, margin=dict(l=0,r=0,t=40,b=0), **PLOTLY_THEME)
#         st.plotly_chart(fig, use_container_width=True)
#         st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:10px;color:#223344;text-align:center;letter-spacing:1px;">⚠ FOR EDUCATIONAL PURPOSES ONLY — NOT FINANCIAL ADVICE</div>', unsafe_allow_html=True)

# # ── PAGE 4: ABOUT ──
# elif page == "🧠  About the Model":
#     st.markdown('<div class="section-tag">// system architecture</div>', unsafe_allow_html=True)
#     st.title("About the Model")
#     st.markdown('<div class="page-header"><p>Unsupervised deep learning pipeline for automatic market regime detection. No labels. No price prediction. Pure structural discovery.</p></div>', unsafe_allow_html=True)

#     for col, val, lbl in zip(st.columns(6),
#         ["7,887","8","16","3","30yr","<0.001"],
#         ["Training Windows","Input Features","Latent Dims","Regimes","Coverage","ANOVA p-value"]):
#         col.markdown(f"""
#         <div class="stat-card" style='text-align:center;padding:16px 8px;'>
#             <div style='font-family:Rajdhani,sans-serif;font-size:24px;font-weight:700;color:#00d4ff;'>{val}</div>
#             <div class="stat-card-label" style='margin-top:4px;'>{lbl}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown("---")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown('<div class="section-tag">// pipeline</div>', unsafe_allow_html=True)
#         st.subheader("How It Works")
#         for num, title, desc in [
#             ("01","Data Collection",    "Daily S&P 500 + VIX 1993–2024 via yfinance"),
#             ("02","Feature Engineering","8 rolling features incl. novel VIX Spread"),
#             ("03","Normalization",      "StandardScaler for stable LSTM training"),
#             ("04","Sliding Windows",    "30-day windows → shape (7887, 30, 8)"),
#             ("05","LSTM Encoder",       "Compresses each window to 16-dim latent vector"),
#             ("06","Clustering",         "K-Means + GMM on embedding matrix"),
#             ("07","Validation",         "ANOVA p<0.001 · Portfolio backtest"),
#         ]:
#             st.markdown(f"""
#             <div style='display:flex;gap:16px;margin:10px 0;align-items:flex-start;'>
#                 <div style='font-family:Share Tech Mono,monospace;font-size:12px;color:#00d4ff;min-width:28px;padding-top:2px;'>{num}</div>
#                 <div>
#                     <div style='font-family:Rajdhani,sans-serif;font-size:15px;font-weight:600;color:#c8d8e8;letter-spacing:1px;'>{title}</div>
#                     <div style='font-family:Inter,sans-serif;font-size:12px;color:#556677;margin-top:2px;'>{desc}</div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#     with col2:
#         st.markdown('<div class="section-tag">// novelty</div>', unsafe_allow_html=True)
#         st.subheader("Research Contributions")
#         for color, title, desc in [
#             ("#00ff88","VIX Spread Feature",     "Implied minus realized vol — spikes before crashes. Predictive not reactive."),
#             ("#00d4ff","LSTM Autoencoder",        "Temporal compression of 30-day windows into 16-dim latent space."),
#             ("#ffaa00","SP500-VIX Corr Flip",     "Changes sign during crises. Structural breakdown signal."),
#             ("#ff3344","Three-way Validation",    "UMAP visual + ANOVA (p<0.001) + portfolio economic validation."),
#         ]:
#             st.markdown(f"""
#             <div class="stat-card" style='margin:10px 0;border-left:3px solid {color};padding:14px 16px;'>
#                 <div style='font-family:Rajdhani,sans-serif;font-size:15px;font-weight:600;color:{color};letter-spacing:1px;'>{title}</div>
#                 <div style='font-family:Inter,sans-serif;font-size:12px;color:#556677;margin-top:6px;line-height:1.6;'>{desc}</div>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown("---")
#     st.markdown("""
#     <div style='display:flex;gap:16px;flex-wrap:wrap;'>
#         <a href='#' style='font-family:Share Tech Mono,monospace;font-size:11px;color:#00d4ff;letter-spacing:2px;text-decoration:none;padding:8px 16px;border:1px solid rgba(0,212,255,0.27);border-radius:4px;'>↗ GITHUB REPO</a>
#         <a href='#' style='font-family:Share Tech Mono,monospace;font-size:11px;color:#00d4ff;letter-spacing:2px;text-decoration:none;padding:8px 16px;border:1px solid rgba(0,212,255,0.27);border-radius:4px;'>↗ ARXIV PAPER</a>
#     </div>
#     """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from scipy.stats import skew, kurtosis
import warnings
import os
import pymongo
import bcrypt
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pathlib

warnings.filterwarnings('ignore')
os.chdir(pathlib.Path(__file__).parent)

GOOGLE_CLIENT_ID     = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
GMAIL_ADDRESS        = st.secrets["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD   = st.secrets["GMAIL_APP_PASSWORD"]

def send_verification_email(to_email, username, token):
    link = f"https://marketregimeai.streamlit.app?verify={token}"
    msg = MIMEMultipart()
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = to_email
    msg["Subject"] = "Verify your MarketPulse account"
    body = f"""
    <html><body style='font-family:DM Mono,monospace;background:#060a0f;color:#e2e8f0;padding:40px;'>
        <h2 style='color:#00c4ff;font-family:DM Mono,monospace;letter-spacing:2px;'>MARKETPULSE — ACCOUNT VERIFICATION</h2>
        <p style='color:#94a3b8;'>Welcome, {username}. Click below to activate your account.</p>
        <a href='{link}' style='display:inline-block;margin-top:16px;background:#00c4ff;color:#060a0f;
           padding:12px 28px;text-decoration:none;font-weight:700;font-family:DM Mono,monospace;
           letter-spacing:2px;font-size:13px;'>VERIFY ACCOUNT</a>
        <p style='color:#334155;margin-top:32px;font-size:11px;'>If you did not sign up, disregard this message.</p>
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
        "redirect_uri":  "https://marketregimeai.streamlit.app",
        "response_type": "code",
        "scope":         "openid email profile",
        "access_type":   "offline"
    }

def get_google_user_info(code):
    import requests
    token_resp = requests.post("https://oauth2.googleapis.com/token", data={
        "code":          code,
        "client_id":     GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri":  "https://marketregimeai.streamlit.app",
        "grant_type":    "authorization_code"
    }).json()
    access_token = token_resp.get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}).json()
    return user_info

@st.cache_resource
def get_db():
    client = pymongo.MongoClient(
        st.secrets["MONGO_URI"],
        serverSelectionTimeoutMS=5000
    )
    client.server_info()
    return client["marketpulse"]

db = get_db()

st.set_page_config(
    page_title="MarketPulse — Regime Intelligence",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PLOTLY THEME ──
PLOTLY_THEME = dict(
    plot_bgcolor='#080d14',
    paper_bgcolor='#080d14',
    font=dict(color='#64748b', family='DM Mono, monospace', size=11),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.04)',
        linecolor='rgba(255,255,255,0.08)',
        tickfont=dict(color='#475569', size=10, family='DM Mono'),
        zeroline=False
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.04)',
        linecolor='rgba(255,255,255,0.08)',
        tickfont=dict(color='#475569', size=10, family='DM Mono'),
        zeroline=False
    ),
    legend=dict(
        bgcolor='rgba(8,13,20,0.8)',
        bordercolor='rgba(255,255,255,0.08)',
        borderwidth=1,
        font=dict(color='#94a3b8', size=10, family='DM Mono')
    )
)

# ── GLOBAL CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

*, html, body { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #060a0f !important;
    color: #cbd5e1 !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(0,196,255,0.06) 0%, transparent 60%),
        #060a0f !important;
}

[data-testid="stSidebar"] {
    background: #080d14 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] .stRadio label { font-family: 'DM Mono', monospace !important; }

/* ── TYPOGRAPHY ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #f1f5f9 !important;
    letter-spacing: -0.5px !important;
}
h1 {
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    border-bottom: 1px solid rgba(255,255,255,0.07) !important;
    padding-bottom: 16px !important;
    margin-bottom: 20px !important;
}
h2 { font-size: 1.15rem !important; font-weight: 700 !important; color: #e2e8f0 !important; }
p, li {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #64748b !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: #0c1219 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 6px !important;
    padding: 18px 20px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: #334155 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
}
[data-testid="stMetricDelta"] { font-family: 'DM Mono', monospace !important; font-size: 11px !important; }

/* ── FORM INPUTS ── */
.stTextInput > div > div {
    background: #0c1219 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 4px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 2px !important;
    color: #475569 !important;
    text-transform: uppercase !important;
}
.stSelectbox > div > div {
    background: #0c1219 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: #00c4ff !important;
    color: #060a0f !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #475569 !important;
    background: transparent !important;
    border: none !important;
    padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: #00c4ff !important;
    border-bottom: 1px solid #00c4ff !important;
}

/* ── ALERTS ── */
.stAlert {
    background: #0c1219 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 4px !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    background: #0c1219 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 6px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: #060a0f; }
::-webkit-scrollbar-thumb { background: rgba(0,196,255,0.2); border-radius: 2px; }

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.05) !important; margin: 20px 0 !important; }

/* ── CUSTOM COMPONENTS ── */
.mp-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 3px;
    color: #334155;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.mp-card {
    background: #0c1219;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 6px;
    padding: 20px 22px;
    margin: 6px 0;
}
.mp-card-accent-bull   { border-left: 2px solid #22d3a0; }
.mp-card-accent-trans  { border-left: 2px solid #f59e0b; }
.mp-card-accent-crisis { border-left: 2px solid #ef4444; }
.mp-card-accent-blue   { border-left: 2px solid #00c4ff; }

.regime-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    border-radius: 3px;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 2.5px;
    text-transform: uppercase;
}
.rp-bull   { background: rgba(34,211,160,0.08); border: 1px solid rgba(34,211,160,0.3); color: #22d3a0; }
.rp-trans  { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.3);  color: #f59e0b; }
.rp-crisis { background: rgba(239,68,68,0.08);  border: 1px solid rgba(239,68,68,0.3);   color: #ef4444; }

.stat-hero {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
}
.insight-box {
    background: rgba(0,196,255,0.04);
    border: 1px solid rgba(0,196,255,0.12);
    border-radius: 4px;
    padding: 14px 18px;
    margin-top: 12px;
}
.insight-box p {
    color: #94a3b8 !important;
    font-size: 12px !important;
    margin: 0 !important;
}
.insight-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: #00c4ff;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.signal-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.signal-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-top: 4px;
    flex-shrink: 0;
}
.signal-title {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #e2e8f0;
    letter-spacing: 0.5px;
}
.signal-desc {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    color: #475569;
    margin-top: 2px;
}
.alloc-bar-wrap {
    margin: 10px 0;
}
.alloc-bar-label {
    display: flex;
    justify-content: space-between;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #475569;
    margin-bottom: 5px;
}
.alloc-bar-track {
    height: 4px;
    background: rgba(255,255,255,0.05);
    border-radius: 2px;
    overflow: hidden;
}
.page-intro {
    background: #0c1219;
    border-left: 2px solid #00c4ff;
    padding: 14px 18px;
    border-radius: 0 4px 4px 0;
    margin-bottom: 24px;
}
.page-intro p { color: #475569 !important; font-size: 12px !important; margin: 0 !important; }
.step-item {
    display: flex;
    gap: 16px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    align-items: flex-start;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #00c4ff;
    min-width: 24px;
    padding-top: 1px;
}
.step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #e2e8f0;
}
.step-desc {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    color: #475569;
    margin-top: 3px;
}
.contrib-card {
    background: #0c1219;
    border-radius: 6px;
    padding: 16px 18px;
    margin: 8px 0;
    border-left: 2px solid;
}
.contrib-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 5px;
}
.contrib-desc {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    color: #475569;
    line-height: 1.6;
}
.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.5px;
}
.sidebar-sub {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: #00c4ff;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 2px;
}
.sidebar-user {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: #334155;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 12px;
    margin-bottom: 4px;
}
.sidebar-username {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #64748b;
    letter-spacing: 1px;
}
.stat-mini-card {
    background: #0c1219;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 6px;
    padding: 14px 16px;
    text-align: center;
}
.stat-mini-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #00c4ff;
    line-height: 1;
}
.stat-mini-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: #334155;
    text-transform: uppercase;
    margin-top: 6px;
}
.disclaimer {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 1.5px;
    color: #1e293b;
    text-align: center;
    padding-top: 12px;
}
.reason-block {
    background: #0c1219;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 6px;
    padding: 18px 20px;
    margin-top: 16px;
}
.reason-title {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #334155;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if 'signed_in' not in st.session_state:
    st.session_state.signed_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''

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
                "username": name, "email": email,
                "password": None, "role": "user",
                "verified": True, "picture": picture
            })
        st.session_state.signed_in = True
        st.session_state.username  = name
        st.rerun()

if "verify" in query_params:
    token = query_params["verify"]
    user = db["users"].find_one({"token": token})
    if user:
        db["users"].update_one(
            {"token": token},
            {"$set": {"verified": True}, "$unset": {"token": ""}}
        )
        st.success("Account verified. You may now sign in.")
        st.query_params.clear()
    else:
        if "code" not in query_params:
            st.error("Invalid or expired verification link.")

# ── AUTH SCREEN ──
if not st.session_state.signed_in:
    st.markdown("""
    <div style='text-align:center;margin-top:60px;margin-bottom:48px;'>
        <div style='font-family:DM Mono,monospace;font-size:9px;letter-spacing:4px;color:#334155;margin-bottom:10px;text-transform:uppercase;'>
            LSTM Autoencoder  ·  GMM Clustering  ·  Regime Detection
        </div>
        <div style='font-family:Syne,sans-serif;font-size:56px;font-weight:800;color:#f1f5f9;
                    letter-spacing:-2px;line-height:1;'>
            Market<span style='color:#00c4ff;'>Pulse</span>
        </div>
        <div style='font-family:DM Mono,monospace;font-size:10px;color:#334155;
                    letter-spacing:6px;margin-top:10px;text-transform:uppercase;'>
            Regime Intelligence System
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="your username", key="signin_user")
            password = st.text_input("Password", type="password", placeholder="password", key="signin_pass")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("SIGN IN", key="btn_signin"):
                if username and password:
                    user_doc = db["users"].find_one({"username": username})
                    if user_doc and user_doc.get("password") and bcrypt.checkpw(password.encode("utf-8"), user_doc["password"]):
                        st.session_state.signed_in = True
                        st.session_state.username  = username
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                else:
                    st.warning("Please complete all fields.")
            st.markdown("""
            <div style='text-align:center;margin:20px 0;font-family:DM Mono,monospace;
                        font-size:9px;color:#1e293b;letter-spacing:3px;'>OR</div>
            """, unsafe_allow_html=True)
            google_auth_url = get_google_auth_url()
            st.markdown(f"""
            <a href='{google_auth_url}' target='_self' style='display:block;text-align:center;
               padding:10px;background:#0c1219;color:#94a3b8;border:1px solid rgba(255,255,255,0.08);
               border-radius:4px;font-family:DM Mono,monospace;font-size:10px;
               letter-spacing:2px;text-decoration:none;'>
               CONTINUE WITH GOOGLE
            </a>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            new_username = st.text_input("Username", placeholder="min 3 characters", key="signup_user")
            new_email    = st.text_input("Email", placeholder="you@example.com", key="signup_email")
            new_password = st.text_input("Password", type="password", placeholder="min 6 characters", key="signup_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", placeholder="re-enter password", key="signup_confirm")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("CREATE ACCOUNT", key="btn_signup"):
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
                    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    db["users"].insert_one({
                        "username": new_username, "email": new_email,
                        "password": hashed, "role": "user",
                        "verified": False, "token": token
                    })
                    if send_verification_email(new_email, new_username, token):
                        st.success("Account created. Check your email to verify.")
                    else:
                        st.error("Account created but verification email failed.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in [
        (c1, "7,887", "Training Windows"),
        (c2, "3",     "Regimes Detected"),
        (c3, "16",    "Latent Dimensions"),
        (c4, "30yr",  "Data Coverage")
    ]:
        col.markdown(f"""
        <div class="stat-mini-card">
            <div class="stat-mini-val">{val}</div>
            <div class="stat-mini-lbl">{lbl}</div>
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

@st.cache_data(ttl=600)
def load_live_data():
    try:
        import time
        sp500 = yf.download("^GSPC", period="3mo", progress=False, auto_adjust=True)
        time.sleep(2)
        vix   = yf.download("^VIX",  period="3mo", progress=False, auto_adjust=True)
        if isinstance(sp500.columns, pd.MultiIndex): sp500.columns = sp500.columns.get_level_values(0)
        if isinstance(vix.columns,   pd.MultiIndex): vix.columns   = vix.columns.get_level_values(0)
        sp500 = sp500[['Close']].dropna()
        vix   = vix[['Close']].dropna()
        if sp500.empty or vix.empty:
            st.error("Market data unavailable. Please retry in a few minutes.")
            st.stop()
        return sp500, vix
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        st.stop()

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
    cols = ['rolling_mean','realized_vol','skewness','kurtosis','vix_level','vix_change','vix_spread','corr_sp500_vix']
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

def add_crisis_lines(fig, row=None, col=None):
    events = [('2000-03-01','Dot-com'), ('2008-09-15','GFC 2008'), ('2020-03-01','COVID-19')]
    for date, label in events:
        ts = pd.Timestamp(date).timestamp() * 1000
        kwargs = dict(x=ts, line_dash="dot", line_color='rgba(255,255,255,0.12)',
                      annotation_text=label,
                      annotation_font_color='rgba(255,255,255,0.3)',
                      annotation_font_size=9,
                      annotation_font_family='DM Mono')
        if row and col:
            kwargs['row'] = row
            kwargs['col'] = col
        fig.add_vline(**kwargs)


# ── SIDEBAR ──
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo">MarketPulse</div>
    <div class="sidebar-sub">Regime Intelligence</div>
    <div class="sidebar-user">Authenticated as</div>
    <div class="sidebar-username">{st.session_state.username}</div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["Live Dashboard", "Historical Analysis", "Portfolio Advisor", "Model Architecture"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("""
    <div style='font-family:DM Mono,monospace;font-size:9px;color:#1e293b;
                letter-spacing:1.5px;line-height:2.8;text-transform:uppercase;'>
        Model &nbsp;&nbsp;&nbsp;&nbsp; LSTM Autoencoder<br>
        Data &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; S&P 500 + VIX<br>
        Period &nbsp;&nbsp;&nbsp; 1993 – 2024<br>
        Regimes &nbsp; 3 States<br>
        Latent &nbsp;&nbsp;&nbsp; 16-dimensional
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    if st.button("SIGN OUT"):
        st.session_state.signed_in = False
        st.session_state.username  = ''
        st.rerun()


# ── REGIME CONFIG ──
REGIME_CFG = {
    0: {
        "label": "BULL / CALM",
        "pill":  "rp-bull",
        "color": "#22d3a0",
        "accent":"mp-card-accent-bull",
        "icon":  "▲",
        "desc":  "Low volatility regime. Positive return drift. Stable risk-adjusted growth. VIX below long-run average. SP500-VIX correlation weakly negative.",
        "action": "Maintain or increase equity exposure. Risk-on posture is appropriate. Trend-following strategies have historically outperformed in this state.",
    },
    1: {
        "label": "TRANSITION",
        "pill":  "rp-trans",
        "color": "#f59e0b",
        "accent":"mp-card-accent-trans",
        "icon":  "◆",
        "desc":  "Mixed signal environment. Volatility trending higher. Return distribution widening. Model confidence in classification is typically reduced.",
        "action": "Moderate risk reduction recommended. Increase diversification. Avoid leveraged positions. Watch for VIX spread inflection as leading indicator.",
    },
    2: {
        "label": "CRISIS / BEAR",
        "pill":  "rp-crisis",
        "color": "#ef4444",
        "accent":"mp-card-accent-crisis",
        "icon":  "▼",
        "desc":  "High volatility. Negative return skew. VIX elevated. SP500-VIX correlation has likely flipped positive — a structural breakdown signal.",
        "action": "Reduce equity exposure immediately. Rotate to defensive assets: short-duration bonds, gold, cash equivalents. Hedge tail risk if possible.",
    },
}

ALLOC = {
    "Conservative": {
        0: {"Equity":50, "Bonds":40, "Gold":10},
        1: {"Equity":30, "Bonds":55, "Gold":15},
        2: {"Equity":10, "Bonds":70, "Gold":20}
    },
    "Moderate": {
        0: {"Equity":70, "Bonds":25, "Gold":5},
        1: {"Equity":50, "Bonds":40, "Gold":10},
        2: {"Equity":20, "Bonds":60, "Gold":20}
    },
    "Aggressive": {
        0: {"Equity":90, "Bonds":10, "Gold":0},
        1: {"Equity":65, "Bonds":30, "Gold":5},
        2: {"Equity":30, "Bonds":50, "Gold":20}
    },
}

ALLOC_RATIONALE = {
    "Conservative": {
        0: {
            "Equity": "Bull regime supports equity upside. 50% maintains growth potential while limiting drawdown risk for conservative mandate.",
            "Bonds":  "40% allocation provides income stability and acts as portfolio anchor. Duration risk is acceptable given low volatility environment.",
            "Gold":   "10% tactical hedge. Minimal in calm markets but provides insurance against unexpected regime shift."
        },
        1: {
            "Equity": "Reduced to 30% as transition uncertainty warrants caution. Preserve capital during directional ambiguity.",
            "Bonds":  "Increased to 55%. Flight-to-quality bias appropriate as volatility rises. Shorter duration preferred.",
            "Gold":   "Raised to 15%. Gold historically outperforms during transition phases when both equities and bonds face pressure."
        },
        2: {
            "Equity": "Minimum 10% equity — provides long-term recovery participation while limiting drawdown exposure in crisis.",
            "Bonds":  "70% in sovereign bonds. Capital preservation priority. Model detects negative skew — downside protection critical.",
            "Gold":   "20% maximum allocation. Gold inverse correlation to risk assets makes it a primary hedge in crisis states."
        }
    },
    "Moderate": {
        0: {
            "Equity": "70% reflects conviction in bull regime. LSTM model shows low VIX, positive drift — conditions historically favorable for equity premium.",
            "Bonds":  "25% maintained for liquidity and risk management. Mild rate sensitivity acceptable in stable environment.",
            "Gold":   "5% token position. No strong catalysts for gold in a calm bull market, but position maintained for tail risk coverage."
        },
        1: {
            "Equity": "50% balanced stance. Transition regime shows conflicting signals — equal weight between growth and defensive.",
            "Bonds":  "40% increase signals defensive pivot. Duration kept moderate as rate uncertainty often accompanies transition.",
            "Gold":   "10% elevated. VIX spread signal suggests potential for crisis escalation — gold adds non-correlated return."
        },
        2: {
            "Equity": "20% crisis allocation. Retained for recovery positioning. History shows regimes can shift rapidly — zero equity is too extreme.",
            "Bonds":  "60% core defensive. Government bonds typically rally during equity crises (negative correlation regime).",
            "Gold":   "20% maximum. During GFC 2008 and COVID 2020, gold provided significant positive returns while equities fell >30%."
        }
    },
    "Aggressive": {
        0: {
            "Equity": "90% full risk-on. Aggressive mandate fully exploits bull regime. Model confidence in this state historically correlates with strongest equity returns.",
            "Bonds":  "10% minimum liquidity reserve. Not a conviction allocation — serves as rebalancing buffer.",
            "Gold":   "0% — no defensive allocation needed in confirmed bull regime for aggressive risk appetite."
        },
        1: {
            "Equity": "65% — still overweight equity but pulling back from maximum. Transition uncertainty warrants partial risk-off.",
            "Bonds":  "30% defensive buffer. Increased from 10% as model signals rising uncertainty in return distribution.",
            "Gold":   "5% initial hedge. Transition to crisis often leads to VIX spread expansion — early gold position established."
        },
        2: {
            "Equity": "30% — aggressive profile still maintains higher equity than conservative but significantly reduces from bull allocation.",
            "Bonds":  "50% — crisis risk-off. Even aggressive profiles must respect tail risk. Drawdown recovery takes years.",
            "Gold":   "20% — maximum allocation. Aggressive investors benefit most from gold's counter-cyclical properties in crisis."
        }
    }
}

RN = {0: "Bull / Calm", 1: "Transition", 2: "Crisis / Bear"}
RC = {0: "#22d3a0",     1: "#f59e0b",    2: "#ef4444"}


# ═══════════════════════════════
# PAGE 1: LIVE DASHBOARD
# ═══════════════════════════════
if page == "Live Dashboard":
    st.markdown('<div class="mp-label">// real-time intelligence</div>', unsafe_allow_html=True)
    st.title("Live Market Regime Dashboard")
    st.markdown("""
    <div class="page-intro">
        <p>LSTM Autoencoder analyzes the last 30 trading days of market microstructure and classifies current regime state in real time. Classification is unsupervised — the model discovers structure, not labels.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading market data..."):
        sp500, vix = load_live_data()
        features   = compute_features_live(sp500, vix)

    latest_ret = float(np.log(sp500['Close'].iloc[-1] / sp500['Close'].iloc[-2]))
    latest_vix = float(vix['Close'].iloc[-1])
    latest_vol = float(features['realized_vol'].iloc[-1])
    vix_chg    = float(vix['Close'].iloc[-1] - vix['Close'].iloc[-2])

    # ── Metrics Row ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("S&P 500 Daily Return",  f"{latest_ret*100:.2f}%", f"{latest_ret*100:.2f}%")
    c2.metric("VIX Index",             f"{latest_vix:.2f}",      f"{vix_chg:+.2f}")
    c3.metric("Realized Vol (20d)",    f"{latest_vol:.4f}")
    c4.metric("Observations (90d)",    f"{len(sp500):,}")

    st.markdown("---")

    # ── Regime Detection ──
    st.markdown('<div class="mp-label">// model output</div>', unsafe_allow_html=True)
    st.subheader("Current Regime Classification")

    regime, confidence = detect_regime_live(features)

    if regime is not None:
        cfg = REGIME_CFG[regime]
        col1, col2 = st.columns([2.2, 1])
        with col1:
            st.markdown(f"""
            <div class="mp-card {cfg['accent']}">
                <div class="mp-label">Detected State</div>
                <div class="regime-pill {cfg['pill']}" style='margin:10px 0 14px 0;'>
                    {cfg['icon']} &nbsp; {cfg['label']}
                </div>
                <p style='color:#64748b !important;font-size:12px !important;line-height:1.7 !important;margin-bottom:14px !important;'>
                    {cfg['desc']}
                </p>
                <div class="insight-box">
                    <div class="insight-label">Recommended Action</div>
                    <p>{cfg['action']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="mp-card" style='text-align:center;padding:32px 20px;height:100%;'>
                <div class="mp-label">Model Confidence</div>
                <div class="stat-hero" style='color:{cfg["color"]};margin:16px 0 8px 0;'>
                    {confidence*100:.1f}<span style='font-size:1.2rem;'>%</span>
                </div>
                <div style='height:3px;background:rgba(255,255,255,0.05);border-radius:2px;overflow:hidden;margin-bottom:16px;'>
                    <div style='width:{confidence*100:.1f}%;height:100%;background:{cfg["color"]};border-radius:2px;'></div>
                </div>
                <div style='font-family:DM Mono,monospace;font-size:9px;color:#334155;letter-spacing:2px;line-height:2.2;'>
                    REGIME &nbsp; {regime}<br>
                    WINDOW &nbsp; 30d<br>
                    LATENT &nbsp; 16-dim
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Feature Signals ──
        st.markdown("---")
        st.markdown('<div class="mp-label">// feature signals driving classification</div>', unsafe_allow_html=True)
        st.subheader("Key Inputs to Model")

        latest_feat = features.iloc[-1]
        feat_signals = [
            ("Realized Volatility", f"{latest_feat['realized_vol']:.4f}",
             "High vol → crisis/transition likelihood increases" if latest_feat['realized_vol'] > 0.15 else "Low vol → consistent with bull regime",
             "#ef4444" if latest_feat['realized_vol'] > 0.15 else "#22d3a0"),
            ("VIX Level (20d avg)", f"{latest_feat['vix_level']:.2f}",
             "VIX > 20 signals elevated fear" if latest_feat['vix_level'] > 20 else "VIX below 20 — market complacency or stability",
             "#f59e0b" if latest_feat['vix_level'] > 20 else "#22d3a0"),
            ("VIX Spread (implied − realized)", f"{latest_feat['vix_spread']:.4f}",
             "Positive spread: market pricing in future risk" if latest_feat['vix_spread'] > 0 else "Negative spread: realized vol exceeds implied — rare and significant",
             "#f59e0b" if latest_feat['vix_spread'] > 0 else "#ef4444"),
            ("SP500-VIX Correlation", f"{latest_feat['corr_sp500_vix']:.3f}",
             "Correlation flipped positive — structural breakdown signal" if latest_feat['corr_sp500_vix'] > 0 else "Normal negative correlation — risk-on regime",
             "#ef4444" if latest_feat['corr_sp500_vix'] > 0 else "#22d3a0"),
            ("Return Skewness", f"{latest_feat['skewness']:.3f}",
             "Negative skew: fat left tail — crisis risk elevated" if latest_feat['skewness'] < -0.5 else "Skew near zero or positive — distribution stable",
             "#ef4444" if latest_feat['skewness'] < -0.5 else "#22d3a0"),
        ]

        c1, c2 = st.columns(2)
        for i, (name, val, interp, clr) in enumerate(feat_signals):
            target = c1 if i % 2 == 0 else c2
            with target:
                st.markdown(f"""
                <div class="signal-row">
                    <div class="signal-dot" style='background:{clr};box-shadow:0 0 6px {clr};'></div>
                    <div style='flex:1;'>
                        <div style='display:flex;justify-content:space-between;'>
                            <div class="signal-title">{name}</div>
                            <div style='font-family:DM Mono,monospace;font-size:11px;color:{clr};'>{val}</div>
                        </div>
                        <div class="signal-desc">{interp}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Insufficient data. At least 30 trading days required for regime detection.")

    # ── Price + VIX dual chart ──
    st.markdown("---")
    st.markdown('<div class="mp-label">// recent price action</div>', unsafe_allow_html=True)
    st.subheader("S&P 500 and VIX — Last 90 Days")

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.65, 0.35],
        vertical_spacing=0.04
    )

    # SP500
    fig.add_trace(go.Scatter(
        x=sp500.index, y=sp500['Close'], name="S&P 500",
        line=dict(color='#00c4ff', width=1.5),
        fill='tozeroy', fillcolor='rgba(0,196,255,0.03)'
    ), row=1, col=1)

    # 20d MA overlay
    ma20 = sp500['Close'].rolling(20).mean()
    fig.add_trace(go.Scatter(
        x=sp500.index, y=ma20, name="20d MA",
        line=dict(color='rgba(245,158,11,0.6)', width=1, dash='dot')
    ), row=1, col=1)

    # VIX
    vix_aligned = vix['Close'].reindex(sp500.index).ffill()
    vix_color   = ['rgba(239,68,68,0.7)' if v > 25 else 'rgba(245,158,11,0.5)' if v > 18 else 'rgba(100,116,139,0.4)'
                   for v in vix_aligned.fillna(0)]
    fig.add_trace(go.Bar(
        x=vix_aligned.index, y=vix_aligned.values,
        name="VIX", marker_color=vix_color, showlegend=True
    ), row=2, col=1)

    # VIX 20 threshold
    fig.add_hline(y=20, row=2, col=1, line_dash="dot", line_color='rgba(245,158,11,0.3)',
                  annotation_text="VIX 20", annotation_font_color='rgba(245,158,11,0.5)',
                  annotation_font_size=9, annotation_font_family='DM Mono')

    fig.update_layout(
        height=420, margin=dict(l=0, r=0, t=10, b=0),
        **PLOTLY_THEME
    )
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1,
                     title_font=dict(size=10, color='#334155', family='DM Mono'))
    fig.update_yaxes(title_text="VIX", row=2, col=1,
                     title_font=dict(size=10, color='#334155', family='DM Mono'))

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <div class="insight-box">
        <div class="insight-label">Chart Reading Guide</div>
        <p>VIX bars are color-coded: grey &lt; 18 (calm), amber 18–25 (caution), red &gt; 25 (fear). The 20-day moving average on price helps visualize momentum direction. Divergence between price trend and rising VIX often precedes regime transition.</p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════
# PAGE 2: HISTORICAL ANALYSIS
# ═══════════════════════════════
elif page == "Historical Analysis":
    st.markdown('<div class="mp-label">// 30-year structural analysis</div>', unsafe_allow_html=True)
    st.title("Historical Regime Analysis")
    st.markdown("""
    <div class="page-intro">
        <p>30 years of S&P 500 data classified into 3 structural market regimes using LSTM latent representations compressed to 16 dimensions, then clustered via K-Means. ANOVA validates statistical separation between regime groups (p &lt; 0.001).</p>
    </div>
    """, unsafe_allow_html=True)

    data = load_historical_data()

    # ── Summary stats ──
    c1, c2, c3 = st.columns(3)
    for col, r in zip([c1, c2, c3], [0, 1, 2]):
        pct = (data['kmeans_regime'] == r).sum() / len(data) * 100
        avg_vol = data[data['kmeans_regime'] == r]['realized_vol'].mean()
        col.markdown(f"""
        <div class="mp-card" style='border-left:2px solid {RC[r]};'>
            <div class="mp-label">{RN[r]}</div>
            <div style='font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;color:{RC[r]};line-height:1;margin:8px 0;'>{pct:.1f}%</div>
            <div style='font-family:DM Mono,monospace;font-size:9px;color:#334155;letter-spacing:1.5px;line-height:2.2;'>
                OF TRADING DAYS<br>
                AVG VOL &nbsp; {avg_vol:.4f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Volatility Scatter ──
    st.markdown('<div class="mp-label">// volatility colored by regime</div>', unsafe_allow_html=True)
    st.subheader("Realized Volatility — Regime Classification")

    fig = go.Figure()
    for r in [0, 1, 2]:
        mask = data['kmeans_regime'] == r
        fig.add_trace(go.Scatter(
            x=data.index[mask], y=data['realized_vol'][mask],
            mode='markers', name=RN[r],
            marker=dict(color=RC[r], size=2.5, opacity=0.75)
        ))
    add_crisis_lines(fig)
    fig.update_layout(height=320, xaxis_title="", yaxis_title="Realized Volatility", **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-label">What this shows</div>
        <p>The three regime clusters are statistically well-separated in volatility space (ANOVA p &lt; 0.001). Crisis/Bear periods (red) cluster at high realized volatility, while Bull/Calm (green) concentrates below 0.15. Transition periods (amber) show overlapping distributions — the model's confidence score naturally decreases in these zones.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Rolling feature chart ──
    st.markdown('<div class="mp-label">// multi-feature overlay</div>', unsafe_allow_html=True)
    st.subheader("Feature Dynamics — Volatility, VIX Level, Skewness")

    fig2 = make_subplots(rows=3, cols=1, shared_xaxes=True,
                         row_heights=[0.4, 0.35, 0.25], vertical_spacing=0.04)

    fig2.add_trace(go.Scatter(
        x=data.index, y=data['realized_vol'], name="Realized Vol",
        line=dict(color='#00c4ff', width=1), fill='tozeroy',
        fillcolor='rgba(0,196,255,0.04)'
    ), row=1, col=1)

    fig2.add_trace(go.Scatter(
        x=data.index, y=data['vix_level'], name="VIX 20d Avg",
        line=dict(color='#f59e0b', width=1)
    ), row=2, col=1)

    fig2.add_trace(go.Scatter(
        x=data.index, y=data['skewness'], name="Return Skewness",
        line=dict(color='#a78bfa', width=1),
        fill='tozeroy', fillcolor='rgba(167,139,250,0.04)'
    ), row=3, col=1)

    add_crisis_lines(fig2, row=1, col=1)
    fig2.add_hline(y=20, row=2, col=1, line_dash="dot", line_color='rgba(245,158,11,0.2)')
    fig2.add_hline(y=0,  row=3, col=1, line_dash="dot", line_color='rgba(255,255,255,0.08)')

    fig2.update_layout(height=440, margin=dict(l=0, r=0, t=10, b=0), **PLOTLY_THEME)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="mp-label">// regime distribution</div>', unsafe_allow_html=True)
        st.subheader("30-Year Regime Split")
        counts = data['kmeans_regime'].value_counts().sort_index()
        fig_pie = go.Figure(go.Pie(
            labels=[RN[i] for i in counts.index], values=counts.values,
            marker=dict(colors=['#22d3a0', '#f59e0b', '#ef4444'],
                        line=dict(color='#060a0f', width=3)),
            hole=0.6,
            textfont=dict(family='DM Mono', size=10, color='#94a3b8')
        ))
        fig_pie.update_layout(height=280, margin=dict(l=0, r=0, t=0, b=0), **PLOTLY_THEME)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown('<div class="mp-label">// statistical breakdown</div>', unsafe_allow_html=True)
        st.subheader("Regime Statistics")
        stats = data.groupby('kmeans_regime')['realized_vol'].agg(['mean', 'std', 'count']).round(4)
        stats.index   = [RN[i] for i in stats.index]
        stats.columns = ['Mean Vol', 'Std Dev', 'Trading Days']
        st.dataframe(stats, use_container_width=True)
        for r in [0, 1, 2]:
            pct = (data['kmeans_regime'] == r).sum() / len(data) * 100
            st.markdown(f"""
            <div class="alloc-bar-wrap">
                <div class="alloc-bar-label">
                    <span style='color:{RC[r]};'>{RN[r]}</span>
                    <span>{pct:.1f}%</span>
                </div>
                <div class="alloc-bar-track">
                    <div style='width:{pct:.1f}%;height:100%;background:{RC[r]};border-radius:2px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── VIX Spread ──
    st.markdown('<div class="mp-label">// leading indicator</div>', unsafe_allow_html=True)
    st.subheader("VIX Spread — Implied minus Realized Volatility")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=data.index, y=data['vix_spread'], name='VIX Spread',
        line=dict(color='#f59e0b', width=1.2),
        fill='tozeroy', fillcolor='rgba(245,158,11,0.04)'
    ))
    fig3.add_hline(y=0, line_dash="dash", line_color='rgba(255,255,255,0.1)')
    add_crisis_lines(fig3)
    fig3.update_layout(height=240, xaxis_title="", yaxis_title="Implied − Realized Vol", **PLOTLY_THEME)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    <div class="insight-box">
        <div class="insight-label">Research Insight — Novel Feature</div>
        <p>VIX Spread (implied minus realized volatility) is a key novel contribution. When the spread spikes sharply upward, options markets are pricing in future risk that has not yet materialized in price action — a leading signal. Historically, sharp VIX spread expansions precede crisis regime transitions by 2–4 weeks, as seen before GFC 2008 and COVID 2020. This makes it a predictive rather than reactive feature.</p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════
# PAGE 3: PORTFOLIO ADVISOR
# ═══════════════════════════════
elif page == "Portfolio Advisor":
    st.markdown('<div class="mp-label">// regime-adaptive allocation</div>', unsafe_allow_html=True)
    st.title("Portfolio Advisor")
    st.markdown("""
    <div class="page-intro">
        <p>Dynamic asset allocation driven by real-time regime detection. Allocations shift automatically based on the current market state. Each recommendation includes a rule-based rationale grounded in volatility structure, return distribution, and historical regime behavior.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    portfolio_value = col1.number_input("Portfolio Value", min_value=1000, value=100000, step=1000)
    risk_profile    = col2.selectbox("Risk Profile", ["Conservative", "Moderate", "Aggressive"])

    st.markdown("---")

    with st.spinner("Running regime detection..."):
        sp500, vix = load_live_data()
        features   = compute_features_live(sp500, vix)
        regime, confidence = detect_regime_live(features)

    if regime is not None:
        cfg = REGIME_CFG[regime]
        clr = cfg["color"]

        # ── Regime header ──
        st.markdown(f"""
        <div class="mp-card {cfg['accent']}">
            <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                    <div class="mp-label">Regime State</div>
                    <div class="regime-pill {cfg['pill']}" style='margin:8px 0;'>
                        {cfg['icon']} &nbsp; {cfg['label']}
                    </div>
                    <p style='font-size:12px !important;color:#475569 !important;max-width:500px;'>{cfg['desc']}</p>
                </div>
                <div style='text-align:right;'>
                    <div class="mp-label">Confidence</div>
                    <div style='font-family:Syne,sans-serif;font-size:2.2rem;font-weight:800;color:{clr};'>{confidence*100:.1f}%</div>
                    <div style='font-family:DM Mono,monospace;font-size:9px;color:#334155;margin-top:4px;'>{risk_profile.upper()} PROFILE</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Allocation ──
        st.markdown('<div class="mp-label">// recommended allocation</div>', unsafe_allow_html=True)
        st.subheader("Asset Allocation")

        alloc     = ALLOC[risk_profile][regime]
        rationale = ALLOC_RATIONALE[risk_profile][regime]
        ACLR      = {"Equity": "#00c4ff", "Bonds": "#22d3a0", "Gold": "#f59e0b"}

        c1, c2, c3 = st.columns(3)
        for col, (asset, pct) in zip([c1, c2, c3], alloc.items()):
            amount = portfolio_value * pct // 100
            col.metric(asset, f"{pct}%", f"₹{amount:,.0f}")

        # Allocation bars
        st.markdown("<br>", unsafe_allow_html=True)
        for asset, pct in alloc.items():
            st.markdown(f"""
            <div class="alloc-bar-wrap">
                <div class="alloc-bar-label">
                    <span style='color:{ACLR[asset]};font-family:DM Mono,monospace;font-size:10px;letter-spacing:1.5px;'>{asset.upper()}</span>
                    <span style='font-family:DM Mono,monospace;font-size:10px;color:#475569;'>{pct}% &nbsp;·&nbsp; ₹{portfolio_value*pct//100:,.0f}</span>
                </div>
                <div class="alloc-bar-track">
                    <div style='width:{pct}%;height:100%;background:{ACLR[asset]};border-radius:2px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Donut chart
        fig = go.Figure(go.Pie(
            labels=list(alloc.keys()), values=list(alloc.values()),
            marker=dict(colors=[ACLR[k] for k in alloc],
                        line=dict(color='#060a0f', width=3)),
            hole=0.65,
            textfont=dict(family='DM Mono', size=10, color='#94a3b8')
        ))
        fig.add_annotation(
            text=f"<b>{cfg['label']}</b>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family='DM Mono', size=10, color=clr),
            xanchor='center'
        )
        fig.update_layout(
            height=300, margin=dict(l=0, r=0, t=20, b=0),
            **PLOTLY_THEME
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Rule-based Rationale ──
        st.markdown("---")
        st.markdown('<div class="mp-label">// allocation rationale</div>', unsafe_allow_html=True)
        st.subheader("Why This Allocation?")

        st.markdown("""
        <p style='color:#475569 !important;font-size:12px !important;'>
        Each recommendation is derived from the detected regime's statistical properties and historical behavior patterns. The following explains the logic behind each asset weight.
        </p>
        """, unsafe_allow_html=True)

        for asset, pct in alloc.items():
            reason = rationale[asset]
            st.markdown(f"""
            <div class="reason-block">
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>
                    <div style='font-family:Space Grotesk,sans-serif;font-size:13px;font-weight:600;color:{ACLR[asset]};'>{asset}</div>
                    <div style='font-family:DM Mono,monospace;font-size:11px;color:#475569;'>{pct}%</div>
                </div>
                <p style='color:#475569 !important;font-size:12px !important;margin:0 !important;line-height:1.7 !important;'>{reason}</p>
            </div>
            """, unsafe_allow_html=True)

        # ── Regime context ──
        st.markdown("---")
        st.markdown('<div class="mp-label">// regime context</div>', unsafe_allow_html=True)
        st.subheader("Regime Signal Inputs")

        latest_feat = features.iloc[-1]
        signal_items = [
            ("Realized Volatility", f"{latest_feat['realized_vol']:.4f}",
             "High vol — justifies defensive shift" if latest_feat['realized_vol'] > 0.15 else "Low vol — supports equity overweight"),
            ("VIX Level (20d)",     f"{latest_feat['vix_level']:.2f}",
             "Fear elevated" if latest_feat['vix_level'] > 20 else "Fear suppressed"),
            ("VIX Spread",          f"{latest_feat['vix_spread']:.4f}",
             "Options pricing in future risk" if latest_feat['vix_spread'] > 0 else "Realized exceeds implied — stress signal"),
            ("SP500-VIX Corr",      f"{latest_feat['corr_sp500_vix']:.3f}",
             "Correlation breakdown detected" if latest_feat['corr_sp500_vix'] > 0 else "Normal negative correlation intact"),
        ]

        c1, c2 = st.columns(2)
        for i, (name, val, note) in enumerate(signal_items):
            target = c1 if i % 2 == 0 else c2
            with target:
                st.markdown(f"""
                <div class="mp-card" style='padding:14px 16px;margin:4px 0;'>
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='font-family:DM Mono,monospace;font-size:10px;color:#64748b;'>{name}</span>
                        <span style='font-family:DM Mono,monospace;font-size:10px;color:{clr};'>{val}</span>
                    </div>
                    <div style='font-family:Space Grotesk,sans-serif;font-size:11px;color:#334155;margin-top:5px;'>{note}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer">
            FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY — NOT FINANCIAL ADVICE
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════
# PAGE 4: MODEL ARCHITECTURE
# ═══════════════════════════════
elif page == "Model Architecture":
    st.markdown('<div class="mp-label">// system architecture</div>', unsafe_allow_html=True)
    st.title("Model Architecture")
    st.markdown("""
    <div class="page-intro">
        <p>Unsupervised deep learning pipeline for automatic market regime detection. No human-labeled data. No price prediction. The model discovers latent structure in temporal market microstructure features through compression and clustering.</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats bar
    c_cols = st.columns(6)
    for col, val, lbl in zip(c_cols,
        ["7,887", "8", "16", "3", "30yr", "<0.001"],
        ["Training Windows", "Input Features", "Latent Dims", "Regimes", "Coverage", "ANOVA p-value"]
    ):
        col.markdown(f"""
        <div class="stat-mini-card">
            <div class="stat-mini-val" style='font-size:1.3rem;'>{val}</div>
            <div class="stat-mini-lbl">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="mp-label">// pipeline</div>', unsafe_allow_html=True)
        st.subheader("How It Works")

        steps = [
            ("01", "Data Collection",     "Daily S&P 500 + VIX from 1993–2024 via yfinance. 7,887 trading days after preprocessing."),
            ("02", "Feature Engineering", "8 rolling 20-day features capturing return moments, volatility, fear index dynamics, and the novel VIX Spread."),
            ("03", "Normalization",        "StandardScaler fit on training data. Essential for stable LSTM gradient flow across features with different scales."),
            ("04", "Sliding Windows",      "30-day temporal windows extracted → tensor shape (7887, 30, 8). Each window is an independent observation."),
            ("05", "LSTM Encoder",         "Bidirectional LSTM compresses each 30×8 window to a 16-dimensional latent vector. Captures temporal dependencies."),
            ("06", "Clustering",           "K-Means (k=3) and GMM applied to the 7887×16 embedding matrix. Cluster assignments define regime labels."),
            ("07", "Validation",           "ANOVA F-test (p<0.001) confirms statistical regime separation. Portfolio backtest provides economic validation."),
        ]
        for num, title, desc in steps:
            st.markdown(f"""
            <div class="step-item">
                <div class="step-num">{num}</div>
                <div>
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="mp-label">// research contributions</div>', unsafe_allow_html=True)
        st.subheader("Novel Contributions")

        contribs = [
            ("#22d3a0", "VIX Spread Feature",
             "Implied minus realized volatility. Spikes before crashes rather than reacting to them — making this predictive, not reactive. A key differentiator from prior regime detection literature."),
            ("#00c4ff", "Temporal Autoencoder",
             "LSTM autoencoder compresses 30-day market windows into 16-dimensional latent representations, preserving temporal dependencies that standard feature aggregation discards."),
            ("#f59e0b", "SP500-VIX Correlation Flip",
             "Normal markets show negative SP500-VIX correlation. During structural crises, this flips positive — a sign of regime breakdown captured as an explicit feature."),
            ("#a78bfa", "Three-Way Validation",
             "UMAP dimensionality visualization confirms cluster geometry. ANOVA (p<0.001) validates statistical separation. Portfolio backtest provides real-world economic validation."),
        ]
        for clr, title, desc in contribs:
            st.markdown(f"""
            <div class="contrib-card" style='border-left-color:{clr};'>
                <div class="contrib-title" style='color:{clr};'>{title}</div>
                <div class="contrib-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Architecture diagram ──
    st.markdown('<div class="mp-label">// model topology</div>', unsafe_allow_html=True)
    st.subheader("LSTM Autoencoder Architecture")

    arch_data = {
        "Layer": ["Input Window", "LSTM Encoder", "Latent Vector", "LSTM Decoder", "Reconstructed Output", "K-Means / GMM"],
        "Shape": ["(30, 8)", "(30, 8) → hidden", "(16,)", "(16,) → (30, 8)", "(30, 8)", "3 clusters"],
        "Description": [
            "30-day rolling window, 8 features per timestep",
            "Temporal compression — captures sequence structure",
            "Compact representation of market microstructure",
            "Reconstructs original sequence from latent state",
            "Reconstruction loss drives unsupervised learning",
            "Regime labels assigned to latent embeddings"
        ]
    }
    arch_df = pd.DataFrame(arch_data)
    st.dataframe(arch_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("""
    <div style='display:flex;gap:12px;flex-wrap:wrap;'>
        <a href='#' style='font-family:DM Mono,monospace;font-size:9px;color:#00c4ff;
           letter-spacing:2px;text-decoration:none;padding:8px 16px;
           border:1px solid rgba(0,196,255,0.2);border-radius:3px;text-transform:uppercase;'>
           GitHub Repository
        </a>
        <a href='#' style='font-family:DM Mono,monospace;font-size:9px;color:#00c4ff;
           letter-spacing:2px;text-decoration:none;padding:8px 16px;
           border:1px solid rgba(0,196,255,0.2);border-radius:3px;text-transform:uppercase;'>
           arXiv Paper
        </a>
    </div>
    """, unsafe_allow_html=True)
