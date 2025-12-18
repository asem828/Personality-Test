# Characterify Desktop (PySide6)

Aplikasi desktop **Characterify** untuk tes kepribadian dengan UI/UX modern yang meniru struktur Spotify:
**sidebar navigasi**, **topbar**, **content area**, dan **status bar**.

Tema default: **Dark** dengan warna utama **Spotify Green** `#1DB954`.

---

## Fitur Utama

### 1) Auth & Dashboard
- Login / Register / Logout
- Validasi input (format email, password minimal 8 karakter + huruf & angka)
- Dashboard profil:
  - Nama, email, tanggal join
  - Riwayat tes (tanggal, jenis tes, hasil)
  - Aksi: lihat detail hasil, hapus history, export PDF
- Saved Session:
  - Simpan progress tes dan lanjutkan nanti dari Dashboard

### 2) Test Module (4 Tes)
- MBTI (Myers-Briggs Type Indicator)
- Big Five (OCEAN)
- Enneagram
- 4 Temperaments (Sanguine, Choleric, Phlegmatic, Melancholic)

**Flow**:
Test List → Intro/Petunjuk → Start → (5 pertanyaan per halaman + progress) → Result Page

### 3) Result Page
- Chart hasil (Matplotlib embedded)
- Ringkasan + deskripsi terstruktur
- Saran pengembangan diri:
  - Kekuatan utama
  - Tantangan umum
  - Saran komunikasi
  - Saran kerja tim/karier
  - Rutinitas pengembangan diri (actionable)
- Export PDF (ReportLab)

### 4) Learn Module
- 25 artikel edukasi (search + filter kategori)
- Article reader + bookmark + mark as read

### 5) Help / FAQ & Information
- FAQ (accordion)
- Petunjuk penggunaan
- Disclaimer & privasi

### 6) Settings
- Theme: Dark / Light
- Language: ID / EN (struktur siap, bisa dikembangkan)
- Export history (JSON/CSV)
- Clear history / clear saved sessions
- Preferensi pengingat tes ulang (offline setting)

---

## Tech Stack
- Python 3.11+
- PySide6
- SQLite (built-in `sqlite3`)
- Matplotlib (chart)
- ReportLab (PDF)
- cryptography (enkripsi lokal untuk data sensitif / secret lokal)

---

## Instalasi & Menjalankan

```bash
# (opsional) buat virtual env
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

---

## Lokasi Data (Offline-first)

Aplikasi menyimpan data lokal di folder:

- **Windows**: `C:\Users\<user>\.characterify\`
- **Linux/macOS**: `~/.characterify/`

Struktur di dalamnya:
- `characterify.db` → database SQLite
- `logs/app.log` → log aplikasi
- `exports/` → hasil export PDF/JSON/CSV
- `key.key` → key enkripsi lokal (untuk field sensitif)

> Catatan: `key.key` adalah kunci enkripsi lokal untuk data sensitif. Jangan dibagikan.

---

## Struktur Folder

```
characterify_pyside6/
  main.py
  requirements.txt
  README.md
  characterify/
    __init__.py
    main.py
    app_context.py

    assets/
      images/branding.png
      qss/
        dark.qss
        light.qss

    data/
      mbti_questions.py
      ocean_questions.py
      enneagram_questions.py
      temperaments_questions.py
      articles.py

    db/
      database.py
      repositories.py

    services/
      auth.py
      history.py
      pdf_report.py
      scoring.py
      security.py
      settings.py
      telemetry.py

    ui/
      main_window.py
      pages/
        auth.py
        home.py
        test_flow.py
        result.py
        dashboard.py
        learn.py
        settings.py
        information.py
        help.py
        account_settings.py
      widgets/
        common.py
        sidebar.py
        topbar.py
        charts.py
        dialogs.py

    utils/
      paths.py
      validators.py
```

---

## Packaging (Opsional)

Aplikasi ini sudah siap dipaketkan dengan PyInstaller.

Contoh:
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed main.py
```

Jika ingin menyertakan asset (QSS/images), gunakan opsi `--add-data` sesuai OS.

---

## Catatan
- Tes kepribadian bukan diagnosis klinis.
- Semua data disimpan secara lokal (offline).
- Error/exception dicatat ke `logs/app.log` dan ditampilkan sebagai dialog error.

