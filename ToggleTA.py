import bpy
import math
import mathutils


### 変数

target_angle = 45
target_body_name = bpy.context.active_object.name
armature_name = "Armature"
left_arm_name = "Left arm"
right_arm_name = "Right arm"

t_to_a = -1
a_to_t = 1
angle = 0.785398

def select_armature_and_posemode():
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    armature = bpy.data.objects[armature_name]
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    return armature


def check_angle_below(left_arm_name:str, right_arm_name:str, target_angle):

    # Armatureを選択し、ポーズモードにする
    select_armature_and_posemode()

    # 左腕と右腕のボーンを取得
    left_arm_bone = bpy.context.object.pose.bones.get(left_arm_name)
    right_arm_bone = bpy.context.object.pose.bones.get(right_arm_name)

    # 左腕のボーンの方向ベクトルを取得
    if left_arm_bone:
        left_arm_head = mathutils.Vector(left_arm_bone.head)
        left_arm_tail = mathutils.Vector(left_arm_bone.tail)
        left_arm_direction = (left_arm_tail - left_arm_head).normalized()

    # 右腕のボーンの方向ベクトルを取得
    if right_arm_bone:
        right_arm_head = mathutils.Vector(right_arm_bone.head)
        right_arm_tail = mathutils.Vector(right_arm_bone.tail)
        right_arm_direction = (right_arm_tail - right_arm_head).normalized()

    # 左腕と右腕のボーンの方向ベクトルの角度を計算
    if left_arm_bone and right_arm_bone:
        angle_left = left_arm_direction.angle((1, 0, 0))
        angle_right = right_arm_direction.angle((-1, 0, 0))

        # ボーンの方向ベクトルが指定角度以上傾いているかどうかを判定
        if math.degrees(angle_left) > target_angle:
            return False
        if math.degrees(angle_right) > target_angle:
            return False

    return True

# チェック処理
if check_angle_below(left_arm_name, right_arm_name, target_angle):
    angle = angle * t_to_a
else:
    angle = angle * a_to_t


# Armatureを選択し、ポーズモードにする
armature = select_armature_and_posemode()

# 左右の腕を回転
for bone_name in [left_arm_name, right_arm_name]:
    bone = armature.pose.bones[bone_name]

    # クォータニオンで回転を設定する。
    rotation_quat = mathutils.Quaternion((1, 0, 0), angle)
    bone.rotation_quaternion = rotation_quat

# オブジェクトモードに移行し、target_skinを選択する
bpy.ops.object.mode_set(mode='OBJECT')
target_skin = bpy.data.objects[target_body_name]

# Armatureモディファイアを適用する
armature_mod = target_skin.modifiers.get(armature_name)

# 選択解除
bpy.ops.object.select_all(action='DESELECT')

# ターゲットスキンの選択と適用
target_skin.select_set(True)
bpy.context.view_layer.objects.active = target_skin
if target_skin.data.shape_keys is None:
    bpy.ops.object.modifier_apply(modifier=armature_mod.name)
else:
    bpy.ops.sk.apply_mods_sk()

# ポーズモードに移行する
select_armature_and_posemode()

# レストポーズとして適用
bpy.ops.pose.armature_apply()

# Armatureモディファイアを追加し直す
bpy.ops.object.mode_set(mode='OBJECT')

target_skin = bpy.data.objects[target_body_name]
mod = target_skin.modifiers.new(name=armature_name, type='ARMATURE')
mod.object = armature

# 選択を元の状態に戻す
bpy.context.view_layer.objects.active = target_skin

print('Toggle T-A Pose Done.')
