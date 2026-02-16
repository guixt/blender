"""Main-Orchestrierung der Szene."""

from scene_project.camera import setup_camera
from scene_project.config import SceneConfig
from scene_project.lights import setup_sun_light
from scene_project.objects import add_ground, add_tree_cluster, clear_scene


def build_scene(config: SceneConfig | None = None):
    """Baut die Szene anhand einer Konfiguration auf."""
    cfg = config or SceneConfig()

    clear_scene()
    add_ground(size=cfg.ground_size)
    add_tree_cluster(count=cfg.tree_count, area_half_extent=cfg.tree_area_half_extent, seed=42)
    setup_sun_light(energy=cfg.sun_energy)
    setup_camera(location=cfg.camera_location, rotation_euler=cfg.camera_rotation_euler)

    print("[scene_project] Scene build complete.")
