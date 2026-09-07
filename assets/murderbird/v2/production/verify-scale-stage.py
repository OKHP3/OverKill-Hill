import bpy,json
from pathlib import Path
out=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(out/'murderbird-scale-stage.blend'))
bpy.context.view_layer.update()
def near(a,b): return abs(a-b)<0.00001
def extent(names):
    objects=[bpy.data.objects[n] for n in names]
    return max(o.location.z+o.dimensions.z/2 for o in objects)-min(o.location.z-o.dimensions.z/2 for o in objects)
checks={
 'metric_units':bpy.context.scene.unit_settings.system=='METRIC',
 'bird_envelope_1_8m':near(bpy.data.objects['Bird envelope - WORKING HEIGHT 1.8 m'].dimensions.z,1.8),
 'adult_height_1_8m':near(extent(['Adult left leg','Adult right leg','Adult torso','Adult head']),1.8),
 'bench_top_0_9m':near(bpy.data.objects['Bench top - upper face 0.9 m'].location.z+bpy.data.objects['Bench top - upper face 0.9 m'].dimensions.z/2,0.9),
 'crt_height_0_4m':near(bpy.data.objects['Ordinary CRT - height 0.4 m'].dimensions.z,0.4),
 'three_cameras':len([o for o in bpy.context.scene.objects if o.type=='CAMERA'])==3,
 'packed_reference':any(i.packed_file for i in bpy.data.images),
}
report={'checks':checks,'all_pass':all(checks.values()),'blender_version':bpy.app.version_string}
(out/'scale-stage-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
assert report['all_pass']

