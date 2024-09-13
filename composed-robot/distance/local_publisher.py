from .rangers import RangersGenerator

rg = RangersGenerator()


def rangers_generator():
    for distances in rg.start():
        yield ("distances", "local", distances)


# for distance in rangers_generator():
#     print(distance)
