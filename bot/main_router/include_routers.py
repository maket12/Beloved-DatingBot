from aiogram import Dispatcher
from bot.handlers.messages.start import router as start_router
from bot.handlers.messages.help import router as help_router
from bot.handlers.messages.delete import router as delete_router
from bot.handlers.callback_queries.form.create_form import router as create_form_router
from bot.handlers.callback_queries.form.edit_form import router as edit_form_router
from bot.handlers.states_handlers.form_steps_states import router as form_steps_states_router
from bot.handlers.states_handlers.edit_form_states import router as edit_form_states_router
from bot.handlers.callback_queries.scrolling.start_scrolling import router as start_scrolling_router
from bot.handlers.callback_queries.scrolling.forms_actions import router as forms_actions_router
from bot.handlers.states_handlers.forms_actions_states import router as forms_actions_states_router
from bot.handlers.messages.main_menu import router as main_menu_router
from bot.handlers.callback_queries.likes.like_answers import router as like_answers_router
from bot.handlers.callback_queries.main_menu.main_menu_actions import router as main_menu_actions_router
from bot.handlers.callback_queries.main_menu.profile_actions import router as profile_router
from bot.handlers.callback_queries.main_menu.payments import router as payments_router
from bot.services.payments.sberbank.answer_pre_checkout import router as sberbank_router
from bot.services.payments.sberbank.successful_payment import router as sberbank_success_router


def include_all_routers(dp: Dispatcher):
    routers_list = [start_router, help_router, delete_router, create_form_router, edit_form_router,
                    form_steps_states_router, edit_form_states_router, start_scrolling_router,
                    forms_actions_router, forms_actions_states_router, main_menu_router,
                    like_answers_router, main_menu_actions_router, profile_router,
                    payments_router, sberbank_router, sberbank_success_router]
    for router in routers_list:
        dp.include_router(router)

