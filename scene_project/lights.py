"""Licht-Setup für die Szene."""

import bpy


def setup_sun_light(energy: float = 3.5, location: tuple[float, float, float] = (6.0, -6.0, 8.0)):
    """Fügt ein Sonnenlicht hinzu."""
    bpy.ops.object.light_add(type="SUN", location=location)
    sun = bpy.context.active_object
    sun.name = "SunKey"
    sun.data.energy = energy
    sun.rotation_euler = (0.8, 0.2, 0.6)
    return sun
