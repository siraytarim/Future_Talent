from certificate import generate_certificate


def main():
    name = input("Ad (İsim Soyisim): ").strip()
    title = input("Etkinlik başlığı: ").strip()
    date = input("Tarih (örn. 23.03.2026): ").strip()

    if not name or not title or not date:
        print("Hata: Ad, başlık ve tarih boş olamaz.")
        return

    pdf_path = generate_certificate(
        name=name,
        title=title,
        date=date,
        output_path=f"sertifika_{name}.pdf",
    )
    print(pdf_path)


if __name__ == "__main__":
    main()

