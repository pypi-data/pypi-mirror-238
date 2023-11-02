class TodoListManager:
    def __init__(self):
        self.todo_lists = {}

    def create_todo_list(self, name):
        if name in self.todo_lists:
            raise ValueError(f"TodoList named {name} already exists.")
        self.todo_lists[name] = []

    def delete_todo_list(self, name):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        del self.todo_lists[name]

    def show_all_todo_list(self):
        return self.todo_lists

    def change_todo_list_name(self, old_name, new_name):
        if old_name not in self.todo_lists:
            raise ValueError(f"No TodoList named {old_name} found.")
        if new_name in self.todo_lists:
            raise ValueError(f"TodoList named {new_name} already exists.")
        self.todo_lists[new_name] = self.todo_lists.pop(old_name)

    def add_item_to_todo_list(self, name, item):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        self.todo_lists[name].append(item)

    def show_all_items_in_todo_list(self, name):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        return self.todo_lists[name]

    def remove_item_from_todo_list(self, name, index):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        try:
            del self.todo_lists[name][index]
        except IndexError:
            raise IndexError(f"No item at index {index} in TodoList {name}.")
