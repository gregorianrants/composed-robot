# import math


# def min_left(distances):
#     return min(distances[0], distances[1])


# def min_right(distances):
#     return min(distances[3], distances[4])


# def min_all(distances):
#     return min(*distances)


# # TRANSITIONS = {
# #     "DRIVE_FREE_TO_AVOID_SIDE": 50,
# #     "AVOID_SIDE_TO_DRIVE_FREE": 90,
# #     "DIFFERENCE_TO_SWITCH_SIDE": 10,
# # }


# class AvoidSide:
#     def __init__(self, side):
#         if side == "left":
#             self.min_this_side = min_left
#             self.min_other_side = min_right
#             self.avoidance_rotation_direction = 1
#             self.side = "left"
#             self.other_side = "right"
#         if side == "right":
#             self.min_this_side = min_right
#             self.min_other_side = min_left
#             self.avoidance_rotation_direction = -1
#             self.side = "right"
#             self.other_side = "left"

#     def proportion_across_zone(self, distance):
#         return (TRANSITIONS["AVOID_SIDE_TO_DRIVE_FREE"] - distance) / TRANSITIONS[
#             "AVOID_SIDE_TO_DRIVE_FREE"
#         ]

#     def update_state(self, distances):
#         if min_all(distances) > TRANSITIONS["AVOID_SIDE_TO_DRIVE_FREE"]:
#             return DriveFree()
#         if (
#             self.min_other_side(distances)
#             < self.min_this_side(distances) - TRANSITIONS["DIFFERENCE_TO_SWITCH_SIDE"]
#         ):
#             return AvoidSide(self.other_side)
#         return self

#     def radians_per_second(self, distance):
#         rotations_per_second = self.proportion_across_zone(distance) * 0.5
#         radians_per_second = rotations_per_second * (2 * math.pi)
#         return radians_per_second * self.avoidance_rotation_direction

#     def get_velocities(self, distances):
#         # should maybe changes this as the closest distance may not be on side we are avoiding
#         translation = (1 - self.proportion_across_zone(min_all(distances))) * 300
#         rotation = self.radians_per_second(min_all(distances))
#         return (translation, rotation)

#     def __str__(self):
#         return f"State: Avoid-{self.side}"


# class DriveFree:
#     def __init__(self):
#         self.transition_avoid_side = 50


#     def get_velocities(self):
#         pass

#     def update_state(self, distances):
#         if min_all(distances) > self.transition_avoid_side:
#             return self
#         if min_left(distances) < min_right(distances):
#             return AvoidSide("left")
#         else:
#             return AvoidSide("right")

#     def get_velocities(self, distances):
#         return (300, 0)

#     def __str__(self) -> str:
#         return "State: DriveFree"


# class State:
#     def __init__(self):
#         self.state = DriveFree()
#         print("yahhhhhhhhhhhhhhhhhhhh")

#     def update_state(self, distances):
#         self.state = self.state.update_state(distances)

#     def get_velocities(self, distances):
#         return self.state.get_velocities(distances)


# print(min_all([1,2,3,4]))

# state = State()
# print(state.state)
# state.update_state([10,10,100,50,50])
# print(state.state)
# print(state.get_velocities([10,10,100,50,50]))
# state.update_state([70,70,100,50,50])
# print(state.state)
# state.update_state([200,200,100,200,200])
# print(state.state)

import math


def min_left(distances):
    return min(distances[0], distances[1])


def min_right(distances):
    return min(distances[3], distances[4])


def min_all(distances):
    return min(*distances)


TRANSITIONS = {
    "DRIVE_FREE_TO_AVOID_SIDE": 30,
    "AVOID_SIDE_TO_DRIVE_FREE": 50,
    "DIFFERENCE_TO_SWITCH_SIDE": 7,
}


class AvoidSide:
    def __init__(self, side):
        if side == "left":
            self.min_this_side = min_left
            self.min_other_side = min_right
            self.avoidance_rotation_direction = 1
            self.side = "left"
            self.other_side = "right"
        if side == "right":
            self.min_this_side = min_right
            self.min_other_side = min_left
            self.avoidance_rotation_direction = -1
            self.side = "right"
            self.other_side = "left"

    def proportion_across_zone(self, distance):
        return (TRANSITIONS["AVOID_SIDE_TO_DRIVE_FREE"] - distance) / TRANSITIONS[
            "AVOID_SIDE_TO_DRIVE_FREE"
        ]

    def update_state(self, distances):
        if min_all(distances) > TRANSITIONS["AVOID_SIDE_TO_DRIVE_FREE"]:
            return DriveFree()
        if (
            self.min_other_side(distances)
            < self.min_this_side(distances) - TRANSITIONS["DIFFERENCE_TO_SWITCH_SIDE"]
        ):
            return AvoidSide(self.other_side)
        return self

    def radians_per_second(self, distance):
        rotations_per_second = self.proportion_across_zone(distance) * 0.25
        radians_per_second = rotations_per_second * (2 * math.pi)
        return radians_per_second * self.avoidance_rotation_direction

    def get_velocities(self, distances):
        # should maybe changes this as the closest distance may not be on side we are avoiding
        translation = (1 - self.proportion_across_zone(min_all(distances))) * 200
        rotation = self.radians_per_second(min_all(distances))
        return (translation, rotation)

    def __str__(self):
        return f"State: Avoid-{self.side}"


class DriveFree:
    def __init__(self):
        self.transition_avoid_side = 50

    def get_velocities(self):
        pass

    def update_state(self, distances):
        if min_all(distances) > self.transition_avoid_side:
            return self
        if min_left(distances) < min_right(distances):
            return AvoidSide("left")
        else:
            return AvoidSide("right")

    def get_velocities(self, distances):
        return (200, 0)

    def __str__(self) -> str:
        return "State: DriveFree"


class State:
    def __init__(self):
        self.state = DriveFree()
        print("yahhhhhhhhhhhhhhhhhhhh")

    def update_state(self, distances):
        self.state = self.state.update_state(distances)

    def get_velocities(self, distances):
        return self.state.get_velocities(distances)


# print(min_all([1,2,3,4]))

# state = State()
# print(state.state)
# state.update_state([10,10,100,50,50])
# print(state.state)
# print(state.get_velocities([10,10,100,50,50]))
# state.update_state([70,70,100,50,50])
# print(state.state)
# state.update_state([200,200,100,200,200])
# print(state.state)
