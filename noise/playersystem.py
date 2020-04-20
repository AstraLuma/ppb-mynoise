from dataclasses import dataclass
import random

from sdl2.sdlmixer import (
    # Channels https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_25.html#SEC25
    Mix_PlayChannel, Mix_Volume, Mix_Playing, Mix_Pause, Mix_Resume,
    # Other
    MIX_MAX_VOLUME,
)

import ppb
from ppb.systems.sound import SoundController, _call


def select_sounds(sounds):
    for group in sounds:
        yield random.choice(group)


@dataclass
class SetVolume:
    channel: int
    value: float


@dataclass
class PlayNoise:
    pass


@dataclass
class PauseNoise:
    pass


class NoiseSoundController(SoundController):
    def on_scene_started(self, event, signal):
        scene = event.scene
        if hasattr(scene, 'sounds') and scene.sounds:
            for i, sound in enumerate(select_sounds(scene.sounds)):
                channel = _call(
                    Mix_PlayChannel,
                    i,
                    sound.load(),
                    0,  # Do not repeat
                    _check_error=lambda rv: rv == -1
                )
                self._currently_playing[channel] = sound  # Keep reference of playing asset

    def on_idle(self, event, signal):
        scene = event.scene
        if hasattr(scene, 'sounds') and scene.sounds:
            for i, sound in enumerate(select_sounds(scene.sounds)):
                if not Mix_Playing(i):
                    channel = _call(
                        Mix_PlayChannel,
                        i,
                        sound.load(),
                        0,  # Do not repeat
                        _check_error=lambda rv: rv == -1
                    )
                    self._currently_playing[channel] = sound  # Keep reference of playing asset

    def on_set_volume(self, event, signal):
        Mix_Volume(int(event.channel), int(event.value * MIX_MAX_VOLUME))

    def on_pause_noise(self, event, signal):
        Mix_Pause(-1)

    def on_play_noise(self, event, signal):
        Mix_Resume(-1)

    # def on_key_pressed(self, event, signal):
    #     if event.key == ppb.keycodes.C:
    #         print("Current channels playing:", Mix_Playing(-1))
