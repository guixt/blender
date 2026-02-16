"""Material-Helferfunktionen."""

import bpy


def make_principled_material(
    name: str,
    base_color: tuple[float, float, float, float],
    roughness: float = 0.5,
    metallic: float = 0.0,
):
    """Erzeugt oder aktualisiert ein Principled-Material."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    nodes.clear()
    out = nodes.new(type="ShaderNodeOutputMaterial")
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")

    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic

    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def assign_material(obj, material):
    """Weist einem Objekt ein Material zu."""
    if obj is None or material is None:
        return

    if len(obj.data.materials) == 0:
        obj.data.materials.append(material)
    else:
        obj.data.materials[0] = material
