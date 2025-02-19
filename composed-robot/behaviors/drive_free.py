from ..arbitration.behaviour import Behaviour


class DriveFree(Behaviour):
    def update(self, distances):
        return self._update(True,200, 0)