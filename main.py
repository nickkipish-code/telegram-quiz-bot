#!/usr/bin/env python3
"""
Telegram Quiz Bot - Main entry point
"""

import asyncio
import logging
from aiogram_bot import main

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot crashed with error: {e}")