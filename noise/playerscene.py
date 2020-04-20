import ppb
from ppb_mutant import Emoji

from .ui import SliderSprite, ToggleSprite, ButtonSprite
from .playersystem import SetVolume, PlayNoise, PauseNoise


COLORS = [
    (0x66, 0x33, 0x00),
    (0xCC, 0x00, 0x00),
    (0xFF, 0x88, 0x00),
    (0x99, 0xBB, 0x00),
    (0x00, 0xCC, 0x00),
    (0x00, 0xCC, 0xAA),
    (0x00, 0x88, 0xDD),
    (0x00, 0x00, 0xFF),
    (0x88, 0x00, 0xAA),
    (0xCC, 0x88, 0xFF),
]


def _build_sounds(prefix):
    files = sorted(f for f in ppb.vfs.iterdir(prefix) if f.endswith('.ogg'))
    channels = [
        [
            ppb.Sound(f"{prefix}/{fn}")
            for fn in files
            if fn.startswith(str(i))
        ]
        for i in range(10)
    ]
    return channels


class ChannelSlider(SliderSprite):
    channel = None

    def do_value_changed(self, event, signal):
        # self.size = max(self.value, 0.1)
        signal(SetVolume(
            channel=self.channel,
            value=self.value,
        ))


class PlayToggle(ToggleSprite):
    true_image = Emoji('awoo')
    false_image = Emoji('dont_awoo')

    def do_value_changed(self, event, signal):
        if self.value:
            signal(PlayNoise())
        else:
            signal(PauseNoise())


class VolumeUp(ButtonSprite):
    image = Emoji('speaker_loud_volume')

    def do_click(self, event, signal):
        for slider in event.scene.get(tag='slider'):
            slider.value *= 1.1


class VolumeDown(ButtonSprite):
    image = Emoji('speaker_low_volume')

    def do_click(self, event, signal):
        for slider in event.scene.get(tag='slider'):
            slider.value /= 1.1


class Reset(ButtonSprite):
    image = Emoji('arrows_clockwise')

    def do_click(self, event, signal):
        for slider in event.scene.get(tag='slider'):
            slider.value = 0.1


class PlayerScene(ppb.BaseScene):
    sounds = _build_sounds('noise/noises/osmosis')

    def on_scene_started(self, event, signal):
        # UI
        self.add(Reset(position=(-4, -1.5)))
        self.add(VolumeDown(position=(2, -1.5)))
        self.add(VolumeUp(position=(3, -1.5)))
        self.add(PlayToggle(position=(4, -1.5), value=True))

        for i, color in enumerate(COLORS):
            self.add(sprite := ChannelSlider(
                image=ppb.assets.Circle(*color),
                position=ppb.Vector(i - 4.5, 0),
                min=0,
                max=4,
                channel=i,
                value=0.1
            ), tags=['slider'])
            signal(SetVolume(channel=i, value=sprite.value))
