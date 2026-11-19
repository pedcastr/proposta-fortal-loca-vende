# Recolore os prints do app da equipe (Zé Loc) para a Fortal e troca os dados reais por fictícios.
# Coordenadas na metade da resolução (540x1200); o script multiplica por 2.
import glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = 'C:/Users/Pedro/AppData/Local/Temp/claude/0ac4a722d1abc57c/dec26e6f-edc7-46e9-abfe-3d8a5b57add0/scratchpad/app-equipe/'
OUT = 'D:/Projetos/proposta-fortal-loca-vende/img/app-equipe/'
LOGO = 'D:/Projetos/proposta-fortal-loca-vende/img/logo-fortal.png'
ICONE = 'D:/Projetos/proposta-fortal-loca-vende/img/icone.png'
F = {False: 'C:/Windows/Fonts/segoeui.ttf', True: 'C:/Windows/Fonts/segoeuib.ttf', 's': 'C:/Windows/Fonts/seguisb.ttf'}
NOMES = ['login', 'notificacao', 'inicio', 'menu', 'safelock', 'contratos', 'contrato', 'mapa', 'multas']


def recolor(im, so_saturado_em=None):
    hsv = np.asarray(im.convert('HSV')).astype(float)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    bh = (H > 125) & (H < 185)
    blue = bh & (S > 50)
    light = bh & (S > 8) & (S <= 50) & (V > 170)
    if so_saturado_em:  # dentro do mapa só as bolhas (azul forte), o mar fica como está
        y0, y1 = so_saturado_em
        zona = np.zeros_like(blue); zona[y0:y1] = True
        blue = blue & ~(zona & (S < 150))
        light = light & ~zona
    H2 = np.where(blue | light, 252, H)
    dark = blue & (V < 90)
    S2 = np.where(dark, S * .75, np.where(blue, np.minimum(255, S * 1.05), np.where(light, S * .7, S)))
    V2 = np.where(dark, V * .6, V)
    return Image.fromarray(np.stack([H2, S2, V2], -1).clip(0, 255).astype(np.uint8), 'HSV').convert('RGB')


def lum(c): return .299 * c[0] + .587 * c[1] + .114 * c[2]


def texto(im, box, linhas, size, bold=False, align='left', cor=None, fundo=None, pad=3, limpar=True):
    x0, y0, x1, y1 = [v * 2 for v in box]
    a = np.asarray(im)
    bg = tuple(int(v) for v in (fundo or a[(y0 + y1) // 2, max(0, x0 - 6)]))
    if cor is None:
        reg = a[y0:y1, x0:x1].reshape(-1, 3)
        ls = reg @ np.array([.299, .587, .114])
        cor = tuple(int(v) for v in (reg[ls.argmax()] if lum(bg) < 128 else reg[ls.argmin()]))
    d = ImageDraw.Draw(im)
    if limpar: d.rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], fill=bg)
    f = ImageFont.truetype(F[bold], int(size * 2 * 1.62))
    if isinstance(linhas, str): linhas = [linhas]
    lh = (y1 - y0) / len(linhas)
    for i, t in enumerate(linhas):
        cy = y0 + lh * i + lh / 2
        if align == 'center':
            d.text(((x0 + x1) / 2, cy), t, font=f, fill=cor, anchor='mm')
        else:
            d.text((x0, cy), t, font=f, fill=cor, anchor='lm')


def colar(im, caminho, box, circulo=False):
    x0, y0, x1, y1 = [v * 2 for v in box]
    p = Image.open(caminho).convert('RGBA')
    p.thumbnail((x1 - x0, y1 - y0), Image.LANCZOS)
    if circulo:
        m = Image.new('L', p.size, 0); ImageDraw.Draw(m).ellipse([0, 0, p.size[0] - 1, p.size[1] - 1], fill=255)
        p.putalpha(m)
    im.paste(p, (x0 + (x1 - x0 - p.size[0]) // 2, y0 + (y1 - y0 - p.size[1]) // 2), p)


arqs = dict(zip(NOMES, sorted(glob.glob(SRC + '*.jpg'))))
res = {}

# --- login: topo preto da marca + logo da Fortal
im = recolor(Image.open(arqs['login']).convert('RGB'))
a = np.asarray(im).astype(float)
a[:90] = a[:90] * np.array([.32, .18, .2])  # barra de status escurecida
h = 670 - 90
g = np.linspace(0, 1, h)[:, None]
topo = np.zeros((h, a.shape[1], 3))
c0, c1 = np.array([10, 10, 11]), np.array([58, 8, 12])
xx = np.linspace(0, 1, a.shape[1])[None, :]
mix = np.clip(.55 * g + .45 * xx, 0, 1)[..., None]
topo = c0 * (1 - mix) + c1 * mix
a[90:670] = topo
im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
colar(im, LOGO, (90, 100, 450, 225))
texto(im, (60, 248, 480, 282), 'Bem-vindo à Fortal Loca & Vende', 15, True, 'center', cor=(255, 255, 255), limpar=False)
texto(im, (62, 572, 420, 600), 'equipe@fortallocaevende.com', 13, cor=(31, 31, 31))
res['login'] = im

# --- notificação no celular
im = recolor(Image.open(arqs['notificacao']).convert('RGB'))
colar(im, ICONE, (42, 203, 76, 237), circulo=True)
texto(im, (91, 208, 300, 230), 'Fortal Loca & Vende  •  agora', 10.5)
texto(im, (91, 252, 470, 279), 'OS #218 aguardando sua aprovação', 12.5, True)
texto(im, (91, 288, 500, 340), ['Moto Peças do Zé · Bros 160 · R$ 286,00', '3 fotos · toque para aprovar ou recusar'], 11)
res['notificacao'] = im

# --- início do app da equipe
im = recolor(Image.open(arqs['inicio']).convert('RGB'))
texto(im, (75, 66, 300, 88), 'FORTAL LOCA & VENDE', 10.5, True, cor=(255, 225, 226))
texto(im, (370, 588, 515, 618), 'SafeLock', 12.5, False, 'center')
texto(im, (200, 1102, 340, 1164), ['Mapa', '(ÁgilLock)'], 12.5, False, 'center')
# Rastreamento (próprio da Zé Loc) vira Multas, com o ícone de alerta de Sinistros
a = im.copy()
ic = a.crop((250 * 2, 860 * 2, 290 * 2, 898 * 2))
ImageDraw.Draw(im).rectangle([414 * 2, 1070 * 2, 472 * 2, 1112 * 2], fill=tuple(int(v) for v in np.asarray(im)[1060 * 2, 380 * 2]))
im.paste(ic, (423 * 2, 1072 * 2))
texto(im, (370, 1118, 515, 1146), 'Multas', 12.5, False, 'center')
res['inicio'] = im

# --- consultas SafeLock (com a origem VozChat)
im = recolor(Image.open(arqs['safelock']).convert('RGB'))
texto(im, (70, 66, 360, 100), 'Consultas SafeLock', 17, True, cor=(255, 255, 255))
texto(im, (70, 102, 485, 124), 'Conectada · cada consulta é cobrada na conta SafeLock', 10.5, cor=(255, 225, 226))
for y, nome, cpf in [(422, 'BRUNO TAVARES LIMA', '***.733.208-**'), (681, 'LIA MATOS DE OLIVEIRA', '***.190.775-**'), (940, 'WILLIAN K. TEIXEIRA', '***.592.184-**')]:
    texto(im, (35, y, 440, y + 26), nome, 13)
    texto(im, (35, y + 33, 210, y + 58), cpf, 12.5)
res['safelock'] = im

# --- contratos
im = recolor(Image.open(arqs['contratos']).convert('RGB'))
texto(im, (245, 200, 300, 228), '4', 13.5, True)
for y, t in [(360, '#463 · DIEGO ROCHA DA SILVA'), (575, '#462 · CAIO PRADO MENEZES'), (789, '#461 · ANA PAULA MOURA'), (1004, '#460 · RAFAEL SILVA NUNES')]:
    texto(im, (34, y, 460, y + 28), t, 12.5)
res['contratos'] = im

# --- contrato aberto
im = recolor(Image.open(arqs['contrato']).convert('RGB'))
texto(im, (66, 102, 400, 124), 'DIEGO ROCHA DA SILVA', 11, cor=(255, 225, 226))
texto(im, (230, 742, 470, 769), 'Equipe Fortal', 12.5)
texto(im, (230, 872, 470, 930), 'DIEGO ROCHA DA SILVA', 12.5)
texto(im, (230, 951, 460, 978), '***.482.113-**', 12.5)
texto(im, (230, 999, 460, 1025), '(85) 9 ****-4120', 12.5)
texto(im, (230, 1046, 465, 1137), 'diego@email.com', 12.5)
res['contrato'] = im

# --- mapa (só cabeçalho e bolhas)
im = recolor(Image.open(arqs['mapa']).convert('RGB'), so_saturado_em=(580, 2090))
texto(im, (112, 1128, 288, 1154), 'MARCOS A. LIMA', 11.5)
texto(im, (403, 1128, 540, 1154), 'JÉSSICA N. SOUZA', 11.5)
res['mapa'] = im

# --- multas
im = recolor(Image.open(arqs['multas']).convert('RGB'))
texto(im, (34, 344, 190, 374), 'R$ 1.284,60', 13.5, True)
texto(im, (228, 344, 268, 374), '3', 13.5, True)
for y, l1, l2 in [(494, 'MARCOS A. LIMA', 'HONDA NXR 160 BROS'), (724, 'RAFAEL S. NUNES', 'YAMAHA ZR 125 CONNECTED'), (1023, 'ANA P. MOURA · HONDA', 'CG 160 START')]:
    texto(im, (106, y, 470, y + 52), [l1, l2], 11)
res['multas'] = im

import os
os.makedirs(OUT, exist_ok=True)
for n, im in res.items():
    im.thumbnail((540, 1200), Image.LANCZOS)
    im.save(OUT + n + '.jpg', quality=88)
    print(n, im.size)
