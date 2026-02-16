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
