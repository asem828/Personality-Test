"""Lightweight i18n helpers.

The app supports 2 languages:
 - Indonesian (id) [default]
 - English (en)

Instead of relying solely on Qt's QTranslator (.qm), we keep i18n explicit
and deterministic: call :func:`t` with (id_text, en_text) and we pick the
right one based on current settings.

Qt translation files are still supported (optional): if you compile
`characterify/assets/i18n/characterify_en.ts` into a `.qm` file,
`SettingsService.apply_language()` will load it. This is useful if you want
to translate via Qt Linguist.
"""

from __future__ import annotations

from typing import Optional


def get_lang(ctx) -> str:
    """Return current language code ('id' or 'en')."""
    try:
        return str(ctx.settings.get_language(getattr(ctx, "current_user_id", None)))
    except Exception:
        return "id"


def t(ctx, id_text: str, en_text: Optional[str] = None) -> str:
    """Translate helper.

    Args:
        ctx: AppContext
        id_text: Indonesian text (source)
        en_text: English text

    Returns:
        The text in the active language. If `en_text` is not provided, we
        fall back to `id_text`.
    """

    lang = get_lang(ctx)
    if lang == "en" and en_text is not None:
        return en_text
    return id_text
