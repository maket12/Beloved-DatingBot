from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Кнопка создания анкеты

create_form_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='➕Создать анкету➕', callback_data='create_form')
    ]
])


# Кнопки прикрепления медиа на этапе создания анкеты

async def create_edit_media_markup(medias_amount: int):  # Если кол-во 3, выводим только одну кнопку
    edit_medias_markup = InlineKeyboardBuilder()
    buttons = []
    if medias_amount == 3:
        buttons.append(InlineKeyboardButton(text='Это всё✅', callback_data='complete_add_media'))
    else:
        buttons.append(InlineKeyboardButton(text='Добавить фото', callback_data='create_form_add_photo'))
        buttons.append(InlineKeyboardButton(text='Добавить видео', callback_data='create_form_add_video'))
        buttons.append(InlineKeyboardButton(text='Это всё✅', callback_data='complete_add_media'))
    edit_medias_markup.add(*buttons)
    return edit_medias_markup.adjust(1).as_markup()


# Кнопки выбора цели создания анкеты
goals_of_form_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='💕Отношения💕', callback_data='goal_love')
    ],
    [
        InlineKeyboardButton(text='🤝Дружба🤝', callback_data='goal_friends')
    ],
    [
        InlineKeyboardButton(text='💬Общение💬', callback_data='goal_chatting')
    ],
    [
        InlineKeyboardButton(text='🤷Без разницы🤷', callback_data='goal_nothing')
    ]
])


# Кнопки выбора своего гендера

my_gender_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='👨', callback_data='my_gender_male'),
        InlineKeyboardButton(text='👩', callback_data='my_gender_female')
    ]
])


# Кнопки выбора гендера собеседника

they_gender_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='👨', callback_data='they_gender_male'),
        InlineKeyboardButton(text='👩', callback_data='they_gender_female')
     ],
    [
        InlineKeyboardButton(text='Любой', callback_data='they_gender_any')
    ]
])


# Кнопки запроса геолокации

geolocation_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Отправить геолокацию✅', request_location=True)
    ],
    [
        KeyboardButton(text='Пропустить')
    ]
], resize_keyboard=True)


# Кнопки изменить анкету

form_settings_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='✏️Изменить анкету✏️', callback_data='edit_form')
    ],
    [
        InlineKeyboardButton(text='Продолжить✅',callback_data='start_scrolling')
    ]
])


edit_form_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='📝Изменить текст📝', callback_data='edit_form_text'),
        InlineKeyboardButton(text='Изменить фото/видео', callback_data='edit_form_media')
    ],
    [
        InlineKeyboardButton(text='🔁Заполнить анкету заново🔁', callback_data='edit_form_again')
    ],
    [
        InlineKeyboardButton(text='◀️Назад', callback_data='edit_form_back')
    ]
])


# # Кнопки редактора фото/видео

edit_media_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='➕Добавить фото/видео➕', callback_data='media_add')
    ],
    [
        InlineKeyboardButton(text='❌Удалить фото/видео❌', callback_data='media_delete')
    ],
    [
        InlineKeyboardButton(text='◀️Назад', callback_data='media_back')
    ]
])

# Кнопки взаимодействия с анкетой

forms_actions_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='♥️', callback_data='forms_action_like'),
        InlineKeyboardButton(text='👎', callback_data='forms_action_dislike')
    ],
    [
        InlineKeyboardButton(text='📝', callback_data='forms_action_text'),
        InlineKeyboardButton(text='📷/📹', callback_data='forms_action_media'),
        InlineKeyboardButton(text='🎤', callback_data='forms_action_voice')
    ],
    [
        InlineKeyboardButton(text='🚫Пожаловаться🚫', callback_data='forms_action_complaint')
    ],
    [
        InlineKeyboardButton(text='◀️Вернуться в меню', callback_data='forms_action_back')
    ]
])


# Кнопки главного меню

main_menu_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
       InlineKeyboardButton(text="Начать просмотр🔎", callback_data="start_scrolling")
    ],
    [
        InlineKeyboardButton(text="👤Профиль👤", callback_data="profile"),
        InlineKeyboardButton(text="💟Лайки💟", callback_data="likes")
    ]
])


# Кнопки профиля

profile_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✏️Изменить анкету✏️", callback_data='edit_form')
    ],
    [
        InlineKeyboardButton(text="Изменить параметры поиска🔎",
                             callback_data="change_scrolling_parameters")
    ],
    [
        InlineKeyboardButton(text="Купить 👑Premium👑", callback_data="buy_premium")
    ],
    [
        InlineKeyboardButton(text="◀️Назад", callback_data="menu_back")
    ]
])


# Кнопки посмотреть кто лайкнул/пропустить

async def create_check_like_markup(like_id: int):
    check_like_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Посмотреть👀", callback_data=f"check_like_{like_id}")
        ],
        [
            InlineKeyboardButton(text="Пропустить", callback_data="skip_like")
        ]
    ])
    return check_like_markup


# Кнопки ответа на лайк

async def create_like_answers_markup(like_id: int):
    like_answers_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="♥️", callback_data=f"answer_like_{like_id}"),
            InlineKeyboardButton(text="👎", callback_data=f"answer_dislike_{like_id}")
        ],
        [
            InlineKeyboardButton(text="🚫Пожаловаться🚫", callback_data=f"answer_complaint_{like_id}")
        ]
    ])
    return like_answers_markup


# Кнопка скрыть дополнение к лайку

put_away_like_addition_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Скрыть", callback_data="put_away_addition")
    ]
])


# Отдельная кнопка начать скроллинг

start_scrolling_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Продолжить поиск", callback_data="start_scrolling")
    ]
])


# Кнопки выбора варианта оплаты

payments_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="СберБанк", callback_data="payment_sberbank"),
        InlineKeyboardButton(text="YooMoney", callback_data="payment_yoomoney")
    ]
])


# Создание кнопки на оплату

async def create_payment_button(url: str):
    pay_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Оплатить", url=url)
        ]
    ])
    return pay_markup


# Кнопка перейти в меню

to_menu_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Перейти в меню", callback_data="menu_back")
    ]
])

