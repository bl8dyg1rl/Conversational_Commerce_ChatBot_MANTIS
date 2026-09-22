from app.core.config import settings


print(
    "Token cargado:",
    bool(settings.telegram_bot_token)
)