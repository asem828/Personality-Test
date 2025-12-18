# i18n (Qt .ts/.qm)

Aplikasi ini sudah mendukung switching bahasa **ID/EN** lewat `Settings`.

- Secara default, teks UI memakai helper Python (`characterify/utils/i18n.py`) agar switching **langsung jalan** tanpa tool tambahan.
- Jika Anda ingin menggunakan mekanisme i18n native Qt (QTranslator), Anda bisa **compile** file `.ts` menjadi `.qm`.

## Compile `.ts` -> `.qm`

Pastikan PySide6 ter-install, lalu jalankan (di root project):

```bash
pyside6-lrelease characterify/assets/i18n/characterify_en.ts -qm characterify/assets/i18n/characterify_en.qm
```

Setelah file `.qm` ada, aplikasi akan otomatis memuatnya saat bahasa di-set ke `en`.
