# Kit de personagens no estilo "Notion": traço preto, preenchimento branco, laranja só em detalhes.
import math
INK = "#1C1F26"; WHITE = "#FFFFFF"; AMBER = "#E85002"; SOFT = "#F3EFE8"; GREY = "#C9C4BB"; TINT = "#FCE7DA"
SW = 3.2

def _pt(x, y, ang, L):
    a = math.radians(ang)
    return x + math.sin(a) * L, y + math.cos(a) * L

def limb(x, y, a1, a2, L1, L2, inner, outer=INK, w=12, wi=6):
    kx, ky = _pt(x, y, a1, L1); ex, ey = _pt(kx, ky, a2, L2)
    d = f"M{x:.1f} {y:.1f} L{kx:.1f} {ky:.1f} L{ex:.1f} {ey:.1f}"
    s = f'<path d="{d}" fill="none" stroke="{outer}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    if inner != outer:
        s += f'<path d="{d}" fill="none" stroke="{inner}" stroke-width="{wi}" stroke-linecap="round" stroke-linejoin="round"/>'
    return s, (ex, ey)

def hair(style, color=INK):
    if style == "short":
        return f'<path d="M-23.5 -157 C-26 -186 24 -192 24.5 -160 C16 -169 4 -171 -6 -166 C-13 -170 -20 -167 -23.5 -157 Z" fill="{color}"/>'
    if style == "bun":
        return (f'<circle cx="2" cy="-187" r="10" fill="{color}"/>'
                f'<path d="M-23.5 -156 C-25 -188 25 -190 24 -157 C14 -170 -6 -172 -23.5 -156 Z" fill="{color}"/>')
    if style == "curly":
        cs = [(-20, -168, 9), (-12, -179, 10), (0, -184, 10), (12, -180, 10), (20, -170, 9), (24, -159, 7), (-24, -158, 7)]
        return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>' for x, y, r in cs)
    if style == "cap":
        return (f'<path d="M-23 -160 C-24 -190 24 -190 23 -160 Z" fill="{AMBER}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                f'<path d="M14 -161 L44 -160" stroke="{INK}" stroke-width="{SW+3}" stroke-linecap="round"/>'
                f'<circle cx="0" cy="-189" r="3" fill="{INK}"/>')
    if style == "long_front":
        return f'<path d="M-24 -154 C-27 -190 26 -192 24 -156 C16 -166 8 -170 -2 -163 C-10 -168 -18 -164 -24 -154 Z" fill="{color}"/>'
    return ""

def hair_back(style, color=INK):
    if style == "long_front":
        return f'<path d="M-28 -152 C-32 -200 32 -200 28 -152 L30 -122 Q22 -118 18 -132 L-18 -132 Q-22 -118 -30 -122 Z" fill="{color}"/>'
    return ""

def face(expr="smile", look=0):
    e = f'<circle cx="{-8+look}" cy="-158" r="2.6" fill="{INK}"/><circle cx="{8+look}" cy="-158" r="2.6" fill="{INK}"/>'
    if expr == "smile":
        m = f'<path d="M{-7+look} -147 Q{look} -141 {7+look} -147" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
    elif expr == "open":
        m = f'<path d="M{-7+look} -148 Q{look} -137 {7+look} -148 Z" fill="{INK}"/>'
    elif expr == "worried":
        m = (f'<path d="M{-6+look} -144 Q{look} -148 {6+look} -144" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
             f'<path d="M{-13+look} -167 L{-4+look} -164 M{13+look} -167 L{4+look} -164" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
    else:
        m = f'<path d="M{-5+look} -145 L{5+look} -145" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
    return e + m

def person(x=0, y=0, s=1, shirt=WHITE, pants=INK, hair_style="short", expr="smile", look=0,
           armL=(15, 10), armR=(-15, -10), legL=(8, 0), legR=(-8, 0), lift=0, flip=False, extra_front="", extra_back=""):
    """armL/armR: (ombro, cotovelo) em graus a partir da vertical para baixo; positivo gira para a direita da tela."""
    out = []
    sx = -s if flip else s
    out.append(f'<g transform="translate({x} {y}) scale({sx} {s})">')
    out.append(f'<ellipse cx="0" cy="2" rx="30" ry="5" fill="{INK}" fill-opacity=".08"/>')
    out.append(f'<g transform="translate(0 {-lift})">')
    out.append(extra_back)
    # pernas
    for hx, (a1, a2) in ((-9, legL), (9, legR)):
        p, (fx, fy) = limb(hx, -62, a1, a2, 34, 32, pants, w=13, wi=7)
        out.append(p)
        dirx = 1 if hx > 0 else -1
        out.append(f'<ellipse cx="{fx+4*dirx:.1f}" cy="{fy+2:.1f}" rx="9" ry="5" fill="{INK}"/>')
    # braço de trás (esquerdo da tela)
    pL, hL = limb(-18, -116, armL[0], armL[1], 30, 28, WHITE, w=11, wi=5)
    # tronco
    torso = f'<path d="M-21 -124 Q-25 -92 -17 -58 L17 -58 Q25 -92 21 -124 Q0 -130 -21 -124 Z" fill="{shirt}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
    pR, hR = limb(18, -116, armR[0], armR[1], 30, 28, WHITE, w=11, wi=5)
    out.append(pL); out.append(torso); out.append(pR)
    for hx, hy in (hL, hR):
        out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="6" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>')
    # pescoço + cabeça
    out.append(f'<path d="M0 -127 L0 -136" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M0 -127 L0 -136" stroke="{WHITE}" stroke-width="4" stroke-linecap="round"/>')
    out.append(hair_back(hair_style))
    out.append(f'<circle cx="0" cy="-158" r="23" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>')
    out.append(hair(hair_style))
    out.append(face(expr, look))
    out.append(extra_front)
    out.append('</g></g>')
    return "".join(out), (x, y)

# ---------- objetos ----------
def ball(x, y, r=11):
    return (f'<g transform="translate({x} {y})"><circle r="{r}" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M{-r} 0 Q0 {-r*.55} {r} 0" fill="none" stroke="{AMBER}" stroke-width="2.4"/>'
            f'<path d="M{-r*.3} {-r*.95} Q{r*.35} 0 {-r*.3} {r*.95}" fill="none" stroke="{INK}" stroke-width="1.8"/></g>')

def motion_lines(x, y, n=3, ang=0, L=14, gap=8, color=INK):
    s = ""
    for i in range(n):
        dx = math.cos(math.radians(ang)); dy = math.sin(math.radians(ang))
        ox = -dy * (i - (n-1)/2) * gap; oy = dx * (i - (n-1)/2) * gap
        s += f'<path d="M{x+ox:.1f} {y+oy:.1f} l{dx*L:.1f} {dy*L:.1f}" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/>'
    return s

def sparkle(x, y, r=7, color=AMBER):
    return (f'<path d="M{x} {y-r} L{x} {y+r} M{x-r} {y} L{x+r} {y}" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/>')

def ground(x1, x2, y, wobble=3):
    pts = []; n = 8
    for i in range(n+1):
        xx = x1 + (x2-x1)*i/n; yy = y + (wobble if i % 2 else -wobble*0.4)
        pts.append(f"{xx:.1f} {yy:.1f}")
    return f'<path d="M{" L".join(pts)}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>'

def phone(x, y, w=26, h=46, rot=0, screen=AMBER, play=True):
    s = f'<g transform="translate({x} {y}) rotate({rot})"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="6" fill="{INK}"/>'
    s += f'<rect x="{-w/2+3}" y="{-h/2+4}" width="{w-6}" height="{h-8}" rx="3" fill="{screen}"/>'
    if play:
        s += f'<path d="M-4 -6 L6 0 L-4 6 Z" fill="{WHITE}"/>'
    return s + '</g>'

def heart(x, y, s=1, fill=AMBER):
    return (f'<path transform="translate({x} {y}) scale({s})" d="M0 6 C0 -2 -10 -6 -14 0 C-20 8 -8 16 0 22 C8 16 20 8 14 0 C10 -6 0 -2 0 6 Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="{SW/s:.2f}" stroke-linejoin="round"/>')

def bubble(x, y, w, h, text, fs=16, tail="left", fill=WHITE, color=INK):
    tx = x + 18 if tail == "left" else x + w - 18
    t = f'<path d="M{tx-8} {y+h-1} L{tx-14 if tail=="left" else tx+14} {y+h+14} L{tx+8} {y+h-1}" fill="{fill}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{INK}" stroke-width="{SW}"/>' + t +
            f'<rect x="{tx-10}" y="{y+h-6}" width="20" height="5" fill="{fill}"/>'
            f'<text x="{x+w/2}" y="{y+h/2+fs*0.36}" text-anchor="middle" font-family="Geist, Arial, sans-serif" font-weight="600" font-size="{fs}" fill="{color}">{text}</text>')

def coin(x, y, r=13):
    return (f'<g transform="translate({x} {y})"><circle r="{r}" fill="{AMBER}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<text y="5" text-anchor="middle" font-family="Geist, Arial, sans-serif" font-weight="700" font-size="{r*0.95:.0f}" fill="{WHITE}">R$</text></g>')

def column(x, y_ground, h=170, w=22):
    top = y_ground - h
    s = f'<rect x="{x-w/2}" y="{top}" width="{w}" height="{h}" rx="6" fill="{SOFT}" stroke="{INK}" stroke-width="{SW}"/>'
    s += f'<rect x="{x-w/2-6}" y="{y_ground-10}" width="{w+12}" height="12" rx="3" fill="{INK}"/>'
    # placa
    s += f'<rect x="{x-20}" y="{top-30}" width="40" height="30" rx="6" fill="{AMBER}" stroke="{INK}" stroke-width="{SW}"/><path d="M{x-5} {top-22} L{x+8} {top-15} L{x-5} {top-8} Z" fill="{WHITE}"/>'
    return s

def button_box(x, y, pressed=False):
    s = f'<rect x="{x-20}" y="{y-24}" width="40" height="48" rx="8" fill="{INK}"/>'
    s += f'<circle cx="{x}" cy="{y-4}" r="{11 if not pressed else 9.5}" fill="{AMBER}" stroke="{WHITE}" stroke-width="2"/>'
    s += f'<rect x="{x-11}" y="{y+12}" width="22" height="4" rx="2" fill="{WHITE}" opacity=".7"/>'
    return s

def camera_pole(x, y_ground, h=150):
    top = y_ground - h
    return (f'<path d="M{x} {y_ground} L{x} {top}" stroke="{INK}" stroke-width="{SW+1}" stroke-linecap="round"/>'
            f'<path d="M{x} {top+4} L{x+22} {top-2}" stroke="{INK}" stroke-width="{SW+1}" stroke-linecap="round"/>'
            f'<g transform="translate({x+20} {top-14}) rotate(10)"><rect x="0" y="0" width="46" height="24" rx="6" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<rect x="44" y="5" width="9" height="14" rx="3" fill="{INK}"/><circle cx="10" cy="12" r="3.5" fill="#E5484D"/></g>')

def confetti(x, y, items):
    s = ""
    for dx, dy, kind, rot in items:
        if kind == "r": s += f'<rect x="{x+dx-4}" y="{y+dy-2}" width="8" height="4" rx="1" fill="{AMBER}" transform="rotate({rot} {x+dx} {y+dy})"/>'
        elif kind == "c": s += f'<circle cx="{x+dx}" cy="{y+dy}" r="3.4" fill="none" stroke="{INK}" stroke-width="2"/>'
        else: s += f'<path d="M{x+dx-4} {y+dy} q4 -6 8 0" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" transform="rotate({rot} {x+dx} {y+dy})"/>'
    return s

def svg(w, h, body, label):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">'
            f'{body}</svg>')

# ================= cenas =================
def hero_left():
    b = ground(30, 330, 286)
    p, _ = person(160, 272, 1.0, shirt=AMBER, pants=INK, hair_style="short", expr="open", look=3,
                  armL=(-120, -150), armR=(165, 178), legL=(-35, 25), legR=(30, -20), lift=28)
    b += p
    b += ball(192, 40, 13) + motion_lines(218, 30, 3, -20, 16, 8)
    b += sparkle(70, 80) + sparkle(270, 120, 6)
    return svg(360, 300, b, "Jogador saltando para cortar a bola")

def hero_right():
    b = ground(30, 330, 286)
    front = phone(0, -112, 30, 50, 0)
    p, _ = person(176, 280, 1.0, shirt=WHITE, pants=INK, hair_style="curly", expr="open", look=0,
                  armL=(20, 140), armR=(-20, -140), legL=(-6, 0), legR=(6, 0), extra_front=front)
    b += p
    b += bubble(212, 40, 104, 40, "▶ 30 s", 17, "left", fill=WHITE)
    b += sparkle(106, 72) + sparkle(92, 106, 5) + sparkle(262, 122, 6)
    return svg(360, 300, b, "Jogadora vendo o replay do lance no celular, animada")

def problem_scene():
    b = ground(20, 300, 276)
    front = phone(80, -140, 44, 28, -8, screen="#2A2D35", play=False) + '<circle cx="96" cy="-143" r="3" fill="#E5484D"/>'
    p, _ = person(130, 270, 1.0, shirt=SOFT, pants=INK, hair_style="long_front", expr="worried", look=4,
                  armL=(-14, -6), armR=(110, 100), legL=(-6, 0), legR=(6, 0), extra_front=front)
    b += p
    b += bubble(196, 34, 54, 42, "?", 22, "left")
    b += '<path d="M104 92 q6 8 0 14 q-6 -6 0 -14 Z" fill="#9AC8F0" stroke="#1C1F26" stroke-width="2.4"/>'
    b += ball(276, 150, 11) + motion_lines(256, 140, 3, 210, 12, 7)
    return svg(320, 290, b, "Amigo filmando com o celular e perdendo o lance")

def press_scene():
    b = ground(20, 440, 300)
    b += camera_pole(52, 300, 190)
    b += column(330, 300, 200)
    b += button_box(306, 166, pressed=True)
    b += motion_lines(300, 132, 3, -90, 10, 9, AMBER)
    p, _ = person(212, 296, 1.05, shirt=AMBER, pants=INK, hair_style="cap", expr="smile", look=4,
                  armL=(-14, -6), armR=(95, 92), legL=(-6, 0), legR=(6, 0))
    b += p
    b += ball(112, 288, 11)
    b += bubble(358, 40, 92, 36, "Replay!", 15, "left", fill=WHITE)
    return svg(460, 320, b, "Jogador apertando o botão de replay na coluna da quadra")

def owner_scene():
    b = ground(20, 280, 266)
    front = coin(-62, -118, 14)
    p, _ = person(160, 260, 1.0, shirt=WHITE, pants=INK, hair_style="cap", expr="smile", look=-2,
                  armL=(-40, -120), armR=(150, 175), legL=(-6, 0), legR=(6, 0), extra_front=front)
    b += p
    b += coin(60, 236, 13) + coin(86, 244, 13) + coin(72, 222, 13)
    b += sparkle(236, 60) + sparkle(252, 92, 5)
    return svg(300, 280, b, "Dono da arena feliz com a receita de patrocínio")

def support_scene():
    b = ground(20, 280, 266)
    p, _ = person(130, 260, 1.0, shirt=AMBER, pants=INK, hair_style="bun", expr="smile",
                  armL=(-14, -6), armR=(150, 175), legL=(-6, 0), legR=(6, 0))
    b += p
    b += bubble(176, 34, 108, 40, "Pode falar!", 15, "left")
    b += motion_lines(186, 92, 3, -40, 10, 7)
    return svg(300, 280, b, "Atendente da Aatlas acenando")

def celebrate_scene():
    b = ground(10, 530, 286)
    p1, _ = person(120, 280, .95, shirt=AMBER, pants=INK, hair_style="short", expr="open", armL=(-14, -6), armR=(150, 165), legL=(-8, 0), legR=(8, 0), lift=6)
    p2, _ = person(270, 282, 1.0, shirt=WHITE, pants=INK, hair_style="cap", expr="open", armL=(-160, -172), armR=(160, 172), legL=(-18, 12), legR=(18, -12), lift=18)
    p3, _ = person(420, 280, .95, shirt=SOFT, pants=INK, hair_style="long_front", expr="open", armL=(-150, -165), armR=(150, 165), legL=(-8, 0), legR=(8, 0), lift=6)
    b += p1 + p2 + p3
    b += confetti(270, 44, [(-90, 10, "r", 20), (-50, -10, "c", 0), (-10, 4, "w", 30), (40, -14, "r", -30), (80, 12, "c", 0), (120, -4, "w", -20), (-130, 30, "w", 10), (150, 30, "r", 60)])
    b += phone(462, 106, 24, 40, 12)
    return svg(540, 300, b, "Dono da arena e jogadores comemorando")

SCENES = {"hero_left": hero_left, "hero_right": hero_right, "problem": problem_scene, "press": press_scene,
          "owner": owner_scene, "support": support_scene, "celebrate": celebrate_scene}

if __name__ == "__main__":
    import json, sys
    out = {k: f() for k, f in SCENES.items()}
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "chars.json", "w"), ensure_ascii=False)
    sheet = '<html><body style="margin:0;background:#F7F5F0;display:flex;flex-wrap:wrap;gap:16px;padding:16px">' + "".join(
        f'<div style="background:#fff;border-radius:16px;padding:8px;width:420px"><div style="font:12px monospace">{k}</div>{v}</div>' for k, v in out.items()) + "</body></html>"
    open("chars_sheet.html", "w").write(sheet)
    print("ok", len(out))
