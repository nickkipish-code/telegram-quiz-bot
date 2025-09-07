import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import TELEGRAM_BOT_TOKEN, ADMIN_USERNAMES, bot_settings, WELCOME_MESSAGE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# FSM States for admin panel
class AdminStates(StatesGroup):
    waiting_for_card = State()
    waiting_for_game_link = State()
    waiting_for_calendar_link = State()
    waiting_for_chat_link = State()
    waiting_for_moderator_link = State()
    waiting_for_charity_link = State()
    waiting_for_charity_description = State()

def get_main_menu_keyboard():
    """Create main menu keyboard with 6 buttons in 2 columns"""
    builder = ReplyKeyboardBuilder()
    
    # Row 1
    builder.add(KeyboardButton(text="🎯 Забронювати участь у квізі"))
    builder.add(KeyboardButton(text="🎮 Найближча гра"))
    
    # Row 2
    builder.add(KeyboardButton(text="📅 Календар на місяць"))
    builder.add(KeyboardButton(text="💬 Загальний чат"))
    
    # Row 3
    builder.add(KeyboardButton(text="❓ Питання до модератора"))
    builder.add(KeyboardButton(text="❤️ Благодійність"))
    
    builder.adjust(2, 2, 2)  # 2 buttons per row
    return builder.as_markup(resize_keyboard=True)

def get_admin_menu_keyboard():
    """Create admin menu keyboard"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(text="💳 Змінити номер картки", callback_data="admin_card"))
    builder.add(InlineKeyboardButton(text="🎮 Змінити посилання на гру", callback_data="admin_game"))
    builder.add(InlineKeyboardButton(text="📅 Змінити календар", callback_data="admin_calendar"))
    builder.add(InlineKeyboardButton(text="💬 Змінити загальний чат", callback_data="admin_chat"))
    builder.add(InlineKeyboardButton(text="❓ Змінити модератора", callback_data="admin_moderator"))
    builder.add(InlineKeyboardButton(text="❤️ Налаштувати благодійність", callback_data="admin_charity"))
    builder.add(InlineKeyboardButton(text="📊 Переглянути налаштування", callback_data="admin_view"))
    builder.add(InlineKeyboardButton(text="🔙 Назад до головного меню", callback_data="admin_back"))
    
    builder.adjust(1)
    return builder.as_markup()

def is_admin(username: str) -> bool:
    """Check if user is admin"""
    return username in ADMIN_USERNAMES

async def delete_and_send_message(message: types.Message, text: str, reply_markup=None):
    """Delete current message and send new one"""
    try:
        await message.delete()
    except:
        pass
    return await message.answer(text, reply_markup=reply_markup)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command"""
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=get_main_menu_keyboard()
    )

@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Handle /admin command - only for authorized users"""
    if not message.from_user or not message.from_user.username or not is_admin(message.from_user.username):
        await message.answer("❌ У вас немає доступу до адміністративної панелі.")
        return
    
    await message.answer(
        "🔧 Адміністративна панель\n\nОберіть дію:",
        reply_markup=get_admin_menu_keyboard()
    )

# Main menu handlers
@dp.message(F.text == "🎯 Забронювати участь у квізі")
async def book_quiz_participation(message: types.Message):
    """Handle booking quiz participation"""
    text = f"💳 Для бронювання участі у квізі переведіть кошти на картку:\n\n<code>{bot_settings.payment_card}</code>\n\n💡 Після оплати зв'яжіться з модератором для підтвердження."
    await delete_and_send_message(message, text, get_main_menu_keyboard())

@dp.message(F.text == "🎮 Найближча гра")
async def next_game_info(message: types.Message):
    """Handle next game info"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🎮 Перейти до інформації", url=bot_settings.next_game_link))
    
    text = "🎮 Інформація про найближчу гру доступна за посиланням нижче:"
    await delete_and_send_message(message, text, builder.as_markup())

@dp.message(F.text == "📅 Календар на місяць")
async def monthly_calendar(message: types.Message):
    """Handle monthly calendar"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📅 Переглянути календар", url=bot_settings.calendar_link))
    
    text = "📅 Календар ігор на місяць:"
    await delete_and_send_message(message, text, builder.as_markup())

@dp.message(F.text == "💬 Загальний чат")
async def general_chat(message: types.Message):
    """Handle general chat"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="💬 Приєднатися до чату", url=bot_settings.general_chat_link))
    
    text = "💬 Приєднуйтесь до нашого загального чату:"
    await delete_and_send_message(message, text, builder.as_markup())

@dp.message(F.text == "❓ Питання до модератора")
async def moderator_questions(message: types.Message):
    """Handle moderator questions"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❓ Написати модератору", url=bot_settings.moderator_link))
    
    text = "❓ Якщо у вас є питання, зв'яжіться з модератором:"
    await delete_and_send_message(message, text, builder.as_markup())

@dp.message(F.text == "❤️ Благодійність")
async def charity_info(message: types.Message):
    """Handle charity info"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❤️ Підтримати", url=bot_settings.charity_link))
    
    text = "❤️ Сбор на генераторы для вч а4699"
    await delete_and_send_message(message, text, builder.as_markup())

# Admin panel callback handlers
@dp.callback_query(F.data == "admin_back")
async def admin_back_to_main(callback: types.CallbackQuery):
    """Return to main menu from admin panel"""
    if callback.message and hasattr(callback.message, 'edit_text'):
        await callback.message.edit_text(
            WELCOME_MESSAGE,
            reply_markup=None
        )
        await callback.message.answer("Головне меню:", reply_markup=get_main_menu_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "admin_view")
async def admin_view_settings(callback: types.CallbackQuery):
    """View all current settings"""
    settings = bot_settings.get_all_settings()
    
    text = "📊 Поточні налаштування:\n\n"
    text += f"💳 Номер картки: <code>{settings['payment_card']}</code>\n"
    text += f"🎮 Наступна гра: {settings['next_game_link']}\n"
    text += f"📅 Календар: {settings['calendar_link']}\n"
    text += f"💬 Загальний чат: {settings['general_chat_link']}\n"
    text += f"❓ Модератор: {settings['moderator_link']}\n"
    text += f"❤️ Благодійність: {settings['charity_link']}\n"
    text += f"📝 Опис благодійності: {settings['charity_description']}"
    
    if callback.message and hasattr(callback.message, 'edit_text'):
        await callback.message.edit_text(text, reply_markup=get_admin_menu_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "admin_card")
async def admin_change_card(callback: types.CallbackQuery, state: FSMContext):
    """Start changing payment card"""
    await state.set_state(AdminStates.waiting_for_card)
    if callback.message and hasattr(callback.message, 'edit_text'):
        await callback.message.edit_text(
            f"💳 Поточний номер картки: <code>{bot_settings.payment_card}</code>\n\nВведіть новий номер картки:",
            reply_markup=None
        )
    await callback.answer()

@dp.callback_query(F.data == "admin_game")
async def admin_change_game(callback: types.CallbackQuery, state: FSMContext):
    """Start changing game link"""
    await state.set_state(AdminStates.waiting_for_game_link)
    if callback.message and hasattr(callback.message, 'edit_text'):
        await callback.message.edit_text(
            f"🎮 Поточне посилання на гру: {bot_settings.next_game_link}\n\nВведіть нове посилання:",
            reply_markup=None
        )
    await callback.answer()

@dp.callback_query(F.data == "admin_calendar")
async def admin_change_calendar(callback: types.CallbackQuery, state: FSMContext):
    """Start changing calendar link"""
    await state.set_state(AdminStates.waiting_for_calendar_link)
    if callback.message and hasattr(callback.message, 'edit_text'):
        await callback.message.edit_text(
            f"📅 Поточне посилання на календар: {bot_settings.calendar_link}\n\nВведіть нове посилання:",
            reply_markup=None
        )
    await callback.answer()

@dp.callback_query(F.data == "admin_chat")
async def admin_change_chat(callback: types.CallbackQuery, state: FSMContext):
    """Start changing chat link"""
    await state.set_state(AdminStates.waiting_for_chat_link)
    if callback.message and hasattr(callback.message, 'edit_text'):
        await callback.message.edit_text(
            f"💬 Поточне посилання на чат: {bot_settings.general_chat_link}\n\nВведіть нове посилання:",
            reply_markup=None
        )
    await callback.answer()

@dp.callback_query(F.data == "admin_moderator")
async def admin_change_moderator(callback: types.CallbackQuery, state: FSMContext):
    """Start changing moderator link"""
    await state.set_state(AdminStates.waiting_for_moderator_link)
    if callback.message and hasattr(callback.message, 'edit_text'):
        await callback.message.edit_text(
            f"❓ Поточне посилання на модератора: {bot_settings.moderator_link}\n\nВведіть нове посилання:",
            reply_markup=None
        )
    await callback.answer()

@dp.callback_query(F.data == "admin_charity")
async def admin_change_charity(callback: types.CallbackQuery, state: FSMContext):
    """Start changing charity settings"""
    await state.set_state(AdminStates.waiting_for_charity_link)
    if callback.message and hasattr(callback.message, 'edit_text'):
        await callback.message.edit_text(
            f"❤️ Поточне посилання на благодійність: {bot_settings.charity_link}\n\nВведіть нове посилання:",
            reply_markup=None
        )
    await callback.answer()

# State handlers for admin inputs
@dp.message(StateFilter(AdminStates.waiting_for_card))
async def process_card_input(message: types.Message, state: FSMContext):
    """Process new payment card input"""
    if message.text:
        bot_settings.payment_card = message.text.strip()
        await state.clear()
        await message.answer(
            f"✅ Номер картки оновлено: <code>{bot_settings.payment_card}</code>",
            reply_markup=get_admin_menu_keyboard()
        )

@dp.message(StateFilter(AdminStates.waiting_for_game_link))
async def process_game_link_input(message: types.Message, state: FSMContext):
    """Process new game link input"""
    if message.text:
        bot_settings.next_game_link = message.text.strip()
        await state.clear()
        await message.answer(
            f"✅ Посилання на гру оновлено: {bot_settings.next_game_link}",
            reply_markup=get_admin_menu_keyboard()
        )

@dp.message(StateFilter(AdminStates.waiting_for_calendar_link))
async def process_calendar_link_input(message: types.Message, state: FSMContext):
    """Process new calendar link input"""
    if message.text:
        bot_settings.calendar_link = message.text.strip()
        await state.clear()
        await message.answer(
            f"✅ Посилання на календар оновлено: {bot_settings.calendar_link}",
            reply_markup=get_admin_menu_keyboard()
        )

@dp.message(StateFilter(AdminStates.waiting_for_chat_link))
async def process_chat_link_input(message: types.Message, state: FSMContext):
    """Process new chat link input"""
    if message.text:
        bot_settings.general_chat_link = message.text.strip()
        await state.clear()
        await message.answer(
            f"✅ Посилання на чат оновлено: {bot_settings.general_chat_link}",
            reply_markup=get_admin_menu_keyboard()
        )

@dp.message(StateFilter(AdminStates.waiting_for_moderator_link))
async def process_moderator_link_input(message: types.Message, state: FSMContext):
    """Process new moderator link input"""
    if message.text:
        bot_settings.moderator_link = message.text.strip()
        await state.clear()
        await message.answer(
            f"✅ Посилання на модератора оновлено: {bot_settings.moderator_link}",
            reply_markup=get_admin_menu_keyboard()
        )

@dp.message(StateFilter(AdminStates.waiting_for_charity_link))
async def process_charity_link_input(message: types.Message, state: FSMContext):
    """Process new charity link input"""
    if message.text:
        bot_settings.charity_link = message.text.strip()
        await state.set_state(AdminStates.waiting_for_charity_description)
        await message.answer(
            f"✅ Посилання на благодійність оновлено: {bot_settings.charity_link}\n\nТепер введіть опис благодійності:"
        )

@dp.message(StateFilter(AdminStates.waiting_for_charity_description))
async def process_charity_description_input(message: types.Message, state: FSMContext):
    """Process new charity description input"""
    if message.text:
        bot_settings.charity_description = message.text.strip()
        await state.clear()
        await message.answer(
            f"✅ Опис благодійності оновлено: {bot_settings.charity_description}",
            reply_markup=get_admin_menu_keyboard()
        )

async def main():
    """Main function to start the bot"""
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())