from sqladmin import ModelView, Admin

from main import app, engine
from models import User, Pet

admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = (User.id, User.name)


class PetAdmin(ModelView, model=Pet):
    column_list = (Pet.id, Pet.name)


admin.add_view(UserAdmin)
admin.add_view(PetAdmin)
