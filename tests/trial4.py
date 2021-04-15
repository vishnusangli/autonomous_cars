from pyglet import *
from pyglet.gl import *

key = pyglet.window.key

class main(pyglet.window.Window):
    def __init__ (self, width=800, height=600, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)

        self.keys = {}

        self.alive = 1

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_key_release(self, symbol, modifiers):
        try:
            del self.keys[symbol]
        except:
            pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE: # [ESC]
            self.alive = 0

        self.keys[symbol] = True

    def render(self):
        self.clear()

        ## Add stuff you want to render here.
        ## Preferably in the form of a batch.

        self.flip()

    def run(self):
        while self.alive == 1:
            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()
            print("running")
            if key.UP in self.keys:
                print('Still holding UP')
                self.alive = 0
            self.render()


if __name__ == '__main__':
    x = main()
    x.run()