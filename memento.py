import copy


class history:
    class memento:
        value = {}

        def __init__(self, obj):
            dict_ = vars(obj)
            self.value = {i[0]: copy.deepcopy(i[1]) for i in dict_.items() if type(i[1]) != type(history(None))}
            self.value = self.value

        def import_to(self, obj):
            for i in self.value.items():
                obj.__setattr__(i[0], copy.deepcopy(i[1]))

    obj = None
    current_id = -1
    list_ = []
    limit = 2

    def __init__(self, obj):
        self.obj = obj
        if obj is None:
            return
        self.new_snap()

    def new_snap(self):
        self.list_ = self.list_[:min(self.current_id + 1, len(self.list_))]
        self.list_.append(history.memento(self.obj))
        if len(self.list_) > self.limit:
            self.pop_snap(0)
        self.current_id += 1

    def pop_snap(self, index=None):
        if len(self.list_) == 1:
            return
        if index is None:
            self.list_.pop()
        else:
            self.list_.pop(index)
        self.current_id -= 1

    def undo(self):
        if self.current_id == 0:
            return False
        self.current_id -= 1
        self.list_[self.current_id].import_to(self.obj)
        return True

    def redo(self):
        if self.current_id == len(self.list_) - 1:
            return False
        self.current_id += 1
        self.list_[self.current_id].import_to(self.obj)
        return True
