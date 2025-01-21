from aiogram.fsm.state import State, StatesGroup


class FormBuilder(StatesGroup):
    create_form_name = State()
    create_form_age = State()
    create_form_media = State()
    create_form_profile_text = State()
    create_form_city = State()
    create_form_geolocation = State()


class FormEdit(StatesGroup):
    edit_form_text = State()
    edit_form_media = State()


class FormActions(StatesGroup):
    get_like_message = State()
    get_like_media = State()
    get_like_voice = State()
