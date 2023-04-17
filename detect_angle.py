import bpy
import math
import mathutils

left_arm_bone_name = "Left arm"
right_arm_bone_name = "Right arm"
target_angle = 45


def detect_angle(left_arm_bone_name:str, right_arm_bone_name:str, target_angle):

    # 左腕と右腕のボーンを取得
    left_arm_bone = bpy.context.object.pose.bones.get(left_arm_bone_name)
    right_arm_bone = bpy.context.object.pose.bones.get(right_arm_bone_name)

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