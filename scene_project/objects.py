"""Objekt-Erzeugung für die Szene."""

from __future__ import annotations

import random

import bpy

from scene_project.materials import assign_material, make_principled_material


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
):
    """Erzeugt einen einfachen Tower als Box."""
    x, y, z = location
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z + (height / 2.0)))
    tower = bpy.context.active_object
    tower.name = f"Tower_{x:.1f}_{y:.1f}"
    tower.scale = (width / 2.0, depth / 2.0, height / 2.0)

    tower_mat = make_principled_material(
        name=material_name,
        base_color=base_color,
        roughness=0.25,
        metallic=0.35,
    )
    assign_material(tower, tower_mat)
    return tower


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
        ("M_City_Blue", (0.08, 0.22, 0.45, 1.0)),
        ("M_City_Purple", (0.19, 0.09, 0.32, 1.0)),
        ("M_City_Cyan", (0.05, 0.28, 0.30, 1.0)),
    ]

    for gx in range(grid_size):
        for gy in range(grid_size):
            x = gx * spacing - half
            y = gy * spacing - half
            height = random.uniform(min_height, max_height)

            # Jede dritte Kachel bleibt frei als "Straßenraum".
            if (gx + gy) % 3 == 0:
                continue

            mat_name, color = random.choice(neon_variants)
            width = random.uniform(1.2, 2.0)
            depth = random.uniform(1.2, 2.0)
            tower = _add_city_tower(
                location=(x, y, 0.0),
                width=width,
                depth=depth,
                height=height,
                material_name=mat_name,
                base_color=color,
            )
            created.append(tower)

    return created
