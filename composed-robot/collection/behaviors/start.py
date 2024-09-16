class Start:
    def __init__(self, arbiter):
        self.count = 0
        self.priority = 100
        self.arbiter = arbiter

    def update(self, left_motor_data):
        if self.count < 6:
            print(f"lift off in {6-self.count}")
            self.count += 1
            self.arbiter.update(self, True, 0, 0)
        if self.count == 6:
            self.arbiter.update(self, False, 0, 0)
