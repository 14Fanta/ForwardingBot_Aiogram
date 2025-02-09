from aiogram.fsm.state import State,StatesGroup

class waiting(StatesGroup):
    waiting_a_message = State() 
    add_a_word_to_filter = State()
    waiting_a_group = State()
    delete_a_word_from_filter= State()