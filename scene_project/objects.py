"""Objekt-Erzeugung für die Szene."""

from __future__ import annotations

import math
import random

import bpy

from scene_project.materials import (
    assign_material,
    make_emission_material,
    make_principled_material,
    make_window_material,
)


def clear_scene():
    """Entfernt alle Objekte aus der aktuellen Szene."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def add_ground(size: float = 20.0):
    """Legt eine Ground-Plane an."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0.0, 0.0, 0.0))
    ground = bpy.context.active_object
    ground.name = "Ground"

    ground_mat = make_principled_material(
        name="M_Ground",
        base_color=(0.12, 0.16, 0.13, 1.0),
        roughness=0.9,
        metallic=0.0,
    )
    assign_material(ground, ground_mat)
    return ground


def add_forest_pond(radius: float = 2.4, location: tuple[float, float, float] = (0.0, -1.8, 0.02)):
    """Fügt einen kleinen Teich in den Wald ein."""
    x, y, z = location
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=40,
        radius=radius,
        depth=0.08,
        location=(x, y, z),
    )
    pond = bpy.context.active_object
    pond.name = "ForestPond"

    pond_mat = make_principled_material(
        name="M_Pond_Water",
        base_color=(0.05, 0.16, 0.20, 1.0),
        roughness=0.08,
        metallic=0.0,
    )
    assign_material(pond, pond_mat)

    # Flaches, leicht ovales Gewässer wirkt natürlicher als ein perfekter Kreis.
    pond.scale.x = 1.2
    pond.scale.y = 0.85
    return pond


def add_city_ground(size: float = 24.0):
    """Legt eine dunkle Ground-Plane für City-Szenen an."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0.0, 0.0, 0.0))
    ground = bpy.context.active_object
    ground.name = "CityGround"

    ground_mat = make_principled_material(
        name="M_City_Ground",
        base_color=(0.02, 0.02, 0.03, 1.0),
        roughness=0.95,
        metallic=0.0,
    )
    assign_material(ground, ground_mat)
    return ground


def add_tree(location: tuple[float, float, float], scale: float = 1.0):
    """Erstellt einen sehr einfachen Low-Poly-Baum (Stamm + Krone)."""
    x, y, z = location

    bpy.ops.mesh.primitive_cylinder_add(radius=0.12 * scale, depth=1.1 * scale, location=(x, y, z + 0.55 * scale))
    trunk = bpy.context.active_object
    trunk.name = f"Tree_Trunk_{x:.2f}_{y:.2f}"

    trunk_mat = make_principled_material(
        name="M_Trunk",
        base_color=(0.18, 0.10, 0.05, 1.0),
        roughness=0.8,
        metallic=0.0,
    )
    assign_material(trunk, trunk_mat)

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.6 * scale, location=(x, y, z + 1.25 * scale))
    crown = bpy.context.active_object
    crown.name = f"Tree_Crown_{x:.2f}_{y:.2f}"

    crown_mat = make_principled_material(
        name="M_Crown",
        base_color=(0.08, 0.28, 0.12, 1.0),
        roughness=0.6,
        metallic=0.0,
    )
    assign_material(crown, crown_mat)

    return trunk, crown


def add_tree_cluster(count: int, area_half_extent: float, seed: int = 42):
    """Platziert mehrere einfache Bäume verteilt in einem Bereich."""
    random.seed(seed)
    created = []

    for _ in range(count):
        x = random.uniform(-area_half_extent, area_half_extent)
        y = random.uniform(-area_half_extent, area_half_extent)
        scale = random.uniform(0.8, 1.3)
        created.extend(add_tree(location=(x, y, 0.0), scale=scale))

    return created


def add_rock_field(count: int, area_half_extent: float, seed: int = 101):
    """Verteilt kleinere Felsen auf dem Waldboden."""
    random.seed(seed)
    created = []
    rock_mat = make_principled_material(
        name="M_Rock",
        base_color=(0.24, 0.25, 0.23, 1.0),
        roughness=0.92,
        metallic=0.0,
    )

    for idx in range(count):
        x = random.uniform(-area_half_extent, area_half_extent)
        y = random.uniform(-area_half_extent, area_half_extent)
        scale = random.uniform(0.15, 0.45)

        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(x, y, scale * 0.45))
        rock = bpy.context.active_object
        rock.name = f"Rock_{idx:02d}"
        rock.scale = (scale * random.uniform(1.0, 1.8), scale * random.uniform(0.8, 1.3), scale * random.uniform(0.6, 1.0))
        rock.rotation_euler = (random.uniform(-0.35, 0.35), random.uniform(-0.35, 0.35), random.uniform(0.0, 3.14))
        assign_material(rock, rock_mat)
        created.append(rock)

    return created


def add_bush_cluster(count: int, area_half_extent: float, seed: int = 202):
    """Fügt niedrige Büsche zwischen den Bäumen ein."""
    random.seed(seed)
    created = []
    bush_mat = make_principled_material(
        name="M_Bush",
        base_color=(0.09, 0.33, 0.14, 1.0),
        roughness=0.55,
        metallic=0.0,
    )

    for idx in range(count):
        x = random.uniform(-area_half_extent, area_half_extent)
        y = random.uniform(-area_half_extent, area_half_extent)
        size = random.uniform(0.25, 0.7)

        bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=(x, y, size * 0.6))
        bush = bpy.context.active_object
        bush.name = f"Bush_{idx:02d}"
        bush.scale = (1.2, random.uniform(0.7, 1.4), 0.65)
        assign_material(bush, bush_mat)
        created.append(bush)

    return created


def _add_city_tower(
    location: tuple[float, float, float],
    width: float,
    depth: float,
    height: float,
    material_name: str,
    base_color: tuple[float, float, float, float],
    emission_color: tuple[float, float, float, float],
):
    """Erzeugt einen Tower mit kleinen Aufbauten auf dem Dach."""
    x, y, z = location
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z + (height / 2.0)))
    tower = bpy.context.active_object
    tower.name = f"Tower_{x:.1f}_{y:.1f}"
    tower.scale = (width / 2.0, depth / 2.0, height / 2.0)

    tower_mat = make_window_material(
        name=material_name,
        base_color=base_color,
        emission_color=emission_color,
        emission_strength=1.6,
    )
    assign_material(tower, tower_mat)

    # Dach-Aufbau (Tech-Box)
    roof_height = random.uniform(0.2, 0.5)
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z + height + roof_height / 2.0))
    rooftop = bpy.context.active_object
    rooftop.name = f"Rooftop_{x:.1f}_{y:.1f}"
    rooftop.scale = (width * 0.22, depth * 0.22, roof_height / 2.0)

    rooftop_mat = make_principled_material(
        name="M_City_Rooftop",
        base_color=(0.03, 0.03, 0.04, 1.0),
        roughness=0.45,
        metallic=0.65,
    )
    assign_material(rooftop, rooftop_mat)

    return tower, rooftop


def add_city_block_grid(
    grid_size: int,
    spacing: float,
    min_height: float,
    max_height: float,
    seed: int = 7,
):
    """Erzeugt ein futuristisches City-Grid mit variierenden Tower-Höhen."""
    random.seed(seed)
    created = []
    half = (grid_size - 1) * spacing * 0.5

    neon_variants = [
        ("M_City_Blue", (0.08, 0.22, 0.45, 1.0), (0.18, 0.70, 1.0, 1.0)),
        ("M_City_Purple", (0.19, 0.09, 0.32, 1.0), (0.65, 0.28, 1.0, 1.0)),
        ("M_City_Cyan", (0.05, 0.28, 0.30, 1.0), (0.20, 1.0, 0.9, 1.0)),
    ]

    for gx in range(grid_size):
        for gy in range(grid_size):
            x = gx * spacing - half
            y = gy * spacing - half
            height = random.uniform(min_height, max_height)

            # Jede dritte Kachel bleibt frei als "Straßenraum".
            if (gx + gy) % 3 == 0:
                continue

            mat_name, color, emissive = random.choice(neon_variants)
            width = random.uniform(1.2, 2.0)
            depth = random.uniform(1.2, 2.0)
            tower_parts = _add_city_tower(
                location=(x, y, 0.0),
                width=width,
                depth=depth,
                height=height,
                material_name=mat_name,
                base_color=color,
                emission_color=emissive,
            )
            created.extend(tower_parts)

    return created


def add_city_roads(grid_size: int, spacing: float, line_width: float = 0.12):
    """Fügt ein schlichtes Straßenraster mit leuchtenden Markierungen hinzu."""
    created = []
    half = (grid_size - 1) * spacing * 0.5
    road_extent = half + spacing * 0.5

    road_mat = make_principled_material(
        name="M_City_Road",
        base_color=(0.015, 0.015, 0.02, 1.0),
        roughness=0.85,
        metallic=0.05,
    )
    line_mat = make_emission_material(
        name="M_City_Road_Line",
        color=(0.1, 0.85, 1.0, 1.0),
        strength=3.0,
    )

    for i in range(grid_size + 1):
        offset = -half - spacing * 0.5 + i * spacing

        bpy.ops.mesh.primitive_plane_add(size=1.0, location=(offset, 0.0, 0.001))
        road_x = bpy.context.active_object
        road_x.name = f"Road_X_{i:02d}"
        road_x.scale = (spacing * 0.22, road_extent, 1.0)
        assign_material(road_x, road_mat)
        created.append(road_x)

        bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, offset, 0.001))
        road_y = bpy.context.active_object
        road_y.name = f"Road_Y_{i:02d}"
        road_y.scale = (road_extent, spacing * 0.22, 1.0)
        assign_material(road_y, road_mat)
        created.append(road_y)

    for i in range(grid_size + 1):
        offset = -half - spacing * 0.5 + i * spacing

        bpy.ops.mesh.primitive_cube_add(location=(offset, 0.0, 0.012))
        line_x = bpy.context.active_object
        line_x.name = f"RoadLine_X_{i:02d}"
        line_x.scale = (line_width, road_extent * 0.98, 0.002)
        assign_material(line_x, line_mat)
        created.append(line_x)

        bpy.ops.mesh.primitive_cube_add(location=(0.0, offset, 0.012))
        line_y = bpy.context.active_object
        line_y.name = f"RoadLine_Y_{i:02d}"
        line_y.scale = (road_extent * 0.98, line_width, 0.002)
        assign_material(line_y, line_mat)
        created.append(line_y)

    return created


def add_city_elevated_ring(radius: float = 8.0, width: float = 0.55):
    """Erzeugt einen erhöhten Ring als Sci-Fi-Skyway."""
    created = []

    bpy.ops.mesh.primitive_torus_add(
        location=(0.0, 0.0, 2.8),
        major_radius=radius,
        minor_radius=width,
        abso_major_rad=1.0,
        abso_minor_rad=0.5,
    )
    ring = bpy.context.active_object
    ring.name = "SkywayRing"
    ring_mat = make_principled_material(
        name="M_City_Skyway",
        base_color=(0.04, 0.05, 0.08, 1.0),
        roughness=0.4,
        metallic=0.7,
    )
    assign_material(ring, ring_mat)
    created.append(ring)

    bpy.ops.mesh.primitive_torus_add(
        location=(0.0, 0.0, 2.95),
        major_radius=radius,
        minor_radius=0.06,
        abso_major_rad=1.0,
        abso_minor_rad=0.5,
    )
    rail = bpy.context.active_object
    rail.name = "SkywayRailGlow"
    rail_mat = make_emission_material(
        name="M_City_Skyway_Glow",
        color=(0.42, 0.12, 1.0, 1.0),
        strength=9.0,
    )
    assign_material(rail, rail_mat)
    created.append(rail)

    return created


def add_city_holo_billboards(count: int, radius: float, seed: int = 17):
    """Platziert holografische Werbetafeln um das Zentrum."""
    random.seed(seed)
    created = []

    panel_mat = make_emission_material(
        name="M_Holo_Panel",
        color=(0.05, 0.95, 0.95, 1.0),
        strength=12.0,
    )
    frame_mat = make_principled_material(
        name="M_Holo_Frame",
        base_color=(0.03, 0.03, 0.04, 1.0),
        roughness=0.35,
        metallic=0.78,
    )

    for idx in range(count):
        angle = (idx / count) * 6.283185 + random.uniform(-0.15, 0.15)
        dist = radius + random.uniform(-1.2, 1.2)
        x = dist * math.cos(angle)
        y = dist * math.sin(angle)
        z = random.uniform(2.0, 4.2)

        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=z, location=(x, y, z * 0.5))
        mast = bpy.context.active_object
        mast.name = f"HoloMast_{idx:02d}"
        assign_material(mast, frame_mat)
        created.append(mast)

        bpy.ops.mesh.primitive_plane_add(size=1.0, location=(x, y, z + 0.8))
        panel = bpy.context.active_object
        panel.name = f"HoloPanel_{idx:02d}"
        panel.scale = (1.1, 0.45, 1.0)
        panel.rotation_euler = (1.5708, 0.0, angle + 1.5708)
        assign_material(panel, panel_mat)
        created.append(panel)

    return created


def add_city_central_spire(height: float = 13.0):
    """Baut einen zentralen Spire als Landmarke."""
    created = []

    bpy.ops.mesh.primitive_cylinder_add(radius=1.3, depth=height, location=(0.0, 0.0, height * 0.5))
    core = bpy.context.active_object
    core.name = "CentralSpire_Core"
    core_mat = make_window_material(
        name="M_Spire_Core",
        base_color=(0.07, 0.08, 0.12, 1.0),
        emission_color=(0.35, 0.6, 1.0, 1.0),
        emission_strength=2.8,
    )
    assign_material(core, core_mat)
    created.append(core)

    bpy.ops.mesh.primitive_cone_add(radius1=1.0, radius2=0.2, depth=4.0, location=(0.0, 0.0, height + 2.0))
    tip = bpy.context.active_object
    tip.name = "CentralSpire_Tip"
    tip_mat = make_emission_material(
        name="M_Spire_Tip_Glow",
        color=(0.85, 0.2, 1.0, 1.0),
        strength=15.0,
    )
    assign_material(tip, tip_mat)
    created.append(tip)

    return created


def add_city_sky_drones(count: int, area_half_extent: float, seed: int = 23):
    """Kleine leuchtende Dronen-Kugeln als Leben im Himmel."""
    random.seed(seed)
    created = []

    for idx in range(count):
        x = random.uniform(-area_half_extent, area_half_extent)
        y = random.uniform(-area_half_extent, area_half_extent)
        z = random.uniform(4.0, 9.0)
        size = random.uniform(0.06, 0.16)

        bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=(x, y, z))
        drone = bpy.context.active_object
        drone.name = f"SkyDrone_{idx:02d}"

        hue_variant = random.choice(
            [
                ("M_Drone_Cyan", (0.25, 1.0, 0.9, 1.0)),
                ("M_Drone_Magenta", (1.0, 0.28, 0.85, 1.0)),
                ("M_Drone_Blue", (0.35, 0.55, 1.0, 1.0)),
            ]
        )
        mat_name, color = hue_variant
        drone_mat = make_emission_material(name=mat_name, color=color, strength=20.0)
        assign_material(drone, drone_mat)
        created.append(drone)

    return created
