"""Zentrale Konfiguration für die Szene.

Alle Werte können pro Iteration verändert werden, ohne die Kernlogik umzubauen.
"""

from dataclasses import dataclass


@dataclass
class SceneConfig:
    ground_size: float = 20.0
    tree_count: int = 12
    tree_area_half_extent: float = 8.0
    sun_energy: float = 3.5
    camera_location: tuple[float, float, float] = (12.0, -14.0, 10.0)
    camera_rotation_euler: tuple[float, float, float] = (1.0, 0.0, 0.75)
