import ppb
from ppb.assetlib import AssetLoadingSystem
from ppb.systems import EventPoller, Renderer, Updater

from noise.playerscene import PlayerScene
from noise.playersystem import NoiseSoundController


ppb.run(
    starting_scene=PlayerScene,
    basic_systems=(Renderer, Updater, EventPoller, NoiseSoundController, AssetLoadingSystem),
)
