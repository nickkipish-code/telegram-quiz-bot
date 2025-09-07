import os
from typing import Dict, Any

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7592605103:AAHLGJr7T9it8R8hhmghbRjpqjOmT7QuQOY")

# Admin usernames
ADMIN_USERNAMES = ["nickskinner", "Niko_Kipish"]

# Default bot settings (stored in memory - will reset on restart)
class BotSettings:
    def __init__(self):
        # Payment card number
        self.payment_card = "5375 4141 0123 4567"
        
        # Links
        self.next_game_link = "https://t.me/pubquiz_kharkov"
        self.calendar_link = "https://pubquiz.me/calendar"
        self.general_chat_link = "https://t.me/pubquiz_chat"
        self.moderator_link = "https://t.me/pubquiz_moderator"
        
        # Charity information
        self.charity_link = "https://send.monobank.ua/jar/4zaXBKwdSp"
        self.charity_description = "Сбор на генераторы для вч а4699"
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all current settings as a dictionary"""
        return {
            "payment_card": self.payment_card,
            "next_game_link": self.next_game_link,
            "calendar_link": self.calendar_link,
            "general_chat_link": self.general_chat_link,
            "moderator_link": self.moderator_link,
            "charity_link": self.charity_link,
            "charity_description": self.charity_description
        }

# Global settings instance
bot_settings = BotSettings()

# Welcome message
WELCOME_MESSAGE = "Ласкаво просимо до бота бронювання участі в квізі! ✅"