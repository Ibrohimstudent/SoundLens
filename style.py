from labels import CATS, META

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Syne:wght@700;800&display=swap');
:root{--v:#7c5cff;--c:#00e5ff;--p:#ff3d9a;--g:#b6ff3c;}
#MainMenu, footer, header[data-testid="stHeader"]{visibility:hidden;height:0;}
html, body, .stApp, [class*="css"]{font-family:'Space Grotesk',sans-serif;}
.stApp{background:#07060f;}
.stApp::before{
  content:"";position:fixed;inset:-20%;z-index:0;pointer-events:none;filter:blur(30px);
  background:
    radial-gradient(40% 40% at 20% 20%, rgba(124,92,255,.38), transparent 60%),
    radial-gradient(35% 35% at 80% 30%, rgba(0,229,255,.24), transparent 60%),
    radial-gradient(40% 40% at 60% 85%, rgba(255,61,154,.26), transparent 60%);
  animation:drift 18s ease-in-out infinite alternate;}
@keyframes drift{to{transform:translate3d(-4%,3%,0) scale(1.12) rotate(5deg);}}
.block-container{position:relative;z-index:1;padding-top:1.5rem;max-width:1120px;}

/* HERO */
.hero{text-align:center;padding:2.2rem 0 1.2rem;}
.kicker{display:inline-block;padding:.35rem .9rem;border-radius:99px;font-size:.78rem;letter-spacing:.25em;
  color:var(--c);border:1px solid rgba(0,229,255,.4);background:rgba(0,229,255,.07);}
.hero h1{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(3rem,9vw,6.2rem);line-height:1;
  margin:.9rem 0 .4rem;color:#fff;letter-spacing:-.03em;}
.hero h1 span{background:linear-gradient(90deg,var(--c),var(--v),var(--p),var(--c));background-size:300% 100%;
  -webkit-background-clip:text;background-clip:text;color:transparent;animation:flow 6s linear infinite;}
@keyframes flow{to{background-position:300% 0;}}
.hero p{color:#b9b4e6;font-size:1.15rem;max-width:640px;margin:0 auto;}
.eq{display:flex;gap:6px;justify-content:center;align-items:flex-end;height:64px;margin-top:1.6rem;}
.eq span{width:7px;border-radius:8px;background:linear-gradient(var(--c),var(--v),var(--p));
  box-shadow:0 0 14px rgba(124,92,255,.7);animation:eq 1.1s ease-in-out infinite;animation-delay:var(--d);height:8px;}
@keyframes eq{0%,100%{height:8px;}50%{height:var(--h);}}

/* GLASS */
.glass{background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.11);backdrop-filter:blur(16px);
  border-radius:24px;padding:1.3rem 1.5rem;margin-bottom:1rem;box-shadow:0 10px 40px rgba(0,0,0,.35);}
.glass h3{margin:0 0 .8rem;font-family:'Syne',sans-serif;color:#fff;font-size:1.15rem;letter-spacing:.02em;}

/* UPLOADER / TABS / BUTTONS */
[data-testid="stFileUploaderDropzone"]{border:2px dashed rgba(0,229,255,.55);background:rgba(0,229,255,.05);
  border-radius:22px;padding:2rem;transition:.25s;}
[data-testid="stFileUploaderDropzone"]:hover{background:rgba(0,229,255,.11);box-shadow:0 0 35px rgba(0,229,255,.25);}
.stTabs [data-baseweb="tab-list"]{gap:.5rem;background:transparent;}
.stTabs [data-baseweb="tab"]{border-radius:99px;padding:.5rem 1.3rem;background:rgba(255,255,255,.05);color:#d9d5ff;}
.stTabs [aria-selected="true"]{background:linear-gradient(90deg,var(--v),var(--p));color:#fff;}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"]{display:none;}
.stButton>button{border-radius:99px;border:0;color:#fff;font-weight:700;padding:.6rem 1.6rem;
  background:linear-gradient(90deg,var(--v),var(--p));box-shadow:0 8px 30px rgba(124,92,255,.45);}
.stButton>button:hover{transform:translateY(-2px);color:#fff;}
audio{width:100%;filter:hue-rotate(220deg) saturate(1.4);}
section[data-testid="stSidebar"]{background:rgba(10,8,22,.85);backdrop-filter:blur(14px);}

/* RESULT */
.result{display:flex;align-items:center;gap:1.6rem;flex-wrap:wrap;
  background:linear-gradient(135deg,rgba(124,92,255,.28),rgba(255,61,154,.16));
  border:1px solid rgba(255,255,255,.18);border-radius:30px;padding:1.6rem 2rem;margin:1rem 0;
  box-shadow:0 0 60px rgba(124,92,255,.35);animation:pop .7s cubic-bezier(.2,1.2,.3,1) both;}
@keyframes pop{from{opacity:0;transform:scale(.9) translateY(20px);}}
.result .emoji{font-size:5.5rem;line-height:1;animation:float 3s ease-in-out infinite;
  filter:drop-shadow(0 0 25px rgba(255,255,255,.45));}
@keyframes float{50%{transform:translateY(-10px) rotate(-4deg);}}
.result .meta{flex:1;min-width:200px;}
.tag{font-size:.75rem;letter-spacing:.3em;color:var(--g);}
.name{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(2rem,5vw,3.2rem);color:#fff;line-height:1.1;}
.en{color:#b9b4e6;font-size:1rem;margin-top:.2rem;}
.ring{--p:0;width:118px;height:118px;border-radius:50%;display:grid;place-items:center;position:relative;
  background:conic-gradient(var(--c) calc(var(--p)*1%), rgba(255,255,255,.1) 0);}
.ring::after{content:"";position:absolute;inset:10px;border-radius:50%;background:#0d0b1f;}
.ring span{position:relative;z-index:1;font-family:'Syne',sans-serif;font-weight:800;font-size:1.6rem;color:#fff;}
.warn{padding:.8rem 1.1rem;border-radius:16px;margin:.4rem 0 1rem;background:rgba(255,184,0,.1);
  border:1px solid rgba(255,184,0,.4);color:#ffd77a;}

/* BARS */
.bar{margin:.75rem 0;}
.bar .lab{display:flex;justify-content:space-between;color:#e8e5ff;margin-bottom:.3rem;font-size:.98rem;}
.bar .lab b{color:var(--c);}
.track{height:12px;border-radius:99px;background:rgba(255,255,255,.08);overflow:hidden;}
.track i{display:block;height:100%;border-radius:99px;transform-origin:left;
  background:linear-gradient(90deg,var(--v),var(--c));box-shadow:0 0 14px rgba(0,229,255,.55);
  animation:grow 1.1s cubic-bezier(.2,.8,.2,1) both;}
.bar:first-child .track i{background:linear-gradient(90deg,var(--p),var(--g));}
@keyframes grow{from{transform:scaleX(0);}}

/* TIMELINE */
.tl{display:flex;gap:.7rem;overflow-x:auto;padding-bottom:.5rem;}
.seg{min-width:130px;text-align:center;padding:.8rem .6rem;border-radius:18px;background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.1);}
.seg small{color:#9d97d6;}
.seg div{font-size:2rem;margin:.2rem 0;}
.seg span{font-size:.85rem;color:#e8e5ff;}

/* CHIPS */
.chip{display:inline-block;margin:.2rem;padding:.3rem .7rem;border-radius:99px;font-size:.82rem;color:#e8e5ff;
  background:rgba(124,92,255,.16);border:1px solid rgba(124,92,255,.4);}
</style>
"""


def _flat(s):
    # Markdown HTML'ni "kod bloki" deb o'qimasligi uchun satrlarni birlashtiramiz
    return "".join(line.strip() for line in s.splitlines())


def hero_html():
    bars = "".join(
        f'<span style="--h:{h}px;--d:{d}s"></span>'
        for h, d in zip(
            [30, 52, 22, 60, 38, 58, 26, 48, 62, 34, 54, 24, 46, 58, 30, 50, 22, 42],
            [i * 0.07 for i in range(18)],
        )
    )
    return _flat(f"""
    <div class="hero">
      <div class="kicker">AI · AUDIO · ESC-50</div>
      <h1>Sound<span>Lens</span></h1>
      <p>Tovush yuklang yoki yozib oling — sun'iy intellekt uni 50 xil tovush turidan biri sifatida taniydi.</p>
      <div class="eq">{bars}</div>
    </div>""")


def result_html(cat, conf):
    emoji, uz = META[cat]
    return _flat(f"""
    <div class="result">
      <div class="emoji">{emoji}</div>
      <div class="meta"><div class="tag">ANIQLANDI</div><div class="name">{uz}</div>
        <div class="en">{cat.replace('_', ' ')}</div></div>
      <div class="ring" style="--p:{conf * 100:.0f}"><span>{conf * 100:.0f}%</span></div>
    </div>""")


def bars_html(items):
    out = []
    for cat, p in items:
        emoji, uz = META[cat]
        out.append(
            f'<div class="bar"><div class="lab"><span>{emoji} {uz}</span><b>{p * 100:.1f}%</b></div>'
            f'<div class="track"><i style="width:{max(p * 100, 0.8):.1f}%"></i></div></div>'
        )
    return "".join(out)


def timeline_html(segments):
    out = []
    for t0, t1, cat, p in segments:
        emoji, uz = META[cat]
        out.append(
            f'<div class="seg"><small>{t0}–{t1} s</small><div>{emoji}</div>'
            f'<span>{uz} · {p * 100:.0f}%</span></div>'
        )
    return '<div class="tl">' + "".join(out) + "</div>"


def chips_html():
    return "".join(f'<span class="chip">{META[c][0]} {META[c][1]}</span>' for c in CATS)


def warn_html(text):
    return f'<div class="warn">{text}</div>'
