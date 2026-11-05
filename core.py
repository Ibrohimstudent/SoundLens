from pathlib import Path

import librosa
import numpy as np
import timm
import torch

SR = 22050
WIN = SR * 5            # 5 soniyalik oyna (ESC-50 formati)
HOP = 512
MAX_WINDOWS = 12        # uzun audioda maksimum 60 soniya tahlil qilinadi
MODEL_PATH = Path(__file__).parent / "models" / "fine-tuning.pt"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_model():
    m = timm.create_model(
        "efficientnet_b0", pretrained=False, num_classes=50,
        drop_rate=0.3, drop_path_rate=0.2,
    )
    state = torch.load(MODEL_PATH, map_location="cpu")
    m.load_state_dict(state)
    return m.to(DEVICE).eval()


def load_audio(src):
    sig, _ = librosa.load(src, sr=SR, mono=True)
    return sig


def mel(sig):
    # Notebookdagi funksiya bilan bir xil
    m = librosa.feature.melspectrogram(
        y=sig, sr=SR, n_fft=1024, hop_length=HOP, n_mels=128)
    db = librosa.power_to_db(m, ref=np.max)
    return (db + 40) / 20


def split_windows(sig):
    if len(sig) < WIN:
        sig = np.pad(sig, (0, WIN - len(sig)))
    wins = []
    for i in range(min(int(np.ceil(len(sig) / WIN)), MAX_WINDOWS)):
        w = sig[i * WIN:(i + 1) * WIN]
        if len(w) < WIN:
            if i > 0 and len(w) < WIN * 0.3:   # juda qisqa dumni tashlab yuboramiz
                break
            w = np.pad(w, (0, WIN - len(w)))
        wins.append(w)
    return wins


@torch.no_grad()
def predict(model, sig):
    """Qaytaradi: probs (W, 50), mels (W, 128, 216)"""
    mels = np.stack([mel(w) for w in split_windows(sig)]).astype("float32")
    x = torch.from_numpy(mels)[:, None].repeat(1, 3, 1, 1).to(DEVICE)
    probs = model(x).softmax(1).cpu().numpy()
    return probs, mels
