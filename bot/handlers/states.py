from aiogram.fsm.state import StatesGroup, State

class IncomeState(StatesGroup):
    amount = State()

class ExpenseState(StatesGroup):
    amount = State()

class NotesState(StatesGroup):
    text = State()
    delete_number = State()
