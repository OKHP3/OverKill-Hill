"""Reproducible measured previs, not a finished MurderBird model."""
import bpy, json, math
from pathlib import Path
from mathutils import Vector
OUT = Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
scene.unit_settings.length_unit = 'METERS'
def material(name, color):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); return m
bronze=material('Proxy bronze',(0.3,0.19,0.075))
human=material('Mannequin neutral',(0.35,0.4,0.43))
steel=material('Stage steel',(0.13,0.17,0.18))
orange=material('Height datum',(1,0.35,0.03))
def box(name,loc,size,mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat); return o
box('Ground',(0,0,-0.05),(7,5,0.1),steel)
box('Bird envelope - WORKING HEIGHT 1.8 m',(-1,0,0.9),(0.85,0.9,1.8),bronze).display_type='WIRE'
box('Height datum 1.8 m',(-1.65,0,0.9),(0.025,0.025,1.8),orange)
box('Crown height crossbar',(-1.35,0,1.8),(0.6,0.025,0.015),orange)
# Deliberately abstract floor-standing bird massing. Not a character rig.
box('Bird left leg',(-1.2,0,0.45),(0.13,0.16,0.9),bronze)
box('Bird right leg',(-0.8,0,0.45),(0.13,0.16,0.9),bronze)
box('Bird torso',(-1,0,1.13),(0.65,0.62,0.5),bronze)
box('Bird neck',(-1,-0.16,1.5),(0.23,0.3,0.3),bronze)
box('Bird head',(-1,-0.27,1.68),(0.3,0.5,0.24),bronze)
# Human proxy reaches exactly 1.8m, beside bird on same y plane.
box('Adult left leg',(0.04,0,0.45),(0.15,0.22,0.9),human)
box('Adult right leg',(0.26,0,0.45),(0.15,0.22,0.9),human)
box('Adult torso',(0.15,0,1.2),(0.44,0.26,0.6),human)
box('Adult head',(0.15,0,1.65),(0.22,0.23,0.3),human)
box('Adult left arm',(-0.13,0,1.16),(0.12,0.14,0.62),human)
box('Adult right arm',(0.43,0,1.16),(0.12,0.14,0.62),human)
box('Bench top - upper face 0.9 m',(1.55,0,0.85),(1.45,0.75,0.1),steel)
for x in [0.93,2.17]:
    for y in [-0.28,0.28]: box('Bench leg',(x,y,0.4),(0.08,0.08,0.8),steel)
box('Ordinary CRT - height 0.4 m',(1.45,0,1.1),(0.45,0.42,0.4),human)
box('CRT screen',(1.45,-0.215,1.1),(0.35,0.01,0.27),steel)
box('Floor cradle base',(-1,1.2,0.06),(1.15,0.8,0.12),steel)
for x in [-1.45,-0.55]: box('Cradle upright',(x,1.2,0.35),(0.08,0.08,0.58),steel)
ref=Path('C:/Users/jamie/Documents/murderbird-production/2026-09-06/scale-study-human-height-candidate.png')
if ref.exists():
    img=bpy.data.images.load(str(ref)); img.pack()
    empty=bpy.data.objects.new('REFERENCE ONLY - not dimensionally calibrated',None)
    bpy.context.collection.objects.link(empty)
    empty.empty_display_type='IMAGE'; empty.data=img
    empty.empty_display_size=3.0; empty.location=(0,2,1.5)
    empty.rotation_euler=(math.pi/2,0,0); empty.hide_render=True
def camera(name,loc,target,ortho=False):
    data=bpy.data.cameras.new(name); obj=bpy.data.objects.new(name,data)
    bpy.context.collection.objects.link(obj); obj.location=loc
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
    if ortho: data.type='ORTHO'; data.ortho_scale=5.2
    else: data.lens=50
    return obj
scene.camera=camera('Perspective scale review',(5,-8,4),(0,0,0.95))
camera('Front orthographic - shared floor plane',(0,-8,0.9),(0,0,0.9),True)
camera('Side orthographic',(8,0,0.9),(0,0,0.9),True)
bpy.ops.object.light_add(type='AREA', location=(0,-3,5))
bpy.context.object.data.energy=1000; bpy.context.object.data.shape='DISK'; bpy.context.object.data.size=5
scene.render.resolution_x=1280; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.world.color=(0.15,0.15,0.15)
scene['production_status']='Measured previs only; 1.8m is provisional design target; not a character rig.'
scene['reference_warning']='Packed reference image is concept art and is not dimensionally calibrated.'
bpy.context.view_layer.update()
manifest={'units':'metres','status':scene['production_status'],'objects':[
{'name':o.name,'location_m':list(o.location),'dimensions_m':list(o.dimensions)}
for o in scene.objects if o.type=='MESH']}
(OUT/'scale-stage-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'murderbird-scale-stage.blend'))

