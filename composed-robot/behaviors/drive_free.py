from ..arbitration.behaviour import Behaviour


class DriveFree(Behaviour):
    def _update(self, distances):
        return (True,200, 0)