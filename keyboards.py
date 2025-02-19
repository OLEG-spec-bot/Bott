from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


moderate = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Далее", callback_data="next_moderate")], [InlineKeyboardButton(text="Назад", callback_data="previous_moderate")], 
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ]
)


next = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Далее", callback_data="next")], [InlineKeyboardButton(text="Назад", callback_data="previous")]
    ]
)

add_to_favorites_or_skip = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text="Добавить в избранное", callback_data="add_to_favorites")],
        [InlineKeyboardButton(text="Следующий вариант", callback_data="skip")],
        [InlineKeyboardButton(text="Назад", callback_data="previous_result")]
    ]
)

contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Отправить контакт", request_contact=True)],
    ],
    resize_keyboard=True
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗝️ Сдать квартиру"), KeyboardButton(text="🏠 Найти квартиру")],
        [KeyboardButton(text="📎 О Нас"), KeyboardButton(text="👤 Личный кабинет")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт в меню"
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Назад в главное меню")]
    ],
    resize_keyboard=True
)


type = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Квартира")], [KeyboardButton(text="Дом")] , [KeyboardButton(text="Комната")],
                            [KeyboardButton(text="🔙 Назад в главное меню")]
    ], resize_keyboard=True
)
confirm_or_edit = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Подтвердить")], [KeyboardButton(text="Изменить")]
    ], resize_keyboard=True
)


add_more_photos_or_finish = ReplyKeyboardMarkup(
    keyboard=[
         [KeyboardButton(text="Подтвердить")]
    ], resize_keyboard=True
)


ads = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📢 Мои Объявления")],[KeyboardButton(text="⭐ Избранное")],
        [KeyboardButton(text="📝 Зарегистрироваться")], [KeyboardButton(text="🔙 Назад в главное меню")]
    ],
    resize_keyboard=True
)

Town2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ташкент"), KeyboardButton(text="Самарканд")],
        [KeyboardButton(text="🔙 Назад в главное меню")]
    ],
    resize_keyboard=True
)

tdists1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Алмазарский район"), KeyboardButton(text="Бектемирский район")],
        [KeyboardButton(text="Мирабадский район"), KeyboardButton(text="Мирзо-Улугбекский район")],
        [KeyboardButton(text="Сергелийский район"), KeyboardButton(text="Чиланзарский район")],
        [KeyboardButton(text="Шайхантахурский район"), KeyboardButton(text="Юнусабадский район")],
        [KeyboardButton(text="Яккасарайский район"), KeyboardButton(text="Яшнабадский район")],
        [KeyboardButton(text="Учтепинский район"), KeyboardButton(text="Кибрайский район")],
                    [KeyboardButton(text="🔙 Назад в главное меню")]
    ],
    resize_keyboard=True
)

sdists1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Акадарьинский район"), KeyboardButton(text="Булунгурский район")],
        [KeyboardButton(text="Джамбайский район"), KeyboardButton(text="Иштыханский район")],
        [KeyboardButton(text="Каттакурганский район"), KeyboardButton(text="Кошрабадский район")],
        [KeyboardButton(text="Нарпайский район"), KeyboardButton(text="Нурабадский район")],
        [KeyboardButton(text="Пайарыкский район"), KeyboardButton(text="Пастдаргомский район")],
        [KeyboardButton(text="Пахтачийский район"), KeyboardButton(text="Самаркандский район")],
        [KeyboardButton(text="Тайлякский район"), KeyboardButton(text="Ургутский район")],
                    [KeyboardButton(text="🔙 Назад в главное меню")]
    ],
    resize_keyboard=True
)


tdists2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Алмазарский район"), KeyboardButton(text="Бектемирский район")],
        [KeyboardButton(text="Мирабадский район"), KeyboardButton(text="Мирзо-Улугбекский район")],
        [KeyboardButton(text="Сергелийский район"), KeyboardButton(text="Чиланзарский район")],
        [KeyboardButton(text="Шайхантахурский район"), KeyboardButton(text="Юнусабадский район")],
        [KeyboardButton(text="Яккасарайский район"), KeyboardButton(text="Яшнабадский район")],
        [KeyboardButton(text="Учтепинский район"), KeyboardButton(text="Кибрайский район")],
                            [KeyboardButton(text="Любой район")], 
                    [KeyboardButton(text="🔙 Назад в главное меню")]
    ],
    resize_keyboard=True
)

sdists2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Акадарьинский район"), KeyboardButton(text="Булунгурский район")],
        [KeyboardButton(text="Джамбайский район"), KeyboardButton(text="Иштыханский район")],
        [KeyboardButton(text="Каттакурганский район"), KeyboardButton(text="Кошрабадский район")],
        [KeyboardButton(text="Нарпайский район"), KeyboardButton(text="Нурабадский район")],
        [KeyboardButton(text="Пайарыкский район"), KeyboardButton(text="Пастдаргомский район")],
        [KeyboardButton(text="Пахтачийский район"), KeyboardButton(text="Самаркандский район")],
        [KeyboardButton(text="Тайлякский район"), KeyboardButton(text="Ургутский район")],
                            [KeyboardButton(text="Любой район")],
                    [KeyboardButton(text="🔙 Назад в главное меню")]
    ],
    resize_keyboard=True
)
