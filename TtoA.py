import bpy
from mathutils import Quaternion, Matrix

###
MODE = 0
# MODE=0: TtoA, MODE=1: AtoT
###

target_body_name = "Body2"
armature_name = "Armature"
left_arm_name = "Left arm"
right_arm_name = "Right arm"
t_to_a = -1
a_to_t = 1
angle = 0.785398

###

if (MODE == 0):
    angle = angle * t_to_a
if (MODE == 1):
    angle = angle * a_to_t

# Armatureを選択し、ポーズモードにする
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
armature = bpy.data.objects[armature_name]
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

# 左右の腕を回転
for bone_name in [left_arm_name, right_arm_name]:
    bone = armature.pose.bones[bone_name]

    # クォータニオンで回転を設定する。
    rotation_quat = Quaternion((1, 0, 0), angle)
    bone.rotation_quaternion = rotation_quat

# オブジェクトモードに移行し、target_skinを選択する
bpy.ops.object.mode_set(mode='OBJECT')
target_skin = bpy.data.objects[target_body_name]

# Armatureモディファイアを適用する
armature_mod = target_skin.modifiers.get(armature_name)

# 選択解除（Blender仕様に合わせたおまじない的）
if armature_mod:
    bpy.ops.object.select_all(action='DESELECT')
    target_skin.select_set(True)
    bpy.context.view_layer.objects.active = target_skin
    
    if target_skin.data.shape_keys is None:
        bpy.ops.object.modifier_apply(modifier=armature_mod.name)

    else:
        bpy.ops.sk.apply_mods_sk()

# ポーズモードに移行する
bpy.ops.object.select_all(action='DESELECT')
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

# レストポーズとして適用
bpy.ops.pose.armature_apply()

# Armatureモディファイアを追加し直す
bpy.ops.object.mode_set(mode='OBJECT')

target_skin = bpy.data.objects[target_body_name]
mod = target_skin.modifiers.new(name=armature_name, type='ARMATURE')
mod.object = armature

print('done')
