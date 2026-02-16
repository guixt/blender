"""Kamera-Setup."""

import bpy


def setup_camera(
    location: tuple[float, float, float] = (12.0, -14.0, 10.0),
    rotation_euler: tuple[float, float, float] = (1.0, 0.0, 0.75),
):
    """Erzeugt eine Kamera und setzt sie als aktive Kamera der Szene."""
    bpy.ops.object.camera_add(location=location, rotation=rotation_euler)
    cam = bpy.context.active_object
    cam.name = "MainCamera"

    bpy.context.scene.camera = cam
    return cam
