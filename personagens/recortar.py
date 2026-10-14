"""Recorta os personagens de personagens/*.jpg, troca o fundo creme por transparência,
esfuma as bordas do recorte e grava WebP em assets/.
Uso: python personagens.py <pasta do site> [pasta de saída]
Coordenadas dos recortes em escala 2000 px de largura (como as imagens foram inspecionadas)."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

site = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(site, "assets")

# nome de saída: (arquivo, recorte x0,y0,x1,y1 em escala 2000, largura final em px)
CROPS = {
    "p-botao":     ("01.jpg", (150, 100, 1165, 1200), 760),   # hero esquerda: jogador aperta o botão
    "p-celular":   ("05.jpg", (1010, 120, 1900, 1410), 620),  # hero direita: vê o replay no celular
    "p-problema":  ("02.jpg", (365, 290, 950, 1290), 560),    # problema: perdido com o celular
    "p-skate":     ("03.jpg", (150, 120, 1900, 1390), 1000),  # como funciona: pista de skate
    "p-quadra":    ("01.jpg", (150, 90, 1900, 1380), 1000),   # como funciona (carrossel): beach tennis, cena inteira
    "p-dono":      ("06.jpg", (270, 190, 1000, 1410), 520),   # para a arena: dono apontando
    "p-luta":      ("04.jpg", (120, 150, 1900, 1380), 900),   # como funciona (carrossel): artes marciais
    "p-entrega":   ("05.jpg", (110, 110, 1900, 1410), 900),   # entrega: cena inteira do jogador com o replay no celular
    "p-banco":     ("07.jpg", (110, 160, 1900, 1400), 900),   # indique: quem ficou no banco
    "p-atende":    ("08.jpg", (300, 110, 1070, 1390), 560),   # dúvidas: "pode falar"
    "p-festa":     ("09.jpg", (0, 40, 2000, 1090), 1500),    # final: todo mundo comemorando
}
# pedaços de outros elementos que sobram dentro do recorte (mesma escala 2000) e são apagados
ERASE = {"p-dono": [(930, 270, 1010, 390), (868, 648, 1010, 880)]}
FEATHER = 0.07   # fração de cada borda que some aos poucos
LOW, HIGH = 0.05, 0.16  # abaixo de LOW vira fundo; entre os dois, transição suave (limpa ruído do JPEG)


def to_alpha(rgb, bg):
    """Cor-para-alfa: quanto cada pixel se afasta do fundo vira opacidade; a cor é recalculada sem o fundo."""
    px = rgb.astype(np.float32)
    darker = np.where(px < bg, (bg - px) / bg, 0.0)
    a = np.clip(darker.max(axis=2), 0, 1)  # só o que é mais escuro que o fundo conta: o fundo é quase branco e o "mais claro" é só ruído
    safe = np.maximum(a, 1e-3)[..., None]
    color = np.clip((px - bg) / safe + bg, 0, 255)
    a = np.where(a < HIGH, np.clip((a - LOW) / (HIGH - LOW), 0, 1) * HIGH, a)
    return color, a


def edge_fade(h, w, feather=FEATHER):
    def ramp(n):
        k = max(2, int(n * feather))
        r = np.ones(n, np.float32)
        t = np.linspace(0, 1, k)
        s = t * t * (3 - 2 * t)
        r[:k], r[-k:] = s, s[::-1]
        return r
    return ramp(h)[:, None] * ramp(w)[None, :]


for name, (src, box, width) in CROPS.items():
    im = Image.open(os.path.join(site, "personagens", src)).convert("RGB")
    k = im.width / 2000
    im = im.crop(tuple(int(v * k) for v in box))
    full = np.asarray(Image.open(os.path.join(site, "personagens", src)).convert("RGB"), np.float32)
    m = 40  # o fundo é a mediana dos quatro cantos da imagem inteira
    corners = np.concatenate([full[:m, :m].reshape(-1, 3), full[:m, -m:].reshape(-1, 3), full[-m:, :m].reshape(-1, 3), full[-m:, -m:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    crop = np.asarray(im, np.float32)
    near = crop[np.abs(crop - bg).max(axis=2) < 22]  # fundo dentro do próprio recorte (o tom varia um pouco pela imagem)
    if len(near) > 1000:
        bg = np.median(near, axis=0)
    color, a = to_alpha(np.asarray(im), bg)
    for ex0, ey0, ex1, ey1 in ERASE.get(name, []):
        a[int((ey0 - box[1]) * k):int((ey1 - box[1]) * k), int((ex0 - box[0]) * k):int((ex1 - box[0]) * k)] = 0
    a *= edge_fade(*a.shape, 0.02 if name == "p-festa" else FEATHER)
    noisy = float(((a > 0) & (a < 0.2)).mean())
    # nos pixels quase transparentes a cor recalculada é só ruído: usa a cor dos vizinhos firmes (traço ou preenchimento)
    conf = (a >= 0.3).astype(np.float32)
    blur = lambda arr: np.asarray(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(2.5)), np.float32)
    cb = blur(conf * 255) / 255
    est = np.dstack([blur(color[..., c] * conf) / np.maximum(cb, 1e-3) for c in range(3)])
    est[cb < 0.01] = 255
    color = np.where((a < 0.3)[..., None], est, color)
    color[a == 0] = 255
    rgba = np.dstack([color, a * 255]).astype(np.uint8)
    res = Image.fromarray(rgba, "RGBA")
    res = res.resize((width, round(res.height * width / res.width)), Image.LANCZOS)
    path = os.path.join(out_dir, name + ".webp")
    res.save(path, "WEBP", quality=80, alpha_quality=80, method=6)
    print(f"{name}.webp {res.width}x{res.height} {os.path.getsize(path)//1024} KB  fundo={bg.round().tolist()} meio-transparente={noisy:.1%}")

# celular: é um mockup com sombra, então recorta o aparelho com cantos arredondados em vez de tirar o fundo
im = Image.open(os.path.join(site, "personagens", "celular.jpg")).convert("RGB")
k = im.width / 1493
box = tuple(int(v * k) for v in (322, 194, 1174, 1834))
ph = im.crop(box)
mask = Image.new("L", ph.size, 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), radius=int(128 * k), fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(1.2))
ph.putalpha(mask)
ph = ph.resize((520, round(ph.height * 520 / ph.width)), Image.LANCZOS)
path = os.path.join(out_dir, "p-story.webp")
ph.save(path, "WEBP", quality=86, method=6)
print(f"p-story.webp {ph.width}x{ph.height} {os.path.getsize(path)//1024} KB")

# Ana: rosto da personagem (imagem 07) para o balão do WhatsApp; o círculo é feito no CSS, por isso o fundo creme fica
im = Image.open(os.path.join(site, "personagens", "07.jpg")).convert("RGB")
k = im.width / 2000
ana = im.crop(tuple(int(v * k) for v in (510, 330, 750, 570))).resize((160, 160), Image.LANCZOS)
path = os.path.join(out_dir, "ana.webp")
ana.save(path, "WEBP", quality=86, method=6)
print(f"ana.webp {ana.width}x{ana.height} {os.path.getsize(path)//1024} KB")
