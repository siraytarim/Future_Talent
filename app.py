import os
import uuid
from datetime import datetime

from flask import Flask, render_template, request, send_file

from certificate import generate_certificate


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", error=None)


@app.post("/generate")
def generate():
    name = (request.form.get("name") or "").strip()
    title = (request.form.get("title") or "").strip()
    date_str = (request.form.get("date") or "").strip()
    bg_color = (request.form.get("bg_color") or "#FFF8E7").strip()

    if not name or not title or not date_str:
        return render_template("index.html", error="Ad, başlık ve tarih zorunludur.")

    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        formatted_date = parsed_date.strftime("%d.%m.%Y")
    except ValueError:
        formatted_date = date_str 

    pdf_path = generate_certificate(
        name=name,
        title=title,
        date=formatted_date,
        output_path=f"sertifika_{uuid.uuid4().hex}.pdf",
        bg_color=bg_color,
    )

    filename = os.path.basename(pdf_path)
    return send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)

