"""Zentrale Konfiguration für die Szene.

Alle Werte können pro Iteration verändert werden, ohne die Kernlogik umzubauen.
"""

from dataclasses import dataclass


@dataclass
class SceneConfig:
    scene_name: str = "forest"

    # Forest-Setup
    ground_size: float = 20.0
    tree_count: int = 12
    tree_area_half_extent: float = 8.0

    # City-Setup
    city_grid_size: int = 8
    city_block_spacing: float = 3.0
    city_min_height: float = 2.2
    city_max_height: float = 11.0
    city_holo_billboards: int = 14
    city_drone_count: int = 22
    city_ring_radius: float = 9.5
    city_spire_height: float = 15.0

    # Shared scene settings
    sun_energy: float = 3.5
    camera_location: tuple[float, float, float] = (12.0, -14.0, 10.0)
    camera_rotation_euler: tuple[float, float, float] = (1.0, 0.0, 0.75)
