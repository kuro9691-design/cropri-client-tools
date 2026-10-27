from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "上田瓦商店" / "ロゴ案" / "u-brace-v2"
FONT_PATH = Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf")
COMPANY = "㈲上田瓦商店"


def load_font(weight=900):
    font = TTFont(FONT_PATH)
    return instantiateVariableFont(font, {"wght": weight}, inplace=False)


def outlined_text(font, text, x, baseline, size, tracking=0, fill="#111111"):
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"].metrics
    units = font["head"].unitsPerEm
    scale = size / units
    cursor = 0.0
    parts = []
    for char in text:
        glyph_name = cmap[ord(char)]
        pen = SVGPathPen(glyph_set)
        glyph_set[glyph_name].draw(pen)
        path = pen.getCommands()
        parts.append(
            f'<path d="{path}" transform="translate({x + cursor * scale:.3f} {baseline:.3f}) '
            f'scale({scale:.6f} {-scale:.6f})" fill="{fill}"/>'
        )
        cursor += hmtx[glyph_name][0] + tracking / scale
    return "\n".join(parts), cursor * scale


def ubrace(x, y, scale=1.0, fill="#111111"):
    # Heavy structural U with chamfered inner/outer corners and a single base notch.
    d = (
        "M0 0 H72 V168 L102 198 H178 L208 168 V0 H280 V202 "
        "L222 260 H162 V224 H118 V260 H58 L0 202 Z"
    )
    return f'<path d="{d}" transform="translate({x} {y}) scale({scale})" fill="{fill}"/>'


def ueda_wordmark(x, y, scale=1.0, fill="#111111"):
    # Custom angular wordmark. The A inherits the open-chevron rhythm of the legacy KAWARA mark.
    paths = [
        # U
        "M0 0 H34 V105 L48 119 H82 L96 105 V0 H130 V116 L96 150 H34 L0 116 Z",
        # E
        "M158 0 H278 V30 H192 V57 H265 V87 H192 V120 H278 V150 H158 Z",
        # D, even-odd inner counter
        "M306 0 H391 L432 41 V109 L391 150 H306 Z M340 31 V119 H377 L398 98 V52 L377 31 Z",
        # A, open chevron with a strong crossbar
        "M433 150 L485 0 H526 L578 150 H542 L529 111 H482 L469 150 Z "
        "M492 82 H519 L505 40 Z",
    ]
    return "\n".join(
        f'<path d="{d}" transform="translate({x} {y}) scale({scale})" fill="{fill}" fill-rule="evenodd"/>'
        for d in paths
    )


def make_primary(font):
    jp, _ = outlined_text(font, COMPANY, 390, 456, 82, tracking=2)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="500" viewBox="0 0 1500 500">
  <title>㈲上田瓦商店 U-BRACE primary logo v2</title>
  <g id="mark">{ubrace(55, 90, 1.12)}</g>
  <g id="ueda-wordmark">{ueda_wordmark(390, 118, 1.42)}</g>
  <g id="company-name">{jp}</g>
</svg>'''


def make_compact(font):
    jp, width = outlined_text(font, COMPANY, 0, 675, 72, tracking=1)
    jp_x = (700 - width) / 2
    jp, _ = outlined_text(font, COMPANY, jp_x, 675, 72, tracking=1)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="740" viewBox="0 0 700 740">
  <title>㈲上田瓦商店 U-BRACE compact logo v2</title>
  <g id="mark">{ubrace(210, 48, 1.0)}</g>
  <g id="ueda-wordmark">{ueda_wordmark(80, 365, 0.90)}</g>
  <g id="company-name">{jp}</g>
</svg>'''


def make_board(font):
    jp_main, _ = outlined_text(font, COMPANY, 520, 598, 80, tracking=2)
    jp_small, width = outlined_text(font, COMPANY, 0, 976, 40, tracking=1)
    jp_small_x = 1300 + (500 - width) / 2
    jp_small, _ = outlined_text(font, COMPANY, jp_small_x, 976, 40, tracking=1)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1000" viewBox="0 0 2000 1000">
  <rect width="2000" height="1000" fill="#f7f7f4"/>
  <text x="90" y="90" font-family="Arial, sans-serif" font-size="24" letter-spacing="8" fill="#555">UEDA KAWARA SHOTEN / U-BRACE V1</text>
  <text x="90" y="136" font-family="Arial, sans-serif" font-size="17" letter-spacing="3" fill="#777">PRIMARY HORIZONTAL LOCKUP</text>
  <g id="primary">
    {ubrace(105, 235, 1.30)}
    {ueda_wordmark(520, 220, 1.76)}
    {jp_main}
  </g>
  <line x1="90" y1="620" x2="1910" y2="620" stroke="#c9c9c5" stroke-width="2"/>
  <text x="90" y="690" font-family="Arial, sans-serif" font-size="17" letter-spacing="3" fill="#777">COMPACT WORKWEAR LOCKUP</text>
  <g id="compact">
    {ubrace(1335, 675, 0.48)}
    {ueda_wordmark(1250, 845, 0.84)}
    {jp_small}
  </g>
  <g id="design-notes" font-family="Arial, 'Noto Sans JP', sans-serif" fill="#333">
    <text x="90" y="770" font-size="28" font-weight="700">HERITAGE → MODERN WORK</text>
    <text x="90" y="818" font-size="21">Legacy KAWARAの鋭いAと広い字間を、UEDAの面取りと開いたAへ継承。</text>
    <text x="90" y="858" font-size="21">鬼瓦の細密画・筆文字は外し、胸でも背中でも潰れにくい太い1色構成。</text>
    <text x="90" y="898" font-size="21">用途：撥水アウター用DTF / 黒または白の1色。会社名はアウトライン済み。</text>
  </g>
</svg>'''


def pil_font(size):
    font = ImageFont.truetype(str(FONT_PATH), size=size)
    try:
        font.set_variation_by_axes([900])
    except (AttributeError, OSError):
        pass
    return font


def draw_ubrace(draw, x, y, scale, fill=(17, 17, 17, 255)):
    points = [
        (0, 0), (72, 0), (72, 168), (102, 198), (178, 198),
        (208, 168), (208, 0), (280, 0), (280, 202), (222, 260),
        (162, 260), (162, 224), (118, 224), (118, 260), (58, 260),
        (0, 202),
    ]
    draw.polygon([(x + px * scale, y + py * scale) for px, py in points], fill=fill)


def draw_ueda(draw, x, y, scale, fill=(17, 17, 17, 255), bg=(255, 255, 255, 0)):
    u = [(0, 0), (34, 0), (34, 105), (48, 119), (82, 119), (96, 105),
         (96, 0), (130, 0), (130, 116), (96, 150), (34, 150), (0, 116)]
    e = [(158, 0), (278, 0), (278, 30), (192, 30), (192, 57), (265, 57),
         (265, 87), (192, 87), (192, 120), (278, 120), (278, 150), (158, 150)]
    d = [(306, 0), (391, 0), (432, 41), (432, 109), (391, 150), (306, 150)]
    d_hole = [(340, 31), (377, 31), (398, 52), (398, 98), (377, 119), (340, 119)]
    a = [(433, 150), (485, 0), (526, 0), (578, 150), (542, 150), (529, 111),
         (482, 111), (469, 150)]
    a_hole = [(492, 82), (519, 82), (505, 40)]
    def poly(points, color):
        draw.polygon([(x + px * scale, y + py * scale) for px, py in points], fill=color)
    for shape in (u, e, d, a):
        poly(shape, fill)
    poly(d_hole, bg)
    poly(a_hole, bg)


def render_pngs():
    black = (17, 17, 17, 255)

    primary = Image.new("RGBA", (1500, 500), (255, 255, 255, 0))
    d = ImageDraw.Draw(primary)
    draw_ubrace(d, 55, 90, 1.12, black)
    draw_ueda(d, 390, 118, 1.42, black, (255, 255, 255, 0))
    d.text((390, 355), COMPANY, font=pil_font(82), fill=black)
    primary.save(OUT / "上田瓦商店_U-BRACE_primary_v2.png")

    compact = Image.new("RGBA", (700, 740), (255, 255, 255, 0))
    d = ImageDraw.Draw(compact)
    draw_ubrace(d, 210, 48, 1.0, black)
    draw_ueda(d, 80, 365, 0.90, black, (255, 255, 255, 0))
    f = pil_font(72)
    box = d.textbbox((0, 0), COMPANY, font=f)
    d.text(((700 - (box[2] - box[0])) / 2, 590), COMPANY, font=f, fill=black)
    compact.save(OUT / "上田瓦商店_U-BRACE_compact_v2.png")

    board = Image.new("RGB", (2000, 1000), (247, 247, 244))
    d = ImageDraw.Draw(board)
    latin = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 24)
    latin_small = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
    d.text((90, 58), "UEDA KAWARA SHOTEN / U-BRACE V2", font=latin, fill=(70, 70, 70))
    d.text((90, 110), "PRIMARY HORIZONTAL LOCKUP", font=latin_small, fill=(100, 100, 100))
    draw_ubrace(d, 105, 235, 1.30, black)
    draw_ueda(d, 520, 220, 1.76, black, (247, 247, 244))
    d.text((520, 500), COMPANY, font=pil_font(80), fill=black)
    d.line((90, 620, 1910, 620), fill=(201, 201, 197), width=2)
    d.text((90, 670), "COMPACT WORKWEAR LOCKUP", font=latin_small, fill=(100, 100, 100))
    draw_ubrace(d, 1430, 650, 0.48, black)
    draw_ueda(d, 1270, 800, 0.84, black, (247, 247, 244))
    jf = pil_font(40)
    box = d.textbbox((0, 0), COMPANY, font=jf)
    d.text((1500 - (box[2] - box[0]) / 2, 948), COMPANY, font=jf, fill=black)
    note_bold = pil_font(30)
    note = pil_font(23)
    d.text((90, 750), "HERITAGE → MODERN WORK", font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 30), fill=(45, 45, 45))
    d.text((90, 810), "旧KAWARAの鋭いAと広い字間を、UEDAの面取りと開いたAへ継承。", font=note, fill=(55, 55, 55))
    d.text((90, 855), "鬼瓦の細密画・筆文字は外し、胸でも背中でも潰れにくい太い1色構成。", font=note, fill=(55, 55, 55))
    d.text((90, 900), "用途：撥水アウター用DTF／黒または白の1色。会社名はアウトライン済み。", font=note, fill=(55, 55, 55))
    board.save(OUT / "上田瓦商店_U-BRACE_concept-board_v2.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    font = load_font()
    files = {
        "上田瓦商店_U-BRACE_primary_v2.svg": make_primary(font),
        "上田瓦商店_U-BRACE_compact_v2.svg": make_compact(font),
        "上田瓦商店_U-BRACE_concept-board_v2.svg": make_board(font),
    }
    for name, source in files.items():
        path = OUT / name
        path.write_text(source, encoding="utf-8")
        print(path)
    render_pngs()


if __name__ == "__main__":
    main()
