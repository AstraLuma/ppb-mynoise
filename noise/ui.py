"""
Slider sprites
"""
import ppb


class Region:
    def contains(self, point):
        return (point - self.position).length <= (self.size / 2)


class SliderSprite(Region, ppb.Sprite):
    dragging = False

    min = None
    max = None

    # Defaults
    size = 0.5

    # We have an update to deliver
    _do_update = False

    @classmethod
    def build(cls, *, color, **kwargs):
        return cls(
            image=ppb.assets.Circle(*color),
            size=0.5,
            **kwargs
        )

    def on_button_pressed(self, event, signal):
        if event.button is ppb.buttons.Primary and self.contains(event.position):
            self.dragging = True

    def on_button_released(self, event, signal):
        if event.button is ppb.buttons.Primary:
            self.dragging = False

    def on_mouse_motion(self, event, signal):
        if self.dragging:
            y = event.position.y
            if self.min is not None and y < self.min:
                y = self.min
            if self.max is not None and y > self.max:
                y = self.max
            self.position = ppb.Vector(
                self.position.x,
                y,
            )
            self.do_value_changed(event, signal)

    def do_value_changed(self, event, signal):
        pass

    # value = (y - min) / (max - min)
    # value * (max - min) = y - min
    # (value * (max - min)) + min = y
    @property
    def value(self):
        return (self.position.y - self.min) / (self.max - self.min)

    @value.setter
    def value(self, value):
        if value > 1:
            value = 1
        if value < 0:
            value = 0
        self.position = self.position.update(
            y=(value * (self.max - self.min)) + self.min
        )
        self._do_update = True

    def on_idle(self, event, signal):
        if self._do_update:
            self.do_value_changed(event, signal)
            self._do_update = False


class ButtonSprite(Region, ppb.Sprite):
    def on_button_pressed(self, event, signal):
        if event.button is ppb.buttons.Primary and self.contains(event.position):
            self.do_click(event, signal)

    def do_click(self, event, signal):
        pass


class ToggleSprite(ButtonSprite):
    value = False

    true_image = ppb.assets.Circle(0, 255, 0)
    false_image = ppb.assets.Square(0, 0, 255)

    @property
    def image(self):
        if self.value:
            return self.true_image
        else:
            return self.false_image

    def do_click(self, event, signal):
        self.value = not self.value
        self.do_value_changed(event, signal)

    def do_value_changed(self, event, signal):
        pass
