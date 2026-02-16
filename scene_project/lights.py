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


def setup_city_lighting():
    """Erweitertes Beleuchtungssetup für nächtliche City-Szenen."""
    created = []

    bpy.ops.object.light_add(type="AREA", location=(8.0, -10.0, 12.0))
    area_key = bpy.context.active_object
    area_key.name = "CityAreaKey"
    area_key.data.energy = 950.0
    area_key.data.size = 7.0
    area_key.rotation_euler = (0.95, 0.0, 0.7)
    created.append(area_key)

    bpy.ops.object.light_add(type="AREA", location=(-10.0, 8.0, 9.0))
    area_rim = bpy.context.active_object
    area_rim.name = "CityAreaRim"
    area_rim.data.energy = 420.0
    area_rim.data.size = 5.0
    area_rim.data.color = (0.45, 0.7, 1.0)
    area_rim.rotation_euler = (1.1, 0.0, -2.2)
    created.append(area_rim)

    bpy.ops.object.light_add(type="POINT", location=(0.0, 0.0, 6.0))
    center_glow = bpy.context.active_object
    center_glow.name = "CityCenterGlow"
    center_glow.data.energy = 1500.0
    center_glow.data.color = (0.65, 0.2, 1.0)
    center_glow.data.shadow_soft_size = 3.0
    created.append(center_glow)

    return created


def _set_eevee_bloom_if_supported(scene):
    """Aktiviert Bloom nur in Blender-Versionen, die die Attribute besitzen."""
    eevee_settings = getattr(scene, "eevee", None)
    if eevee_settings is None:
        return

    if hasattr(eevee_settings, "use_bloom"):
        eevee_settings.use_bloom = True
    if hasattr(eevee_settings, "bloom_intensity"):
        eevee_settings.bloom_intensity = 0.11
    if hasattr(eevee_settings, "bloom_radius"):
        eevee_settings.bloom_radius = 6.5


def _set_preferred_render_engine(scene):
    """Setzt Eevee robust für unterschiedliche Blender-Versionen."""
    preferred_engines = ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT")
    available = {item.identifier for item in scene.render.bl_rna.properties["engine"].enum_items}
    for engine in preferred_engines:
        if engine in available:
            scene.render.engine = engine
            return


def setup_city_world_and_fog():
    """Setzt ein dunkles World-Setup mit Bloom/Glare-Fallbacks je nach Blender-Version."""
    scene = bpy.context.scene
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world

    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    out = nodes.new(type="ShaderNodeOutputWorld")
    bg = nodes.new(type="ShaderNodeBackground")
    bg.inputs["Color"].default_value = (0.007, 0.009, 0.02, 1.0)
    bg.inputs["Strength"].default_value = 0.35
    links.new(bg.outputs["Background"], out.inputs["Surface"])

    _set_preferred_render_engine(scene)
    _set_eevee_bloom_if_supported(scene)

    scene.use_nodes = True
    tree = scene.node_tree
    tree.nodes.clear()

    rlayers = tree.nodes.new(type="CompositorNodeRLayers")
    glare = tree.nodes.new(type="CompositorNodeGlare")
    comp = tree.nodes.new(type="CompositorNodeComposite")

    glare.glare_type = "FOG_GLOW"
    glare.quality = "HIGH"
    glare.size = 7
    glare.threshold = 0.45

    tree.links.new(rlayers.outputs["Image"], glare.inputs["Image"])
    tree.links.new(glare.outputs["Image"], comp.inputs["Image"])
