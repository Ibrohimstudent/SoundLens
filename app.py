import io

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core import HOP, MODEL_PATH, SR, load_audio, load_model, predict
from labels import CATS, META
from style import CSS, bars_html, chips_html, hero_html, result_html, timeline_html, warn_html

st.set_page_config(page_title="SoundLens — Tovushni taniydigan AI", page_icon="🎧", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner="Model yuklanmoqda...")
def get_model():
    return load_model()


@st.cache_data(show_spinner=False)
def analyze(data: bytes):
    sig = load_audio(io.BytesIO(data))
    probs, mels = predict(get_model(), sig)
    return probs, mels, len(sig) / SR, float(np.sqrt(np.mean(sig ** 2)))


# ───────────── Sidebar ─────────────
with st.sidebar:
    st.markdown("## ⚙️ Sozlamalar")
    top_k = st.slider("Ko'rsatiladigan natijalar soni", 3, 10, 5)
    st.markdown("---")
    st.markdown(
        "**Model:** EfficientNet-B0 (transfer learning)\n\n"
        "**Dataset:** ESC-50 · 50 klass\n\n"
        "**Kirish:** 5 soniyalik Mel-spektrogram"
    )
    with st.expander("🎼 Model taniy oladigan tovushlar"):
        st.markdown(chips_html(), unsafe_allow_html=True)
    st.caption("Model tovush *turini* aniqlaydi (it, yomg'ir, kulgi...), shaxs ovozini emas.")

# ───────────── Hero ─────────────
st.markdown(hero_html(), unsafe_allow_html=True)

if not MODEL_PATH.exists():
    st.error(f"Model fayli topilmadi: `{MODEL_PATH}`. Colab'dan `fine-tuning.pt` ni yuklab olib, `models/` papkasiga qo'ying.")
    st.stop()

# ───────────── Kirish ─────────────
tab_up, tab_mic = st.tabs(["📁  Fayl yuklash", "🎙️  Mikrofon"])
data = None
with tab_up:
    up = st.file_uploader("Audio faylni shu yerga tashlang", type=["wav", "mp3", "ogg", "flac", "m4a"],
                          label_visibility="collapsed")
    if up:
        data = up.getvalue()
with tab_mic:
    if hasattr(st, "audio_input"):
        mic = st.audio_input("Yozishni boshlang", label_visibility="collapsed")
        if mic and data is None:
            data = mic.getvalue()
    else:
        st.info("Mikrofon uchun Streamlit'ni yangilang: `pip install -U streamlit`")

# ───────────── Natija ─────────────
if data:
    try:
        probs, mels, dur, rms = analyze(data)
    except Exception as e:
        st.error(f"Audioni o'qib bo'lmadi: {e}\n\nMP3/M4A uchun kompyuterda ffmpeg o'rnatilgan bo'lishi kerak, yoki WAV yuklang.")
        st.stop()

    mean = probs.mean(0)
    order = np.argsort(mean)[::-1]
    top1, conf = CATS[order[0]], float(mean[order[0]])

    st.audio(data)
    st.markdown(result_html(top1, conf), unsafe_allow_html=True)

    if rms < 1e-3:
        st.markdown(warn_html("🔇 Audio deyarli jim — natija ishonchsiz bo'lishi mumkin."), unsafe_allow_html=True)
    elif conf < 0.35:
        st.markdown(warn_html("🤔 Model ikkilanyapti. Quyidagi boshqa variantlarni ham ko'ring."), unsafe_allow_html=True)
    if dur > 5 * len(probs) + 0.5:
        st.caption(f"Audio {dur:.0f} s, birinchi {len(probs) * 5} s tahlil qilindi.")

    left, right = st.columns([1, 1.25], gap="large")
    with left:
        st.markdown('<div class="glass"><h3>🏆 Eng ehtimolli tovushlar</h3>'
                    + bars_html([(CATS[i], float(mean[i])) for i in order[:top_k]]) + "</div>",
                    unsafe_allow_html=True)
    with right:
        st.markdown('<div class="glass"><h3>🌈 Ovozning "rasmi" (Mel-spektrogram)</h3>', unsafe_allow_html=True)
        z = np.concatenate(list(mels), axis=1)
        fig = go.Figure(go.Heatmap(z=z, x=np.arange(z.shape[1]) * HOP / SR, colorscale="Magma", showscale=False))
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#cfcaff"), xaxis_title="soniya", yaxis_title="chastota (mel)")
        st.plotly_chart(fig, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    if len(probs) > 1:
        segs = []
        for i, p in enumerate(probs):
            j = int(p.argmax())
            segs.append((i * 5, i * 5 + 5, CATS[j], float(p[j])))
        st.markdown('<div class="glass"><h3>⏱️ Vaqt bo\'yicha tahlil (har 5 soniya)</h3>'
                    + timeline_html(segs) + "</div>", unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="glass" style="text-align:center;color:#b9b4e6">'
        "👆 Audio yuklang yoki mikrofonda yozing — natija shu yerda paydo bo'ladi.</div>",
        unsafe_allow_html=True,
    )
