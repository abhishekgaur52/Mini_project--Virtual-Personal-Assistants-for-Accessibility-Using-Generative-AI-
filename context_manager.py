# context_manager.py

class ContextManager:
    def __init__(self):
        self.last_app = None
        self.last_action = None

    def set_context(self, app=None, action=None):
        if app:
            self.last_app = app
        if action:
            self.last_action = action

    def clear_context(self):
        self.last_app = None
        self.last_action = None

    def get_context(self):
        return {"last_app": self.last_app, "last_action": self.last_action}
