import pygame
import random
import time
import os

# 1. PYGAME VA OVOZ TIZIMINI SOZLASH
pygame.init()
try:
    pygame.mixer.init()
except:
    pass

info = pygame.display.Info()
EKRAN_KENG, EKRAN_BAL = info.current_w, info.current_h
ekran = pygame.display.set_mode((EKRAN_KENG, EKRAN_BAL), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Pro 2026")

# RANGALAR
QORA = (10, 10, 10)
OQ = (255, 255, 255)
YASHIL = (0, 255, 120)
QIZIL = (255, 60, 60)
KULRANG = (45, 45, 45)
SUPER_RANG = (255, 215, 0)

# SHRIFTLAR
shrift_katta = pygame.font.SysFont("arial", 90, bold=True)
shrift_orta = pygame.font.SysFont("arial", 50, bold=True)
shrift_kichik = pygame.font.SysFont("arial", 35, bold=True)

# --- FAYLLAR YO'LINI ANIQLASH ---
joriy_papka = os.path.dirname(os.path.abspath(__file__))

def fayl_yoli(nom):
    return os.path.join(joriy_papka, nom)

# --- OVOZLARNI YUKLASH ---
SND_EAT = None
SND_CLICK = None
try:
    if os.path.exists(fayl_yoli("eat.wav")):
        SND_EAT = pygame.mixer.Sound(fayl_yoli("eat.wav"))
    if os.path.exists(fayl_yoli("tugma_bos.wav")):
        SND_CLICK = pygame.mixer.Sound(fayl_yoli("tugma_bos.wav"))
except:
    pass

# --- MA'LUMOTLARNI SAQLASH ---
def yuklash(fayl, default):
    p = fayl_yoli(fayl)
    if not os.path.exists(p): return default
    with open(p, "r") as f: return f.read().strip()

def saqlash(fayl, qiymat):
    with open(fayl_yoli(fayl), "w") as f: f.write(str(qiymat))

jami_tanga = int(yuklash("tangalar.txt", "0"))
joriy_til = yuklash("til.txt", "UZ")

TILLAR = {
    "UZ": {"title": "ILONCHA 2026", "start": "BOSHLASH", "settings": "SOZLAMALAR", "play": "O'YNASH", "shop": "DO'KON", "back": "ORQAGA", "gameover": "O'YIN TUGADI", "score": "Ochko", "coins": "Tanga", "used": "TANLANDI", "locked": "YAQINDA"},
    "EN": {"title": "SNAKE PRO", "start": "START", "settings": "SETTINGS", "play": "PLAY", "shop": "SHOP", "back": "BACK", "gameover": "GAME OVER", "score": "Score", "coins": "Coins", "used": "SELECTED", "locked": "SOON"},
    "RU": {"title": "ЗМЕЙКА", "start": "СТАРТ", "settings": "НАСТРОЙКИ", "play": "ИГРАТЬ", "shop": "МАГАЗИН", "back": "НАЗАД", "gameover": "ФИНИШ", "score": "Счет", "coins": "Монеты", "used": "ВЫБРАНО", "locked": "СКОРО"}
}

# --- GRAFIKA ---
katak_soni = 20
blok_olchami = (EKRAN_KENG * 0.85) // katak_soni
maydon_olchami = katak_soni * blok_olchami
off_x = (EKRAN_KENG - maydon_olchami) // 2
off_y = 100

def rasm_yukla(nom, w, h):
    try:
        img = pygame.image.load(fayl_yoli(nom)).convert_alpha()
        return pygame.transform.scale(img, (int(w), int(h)))
    except:
        s = pygame.Surface((w, h)); s.fill(YASHIL); return s

IMG_BOSH = rasm_yukla("Ilon_boshi.png", blok_olchami, blok_olchami)
IMG_TANA = rasm_yukla("Ilon_tanasi.jpg", blok_olchami, blok_olchami)
IMG_DUM = rasm_yukla("Ilon_dumi.png", blok_olchami, blok_olchami)
IMG_OVQAT = rasm_yukla("Apple2026.png", blok_olchami, blok_olchami)
IMG_TOSH = rasm_yukla("Tosh.png", blok_olchami, blok_olchami)
IMG_MAYDON_FON = rasm_yukla("Oyin_maydoni.jpg", maydon_olchami, maydon_olchami)

def burish(rasm, dx, dy):
    if dx == 1: return rasm
    if dx == -1: return pygame.transform.rotate(rasm, 180)
    if dy == -1: return pygame.transform.rotate(rasm, 90)
    if dy == 1: return pygame.transform.rotate(rasm, 270)
    return rasm

def yangi_joy(ilon_tanasi, toshlar=[]):
    while True:
        joy = [random.randint(0, katak_soni - 1), random.randint(0, katak_soni - 1)]
        if joy not in ilon_tanasi and joy not in toshlar:
            return joy

# --- SHOP OYNASI ---
def shop_oynasi():
    global jami_tanga
    while True:
        ekran.fill(QORA)
        t_txt = shrift_orta.render(f"💰 {jami_tanga}", True, SUPER_RANG)
        ekran.blit(t_txt, (EKRAN_KENG - 250, 40))
        katak_w, katak_h = 320, 400
        start_x = (EKRAN_KENG - (3 * katak_w + 120)) // 2
        for i in range(3):
            box = pygame.Rect(start_x + i * (katak_w + 60), 250, katak_w, katak_h)
            pygame.draw.rect(ekran, (20, 20, 20), box, border_radius=25)
            if i == 0:
                pygame.draw.rect(ekran, SUPER_RANG, box, border_radius=25, width=5)
                nom = shrift_kichik.render("Standart", True, OQ)
                ekran.blit(nom, nom.get_rect(center=(box.centerx, box.y + 180)))
                btn = pygame.Rect(box.x + 30, box.y + 300, katak_w - 60, 60)
                pygame.draw.rect(ekran, YASHIL, btn, border_radius=15)
                ekran.blit(shrift_kichik.render(TILLAR[joriy_til]["used"], True, QORA), shrift_kichik.render(TILLAR[joriy_til]["used"], True, QORA).get_rect(center=btn.center))
            else:
                lock = shrift_orta.render("🔒", True, KULRANG)
                ekran.blit(lock, lock.get_rect(center=(box.centerx, box.centery)))
        back = pygame.Rect(50, 40, 220, 75)
        pygame.draw.rect(ekran, QIZIL, back, border_radius=20)
        ekran.blit(shrift_kichik.render(TILLAR[joriy_til]["back"], True, OQ), shrift_kichik.render(TILLAR[joriy_til]["back"], True, OQ).get_rect(center=back.center))
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(ev.pos):
                    if SND_CLICK: SND_CLICK.play() # ORQAGA
                    return
            if ev.type == pygame.QUIT: pygame.quit(); exit()

# --- MENYU ---
def welcome_screen():
    while True:
        ekran.fill(QORA)
        title = shrift_katta.render(TILLAR[joriy_til]["title"], True, YASHIL)
        ekran.blit(title, title.get_rect(center=(EKRAN_KENG//2, 200)))
        b_btn, s_btn = pygame.Rect(EKRAN_KENG//2-250, 450, 500, 120), pygame.Rect(EKRAN_KENG//2-250, 620, 500, 120)
        pygame.draw.rect(ekran, SUPER_RANG, b_btn, border_radius=25); pygame.draw.rect(ekran, KULRANG, s_btn, border_radius=25)
        ekran.blit(shrift_orta.render(TILLAR[joriy_til]["start"], True, QORA), shrift_orta.render(TILLAR[joriy_til]["start"], True, QORA).get_rect(center=b_btn.center))
        ekran.blit(shrift_orta.render(TILLAR[joriy_til]["settings"], True, OQ), shrift_orta.render(TILLAR[joriy_til]["settings"], True, OQ).get_rect(center=s_btn.center))
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if b_btn.collidepoint(ev.pos):
                    if SND_CLICK: SND_CLICK.play() # BOSHLASH
                    return
                if s_btn.collidepoint(ev.pos):
                    if SND_CLICK: SND_CLICK.play() # SOZLAMALAR
                    sozlamalar_oynasi()
            if ev.type == pygame.QUIT: pygame.quit(); exit()

def start_menu():
    global jami_tanga
    while True:
        ekran.fill(QORA)
        t_txt = shrift_orta.render(f"💰 {jami_tanga}", True, SUPER_RANG)
        ekran.blit(t_txt, (EKRAN_KENG - 250, 40))
        p_btn, s_btn, b_btn = pygame.Rect(EKRAN_KENG//2-250, 300, 500, 100), pygame.Rect(EKRAN_KENG//2-250, 430, 500, 100), pygame.Rect(EKRAN_KENG//2-250, 560, 500, 100)
        for btn, r, t in [(p_btn, YASHIL, "play"), (s_btn, SUPER_RANG, "shop"), (b_btn, KULRANG, "back")]:
            pygame.draw.rect(ekran, r, btn, border_radius=20)
            ekran.blit(shrift_orta.render(TILLAR[joriy_til][t], True, QORA), shrift_orta.render(TILLAR[joriy_til][t], True, QORA).get_rect(center=btn.center))
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if p_btn.collidepoint(ev.pos):
                    if SND_CLICK: SND_CLICK.play() # O'YNASH
                    return "play"
                if s_btn.collidepoint(ev.pos):
                    if SND_CLICK: SND_CLICK.play() # DO'KON
                    shop_oynasi()
                if b_btn.collidepoint(ev.pos):
                    if SND_CLICK: SND_CLICK.play() # ORQAGA
                    return "back"
            if ev.type == pygame.QUIT: pygame.quit(); exit()

def sozlamalar_oynasi():
    global joriy_til
    while True:
        ekran.fill(QORA)
        opts = [("O'ZBEK", "UZ", 300), ("ENGLISH", "EN", 450), ("PYCCКИЙ", "RU", 600)]
        for label, code, y in opts:
            btn = pygame.Rect(EKRAN_KENG//2-200, y, 400, 100)
            pygame.draw.rect(ekran, YASHIL if joriy_til==code else KULRANG, btn, border_radius=20)
            ekran.blit(shrift_orta.render(label, True, OQ), shrift_orta.render(label, True, OQ).get_rect(center=btn.center))
            if pygame.mouse.get_pressed()[0] and btn.collidepoint(pygame.mouse.get_pos()):
                if joriy_til != code:
                    if SND_CLICK: SND_CLICK.play() # TIL TANLASH
                    joriy_til = code; saqlash("til.txt", code)
        b_btn = pygame.Rect(50, 40, 200, 70)
        pygame.draw.rect(ekran, QIZIL, b_btn, border_radius=15)
        ekran.blit(shrift_kichik.render(TILLAR[joriy_til]["back"], True, OQ), shrift_kichik.render(TILLAR[joriy_til]["back"], True, OQ).get_rect(center=b_btn.center))
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN and b_btn.collidepoint(ev.pos):
                if SND_CLICK: SND_CLICK.play() # ORQAGA
                return
            if ev.type == pygame.QUIT: pygame.quit(); exit()

# --- O'YIN ---
def oyin_tsikli():
    global jami_tanga
    ix, iy, dx, dy, ilon, score, boshlandi = 10, 10, 0, 0, [[8,10], [9,10], [10,10]], 0, False
    turbo_active, turbo_st, last_turbo = False, 0, time.time() - 15
    toshlar = [yangi_joy(ilon) for _ in range(6)]
    ov_joy = yangi_joy(ilon, toshlar)
    ov_x, ov_y = ov_joy[0], ov_joy[1]
    soat = pygame.time.Clock()
    m_x, m_y = EKRAN_KENG//2, off_y + maydon_olchami + 240
    tepa, past, chap, ong, turbo_btn = pygame.Rect(m_x-80, m_y-180, 160, 160), pygame.Rect(m_x-80, m_y+180, 160, 160), pygame.Rect(m_x-260, m_y, 160, 160), pygame.Rect(m_x+100, m_y, 160, 160), pygame.Rect(m_x-80, m_y, 160, 160)

    while True:
        h = time.time()
        if turbo_active and h - turbo_st >= 7: turbo_active, last_turbo = False, h
        can_turbo = (not turbo_active) and (h - last_turbo >= 15)
        ekran.fill(QORA); ekran.blit(IMG_MAYDON_FON, (off_x, off_y))
        ekran.blit(shrift_orta.render(f"{TILLAR[joriy_til]['score']}: {score}", True, OQ), (off_x, 30))
        ekran.blit(shrift_orta.render(f"💰 {jami_tanga}", True, SUPER_RANG), (EKRAN_KENG-250, 30))

        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if tepa.collidepoint(ev.pos) and dy==0: dx, dy, boshlandi = 0, -1, True
                elif past.collidepoint(ev.pos) and dy==0: dx, dy, boshlandi = 0, 1, True
                elif chap.collidepoint(ev.pos) and dx==0: dx, dy, boshlandi = -1, 0, True
                elif ong.collidepoint(ev.pos) and dx==0: dx, dy, boshlandi = 1, 0, True
                elif turbo_btn.collidepoint(ev.pos) and can_turbo: turbo_active, turbo_st = True, h
            if ev.type == pygame.QUIT: pygame.quit(); exit()

        if boshlandi:
            ix += dx; iy += dy
            if ix<0 or ix>=20 or iy<0 or iy>=20 or [ix,iy] in ilon[:-1] or [ix,iy] in toshlar:
                y_tanga = score // 10
                jami_tanga += y_tanga
                saqlash("tangalar.txt", jami_tanga)
                start_time = time.time()
                while time.time() - start_time < 3:
                    ekran.fill(QORA)
                    txt_over = shrift_katta.render(TILLAR[joriy_til]["gameover"], True, QIZIL)
                    ekran.blit(txt_over, txt_over.get_rect(center=(EKRAN_KENG//2, EKRAN_BAL//2 - 100)))
                    txt_res = shrift_orta.render(f"{TILLAR[joriy_til]['score']}: {score}  |  +{y_tanga} 💰", True, OQ)
                    ekran.blit(txt_res, txt_res.get_rect(center=(EKRAN_KENG//2, EKRAN_BAL//2 + 50)))
                    pygame.display.update()
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT: pygame.quit(); exit()
                return

            ilon.append([ix,iy])
            if ix==ov_x and iy==ov_y:
                if SND_EAT: SND_EAT.play()
                score += 20 if turbo_active else 10
                ov_joy = yangi_joy(ilon, toshlar); ov_x, ov_y = ov_joy[0], ov_joy[1]
            else: ilon.pop(0)

        ekran.blit(IMG_OVQAT, (off_x+ov_x*blok_olchami, off_y+ov_y*blok_olchami))
        for t in toshlar: ekran.blit(IMG_TOSH, (off_x+t[0]*blok_olchami, off_y+t[1]*blok_olchami))
        for i, b in enumerate(ilon):
            px, py = off_x+b[0]*blok_olchami, off_y+b[1]*blok_olchami
            if i == len(ilon)-1: ekran.blit(burish(IMG_BOSH, dx, dy), (px, py))
            elif i == 0: ekran.blit(burish(IMG_DUM, ilon[1][0]-b[0], ilon[1][1]-b[1]), (px, py))
            else: ekran.blit(IMG_TANA, (px, py))

        for r, t in [(tepa,"▲"),(past,"▼"),(chap,"◀"),(ong,"▶")]:
            pygame.draw.rect(ekran, KULRANG, r, border_radius=35)
            ekran.blit(shrift_orta.render(t, True, OQ), shrift_orta.render(t, True, OQ).get_rect(center=r.center))
        pygame.draw.rect(ekran, YASHIL if turbo_active else (SUPER_RANG if can_turbo else (60,60,60)), turbo_btn, border_radius=35)
        ekran.blit(shrift_kichik.render("2X" if turbo_active else "GO", True, QORA), turbo_btn.center)
        pygame.display.update(); soat.tick(14 if turbo_active else 9)

# --- START ---
while True:
    welcome_screen()
    while True:
        res = start_menu()
        if res == "play": oyin_tsikli()
        else: break
