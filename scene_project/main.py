"""Main-Orchestrierung der Szene."""

from scene_project.camera import setup_camera
from scene_project.config import SceneConfig
from scene_project.lights import setup_city_lighting, setup_city_world_and_fog, setup_sun_light
from scene_project.objects import (
    add_bush_cluster,
    add_city_block_grid,
    add_city_central_spire,
    add_city_elevated_ring,
    add_city_ground,
    add_city_holo_billboards,
    add_city_roads,
    add_city_sky_drones,
    add_forest_pond,
    add_ground,
    add_rock_field,
    add_tree_cluster,
    clear_scene,
)


def _build_forest_scene(cfg: SceneConfig):
    """Baut eine dichtere Waldszene mit Teich, Felsen und Büschen."""
    add_ground(size=cfg.ground_size)
    add_tree_cluster(count=cfg.tree_count, area_half_extent=cfg.tree_area_half_extent, seed=42)
    add_rock_field(count=cfg.rock_count, area_half_extent=cfg.tree_area_half_extent, seed=101)
    add_bush_cluster(count=cfg.bush_count, area_half_extent=cfg.tree_area_half_extent * 0.95, seed=202)
    add_forest_pond(radius=cfg.pond_radius)


def _build_futuristic_city_scene(cfg: SceneConfig):
    """Baut eine deutlich komplexere futuristische Stadt."""
    ground_size = max(cfg.ground_size, cfg.city_grid_size * cfg.city_block_spacing * 1.2)
    city_extent = cfg.city_grid_size * cfg.city_block_spacing * 0.7

    add_city_ground(size=ground_size)
    add_city_roads(grid_size=cfg.city_grid_size, spacing=cfg.city_block_spacing)
    add_city_block_grid(
        grid_size=cfg.city_grid_size,
        spacing=cfg.city_block_spacing,
        min_height=cfg.city_min_height,
        max_height=cfg.city_max_height,
        seed=7,
    )
    add_city_central_spire(height=cfg.city_spire_height)
    add_city_elevated_ring(radius=cfg.city_ring_radius)
    add_city_holo_billboards(count=cfg.city_holo_billboards, radius=city_extent, seed=17)
    add_city_sky_drones(count=cfg.city_drone_count, area_half_extent=city_extent, seed=23)


def build_scene(config: SceneConfig | None = None):
    """Baut die Szene anhand einer Konfiguration auf."""
    cfg = config or SceneConfig()
    scene_name = cfg.scene_name.lower().strip()

    clear_scene()

    builders = {
        "forest": _build_forest_scene,
        "city": _build_futuristic_city_scene,
    }
    scene_builder = builders.get(scene_name)
    if scene_builder is None:
        supported = ", ".join(sorted(builders))
        raise ValueError(f"Unbekannte Szene '{cfg.scene_name}'. Erlaubt: {supported}")

    scene_builder(cfg)

    if scene_name == "city":
        setup_city_world_and_fog()
        setup_city_lighting()
        setup_camera(location=(20.0, -22.0, 14.0), rotation_euler=(1.08, 0.0, 0.8))
    else:
        setup_sun_light(energy=cfg.sun_energy)
        setup_camera(location=cfg.camera_location, rotation_euler=cfg.camera_rotation_euler)

    print(f"[scene_project] Scene '{scene_name}' build complete.")
