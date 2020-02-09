
class Entity:

    def __init__(self):
        pass

    def on_update(self, delta):
        raise NotImplementedError

    def on_render(self, screen):
        raise NotImplementedError
