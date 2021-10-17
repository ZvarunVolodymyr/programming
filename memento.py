import copy


class snap:
    value = None
    kwargs = None

    def __init__(self, *value, **kwargs):
        self.kwargs = {i[0]: copy.deepcopy(i[1]) for i in kwargs.items()}


class history:
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
        self.list_.append(self.obj.export_snap())
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
        self.obj.import_snap(self.list_[self.current_id])
        return True

    def redo(self):
        if self.current_id == len(self.list_) - 1:
            return False
        self.current_id += 1
        self.obj.import_snap(self.list_[self.current_id])
        return True
