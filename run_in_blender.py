"""Entry point für Blender.

Warum diese Datei?
- In Blender wird oft wiederholt "Run Script" gedrückt.
- Damit Änderungen in Modulen sofort aktiv sind, laden wir die Module per importlib.reload neu.
"""

import importlib

import scene_project.camera as camera
import scene_project.config as config
import scene_project.lights as lights
import scene_project.main as main
import scene_project.materials as materials
import scene_project.objects as objects

# Module in kontrollierter Reihenfolge neu laden (Dependencies zuerst)
for module in (materials, objects, lights, camera, config, main):
    importlib.reload(module)

# Szene bauen
main.build_scene(config.SceneConfig())
