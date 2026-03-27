from App.menu.add_food import AddMenu
from App.menu.view_food import ViewMenu
from App.menu.update_food import UpdateMenu
from App.menu.delete_food import DeleteMenu


class ManageMenu:

    def add_food(self):
        obj = AddMenu()
        obj.add_food()

    def view_food(self):
        obj = ViewMenu()
        obj.view_food()

    def update_food(self):
        obj = UpdateMenu()
        obj.update_food()

    def delete_food(self):
        obj = DeleteMenu()
        obj.delete_food()

