from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


ROOT = Path(r"C:\Users\user\Documents\ChatGPT\cropriクライアント")
OUT = ROOT / "上田瓦商店" / "ロゴ案" / "proposal-v1"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1240, 1754  # A4 at 150 dpi
M = 86

FONT = Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf")


def f(size: int, index: int = 0):
    return ImageFont.truetype(str(FONT), size=size, index=index)


def fit_text(draw, text, max_width, start_size, min_size=18):
    size = start_size
    while size > min_size:
        font = f(size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
        size -= 1
    return f(min_size)


def cover(img, src, box, contain=True):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    pic = src.copy()
    if contain:
        pic.thumbnail((bw, bh), Image.Resampling.LANCZOS)
        x = x0 + (bw - pic.width) // 2
        y = y0 + (bh - pic.height) // 2
        img.alpha_composite(pic.convert("RGBA"), (x, y))
    else:
        pic = ImageOps.fit(pic, (bw, bh), method=Image.Resampling.LANCZOS)
        img.alpha_composite(pic.convert("RGBA"), (x0, y0))


def page_base():
    return Image.new("RGBA", (W, H), "#f2f1ed")


def page1():
    img = page_base()
    d = ImageDraw.Draw(img)
    ink = "#101113"
    gray = "#666a70"
    lime = "#d8ff42"

    d.rectangle((0, 0, W, 22), fill=lime)
    d.text((M, 70), "LOGO CONCEPT / 01", font=f(25), fill=gray)
    d.text((M, 118), "U-BRACE", font=f(100), fill=ink)
    d.text((M, 236), "瓦を描かず、瓦職人の仕事を記号化。", font=f(32), fill=ink)

    panel = (M, 330, W - M, 920)
    d.rounded_rectangle(panel, radius=10, fill=ink)
    compact_path = ROOT / "上田瓦商店" / "ロゴ案" / "u-brace-v2" / "上田瓦商店_U-BRACE_compact_v2.png"
    logo = Image.open(compact_path).convert("RGBA")
    # Existing art is black; turn visible artwork white while retaining alpha.
    alpha = logo.getchannel("A")
    white = Image.new("RGBA", logo.size, "white")
    white.putalpha(alpha)
    cover(img, white, (250, 380, 990, 865), contain=True)
    d.rectangle((panel[0] + 28, panel[1] + 28, panel[0] + 150, panel[1] + 38), fill=lime)

    body = (
        "UEDAの頭文字『U』を基礎に、棟を支える補強金物の構造感と、\n"
        "鬼瓦の角を思わせる切断面を重ねたシンボル。\n"
        "一般的な屋根型や瓦の波形から離れ、現場で働く人のための\n"
        "ワークブランドとして設計した。"
    )
    d.multiline_text((M, 972), body, font=f(27), fill=ink, spacing=11)

    cards = [
        ("U", "UEDA", "上田の頭文字。\n社名を一目で記憶させる。"),
        ("B", "BRACE", "棟補強金物の構造感。\n支える仕事の強さを表す。"),
        ("E", "EDGE", "鬼瓦の角と切断面。\n丸くせず、鋭く仕上げる。"),
    ]
    cw = (W - 2 * M - 36) // 3
    y0, y1 = 1260, 1548
    for i, (letter, title, desc) in enumerate(cards):
        x0 = M + i * (cw + 18)
        x1 = x0 + cw
        d.rounded_rectangle((x0, y0, x1, y1), radius=7, fill="#ffffff", outline="#d5d5d1", width=2)
        d.text((x0 + 25, y0 + 22), letter, font=f(58), fill=ink)
        d.text((x0 + 25, y0 + 104), title, font=f(24), fill=gray)
        d.multiline_text((x0 + 25, y0 + 162), desc, font=f(20), fill=ink, spacing=10)

    d.text((M, 1648), "㈲上田瓦商店  /  WORK IDENTITY PROPOSAL", font=f(19), fill=gray)
    d.text((W - M - 125, 1648), "2026.10", font=f(19), fill=gray)
    path = OUT / "上田瓦商店_ロゴコンセプト_01.png"
    img.convert("RGB").save(path, quality=96, dpi=(150, 150))
    return path


def page2():
    img = page_base()
    d = ImageDraw.Draw(img)
    ink = "#101113"
    gray = "#666a70"
    lime = "#d8ff42"

    d.rectangle((0, 0, W, 22), fill=lime)
    d.text((M, 70), "WEAR APPLICATION / 02", font=f(25), fill=gray)
    d.text((M, 118), "JUMPER  FRONT / BACK", font=f(58), fill=ink)
    d.text((M, 202), "AITOZ 2663  裏メッシュカラーブルゾン  /  010 BLACK  /  LL", font=f(23), fill=gray)

    photo_path = ROOT / "上田瓦商店" / "ロゴ案" / "u-brace-v1" / "上田瓦商店_撥水ワークジャンパー_前後イメージ_v1.png"
    jacket = Image.open(photo_path).convert("RGB")
    # Neutralise the navy cast to show the supplied 010 BLACK body direction.
    jacket = ImageOps.grayscale(jacket).convert("RGB")
    jacket = ImageEnhance.Contrast(jacket).enhance(1.08)
    jacket = ImageEnhance.Brightness(jacket).enhance(0.94)
    photo_box = (M, 290, W - M, 1020)
    d.rounded_rectangle(photo_box, radius=10, fill="#dededa")
    cover(img, jacket.convert("RGBA"), (M + 8, 298, W - M - 8, 1012), contain=True)
    d.rounded_rectangle((M + 26, 318, M + 148, 365), radius=4, fill=ink)
    d.text((M + 50, 326), "FRONT", font=f(18), fill="white")
    d.rounded_rectangle((W - M - 160, 318, W - M - 26, 365), radius=4, fill=ink)
    d.text((W - M - 134, 326), "BACK", font=f(18), fill="white")

    left = (M, 1085, 600, 1505)
    right = (640, 1085, W - M, 1505)
    for box in (left, right):
        d.rounded_rectangle(box, radius=8, fill="#ffffff", outline="#d5d5d1", width=2)
    d.rectangle((left[0], left[1], left[0] + 12, left[3]), fill=lime)
    d.rectangle((right[0], right[1], right[0] + 12, right[3]), fill=lime)

    d.text((left[0] + 36, left[1] + 32), "FRONT / LEFT CHEST", font=f(23), fill=gray)
    d.text((left[0] + 36, left[1] + 84), "U-BRACE + UEDA", font=f(34), fill=ink)
    d.text((left[0] + 36, left[1] + 139), "㈲上田瓦商店", font=f(30), fill=ink)
    d.multiline_text((left[0] + 36, left[1] + 215), "胸元で判読できる\nコンパクトな1色ロゴ。", font=f(23), fill=ink, spacing=12)

    d.text((right[0] + 36, right[1] + 32), "BACK / LOWER", font=f(23), fill=gray)
    d.text((right[0] + 36, right[1] + 84), "K A W A R A", font=f(37), fill=ink)
    d.multiline_text((right[0] + 36, right[1] + 162), "既存のRVCA調書体を継承。\n背面はKAWARAのみ。", font=f(23), fill=ink, spacing=12)

    d.text((M, 1570), "PRINT : 1 COLOR / WHITE / SILK SCREEN", font=f(20), fill=gray)
    note = "※ロゴの大きさ・位置・製品色はイメージです。実物採寸と試刷り後に最終調整します。"
    d.text((M, 1618), note, font=fit_text(d, note, W - 2 * M, 20), fill=gray)
    d.text((M, 1668), "㈲上田瓦商店  /  WORK JUMPER APPLICATION", font=f(19), fill=gray)
    d.text((W - M - 125, 1668), "2026.10", font=f(19), fill=gray)
    path = OUT / "上田瓦商店_ジャンパー前後_02.png"
    img.convert("RGB").save(path, quality=96, dpi=(150, 150))
    return path


if __name__ == "__main__":
    print(page1())
    print(page2())
