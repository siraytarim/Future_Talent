import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


_DEJAVU_SANS_NAME = "DejaVuSans"
_FONT_DIR = r"C:\Users\HP\Desktop\FT\dejavu-fonts-ttf-2.37\ttf"
_dejavu_path = None

for p in (
    r"C:\Users\HP\Desktop\FT\dejavu-fonts-ttf-2.37\ttf\DejaVuSans.ttf",
    r"C:\Users\HP\Desktop\FT\dejavu-fonts-ttf-2.37\ttf\DejaVuSans.ttf",
):
    if os.path.exists(p):
        _dejavu_path = p
        break

if not _dejavu_path and os.path.isdir(_FONT_DIR):
    for filename in os.listdir(_FONT_DIR):
        if not filename.lower().endswith(".ttf"):
            continue
        if "devajusans" in filename.lower().replace(" ", ""):
            _dejavu_path = os.path.join(_FONT_DIR, filename)
            break

if not _dejavu_path:
    raise FileNotFoundError(
        "DejaVuSans font dosyası bulunamadı; C:\Users\HP\Desktop\FT\dejavu-fonts-ttf-2.37\ttf içinde arandı. "
        "Türkçe karakterlerin doğru görünmesi için DejaVuSans.ttf yüklemen gerekir."
    )

pdfmetrics.registerFont(TTFont(_DEJAVU_SANS_NAME, _dejavu_path))


_DEJAVU_SANS_BOLD_NAME = "DejaVuSans-Bold"
_DEJAVU_SANS_ITALIC_NAME = "DejaVuSans-Oblique"

_bold_path = None
_italic_path = None

for filename in os.listdir(os.path.dirname(_dejavu_path)):
    lower = filename.lower()
    if lower == "dejavusans-bold.ttf" or "dejavusans-bold" in lower:
        _bold_path = os.path.join(os.path.dirname(_dejavu_path), filename)
    if (
        lower == "dejavusans-oblique.ttf"
        or lower == "dejavusans-italic.ttf"
        or "dejavusans-oblique" in lower
        or "dejavusans-italic" in lower
    ):
        _italic_path = os.path.join(os.path.dirname(_dejavu_path), filename)

def _try_register(font_name: str, font_path: str) -> bool:
    try:
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        return True
    except Exception:
        return False


if _bold_path and _try_register(_DEJAVU_SANS_BOLD_NAME, _bold_path):
    pass
else:
    _DEJAVU_SANS_BOLD_NAME = _DEJAVU_SANS_NAME

if _italic_path and _try_register(_DEJAVU_SANS_ITALIC_NAME, _italic_path):
    pass
else:
    _DEJAVU_SANS_ITALIC_NAME = _DEJAVU_SANS_NAME


def generate_certificate(name, title, date, output_path, bg_color="#FFF8E7"):
    """
    name: kişi adı
    title: etkinlik başlığı
    date: tarih (str veya datetime/date)
    output_path: çıktı PDF dosya adı (örn. "sertifika.pdf") veya yol; yine de outputs/ içine yazılır
    bg_color: arka plan rengi (örn. "#FFF8E7")
    """

    out_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(out_dir, exist_ok=True)

    def _turkish_to_english(s: str) -> str:
        mapping = {
            "ş": "s",
            "Ş": "S",
            "ğ": "g",
            "Ğ": "G",
            "ü": "u",
            "Ü": "U",
            "ı": "i",
            "İ": "I",
            "ö": "o",
            "Ö": "O",
            "ç": "c",
            "Ç": "C",
        }
        return "".join(mapping.get(ch, ch) for ch in s)

    def _sanitize_filename_part(s: str) -> str:
        s = _turkish_to_english(str(s)).strip()
        s = re.sub(r"\s+", "_", s)
        s = re.sub(r"[<>:\"/\\|?*\x00-\x1F]", "_", s)
        s = re.sub(r"_+", "_", s)
        return s.strip("_")

    safe_name = _sanitize_filename_part(name)
    safe_title = _sanitize_filename_part(title)
    out_name = f"{safe_name}_{safe_title}.pdf"

    out_file = os.path.join(out_dir, out_name)

    if hasattr(date, "strftime"):
        date_str = date.strftime("%d.%m.%Y")
    else:
        date_str = str(date)

    page_w, page_h = landscape(A4)
    c = canvas.Canvas(out_file, pagesize=(page_w, page_h))

    c.setFillColor(colors.HexColor(bg_color))
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    margin = 40
    frame_x = margin
    frame_y = margin
    frame_w = page_w - 2 * margin
    frame_h = page_h - 2 * margin

    gold_dark = colors.HexColor("#B8860B")  
    gold_soft = colors.HexColor("#D4AF37") 

    outer_top_y = frame_y + frame_h
    outer_bottom_y = frame_y
    inner_top_y = outer_top_y - 8
    inner_bottom_y = outer_bottom_y + 8

    c.setStrokeColor(gold_dark)
    c.setLineWidth(4)
    c.line(frame_x, frame_y, frame_x, frame_y + frame_h)
    c.line(frame_x + frame_w, frame_y, frame_x + frame_w, frame_y + frame_h)

    c.setLineWidth(1)
    inner_left_x = frame_x + 8
    inner_right_x = frame_x + frame_w - 8
    c.line(inner_left_x, inner_top_y, inner_left_x, inner_bottom_y)
    c.line(inner_right_x, inner_top_y, inner_right_x, inner_bottom_y)

    top_thin_y = outer_top_y
    top_thick_y = outer_top_y - 4

    c.setStrokeColor(gold_dark)
    c.setLineWidth(1)
    c.line(frame_x, top_thin_y, frame_x + frame_w, top_thin_y)
    c.setLineWidth(4)
    c.line(frame_x, top_thick_y, frame_x + frame_w, top_thick_y)
    c.setLineWidth(1)
    c.line(frame_x, inner_top_y, frame_x + frame_w, inner_top_y)

    c.setLineWidth(4)
    c.line(frame_x, outer_bottom_y, frame_x + frame_w, outer_bottom_y)
    c.setLineWidth(1)
    c.line(frame_x, inner_bottom_y, frame_x + frame_w, inner_bottom_y)

    center_x = frame_x + frame_w / 2
    center_y = frame_y + frame_h / 2

    def fit_center(text, y, max_w, start_font, font_name, color, min_font=10):
        font_size = start_font
        width = pdfmetrics.stringWidth(text, font_name, font_size)
        while width > max_w and font_size > min_font:
            font_size -= 1
            width = pdfmetrics.stringWidth(text, font_name, font_size)
        c.setFont(font_name, font_size)
        c.setFillColor(color)
        c.drawCentredString(center_x, y, text)

    name_max_w = frame_w * 0.85
    fit_center(
        str(name),
        center_y + 45,
        name_max_w,
        start_font=44,
        font_name=_DEJAVU_SANS_BOLD_NAME,
        color=colors.HexColor("#1B2A6B"),
        min_font=18,
    )

    title_max_w = frame_w * 0.9
    title = str(title)
    c.setFont(_DEJAVU_SANS_ITALIC_NAME, 18)
    if pdfmetrics.stringWidth(title, _DEJAVU_SANS_ITALIC_NAME, 22) <= title_max_w:
        fit_center(
            title,
            center_y - 5,
            title_max_w,
            start_font=22,
            font_name=_DEJAVU_SANS_ITALIC_NAME,
            color=colors.HexColor("#8B0000"),
            min_font=12,
        )
        title_bottom_y = center_y - 5
    else:
        words = title.split()
        lines = []
        current = []
        for w in words:
            trial = " ".join(current + [w])
            if (
                pdfmetrics.stringWidth(trial, _DEJAVU_SANS_ITALIC_NAME, 18) <= title_max_w
                and len(lines) < 2
            ):
                current.append(w)
            else:
                if current:
                    lines.append(" ".join(current))
                current = [w]
                if len(lines) == 2:
                    break
        if current and len(lines) < 2:
            lines.append(" ".join(current))

        c.setFont(_DEJAVU_SANS_ITALIC_NAME, 18)
        if len(lines) == 1:
            c.setFillColor(colors.HexColor("#8B0000"))
            c.drawCentredString(center_x, center_y - 5, lines[0])
            title_bottom_y = center_y - 5
        else:
            c.setFillColor(colors.HexColor("#8B0000"))
            c.drawCentredString(center_x, center_y + 10, lines[0])
            c.drawCentredString(center_x, center_y - 18, lines[1])
            title_bottom_y = center_y - 18

    description = f"{title} eğitimini başarıyla tamamlayarak sertifika almaya hak kazanmıştır."
    c.setFont(_DEJAVU_SANS_ITALIC_NAME, 13)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawCentredString(center_x, title_bottom_y - 25, description)
    deco_line_y = center_y + 32
    deco_len = frame_w * 0.28
    c.setStrokeColor(gold_dark)
    c.setLineWidth(0.8)
    c.line(center_x - deco_len, deco_line_y, center_x + deco_len, deco_line_y)

    seal_center_y = frame_y + 70
    seal_r_outer = 28
    seal_r_inner = 18
    c.setStrokeColor(gold_dark)
    c.setLineWidth(2)
    c.circle(center_x, seal_center_y, seal_r_outer, stroke=1, fill=0)
    c.setLineWidth(1)
    c.circle(center_x, seal_center_y, seal_r_inner, stroke=1, fill=0)

    c.setFont(_DEJAVU_SANS_NAME, 12)
    c.setFillColor(colors.black)
    c.drawString(frame_x + 28, frame_y + 28, f"Tarih: {date_str}")

    sig_label_y = frame_y + 18
    sig_bar_y = frame_y + 32
    sig_bar_len = 210

    sig_end_x = frame_x + frame_w - 5
    sig_start_x = sig_end_x - sig_bar_len

    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(sig_start_x, sig_bar_y, sig_end_x, sig_bar_y)

    c.setFont(_DEJAVU_SANS_NAME, 11)
    c.drawCentredString((sig_start_x + sig_end_x) / 2, sig_label_y, "İmza")

    corner_offset = 12
    corner_len = 20
    c.setStrokeColor(gold_dark)
    c.setLineWidth(1.6)

    tl_x = frame_x + corner_offset
    tl_y = outer_top_y - corner_offset
    c.line(tl_x, tl_y, tl_x + corner_len, tl_y)         
    c.line(tl_x, tl_y, tl_x, tl_y - corner_len)  
   
    tr_x = frame_x + frame_w - corner_offset
    tr_y = outer_top_y - corner_offset
    c.line(tr_x, tr_y, tr_x - corner_len, tr_y)  
    c.line(tr_x, tr_y, tr_x, tr_y - corner_len)  

    bl_x = frame_x + corner_offset
    bl_y = outer_bottom_y + corner_offset
    c.line(bl_x, bl_y, bl_x + corner_len, bl_y) 
    c.line(bl_x, bl_y, bl_x, bl_y + corner_len) 

    br_x = frame_x + frame_w - corner_offset
    br_y = outer_bottom_y + corner_offset
    c.line(br_x, br_y, br_x - corner_len, br_y) 
    c.line(br_x, br_y, br_x, br_y + corner_len)  

    c.showPage()
    c.save()

    return out_file

