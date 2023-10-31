import osmium


class WayCounter(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.count = 0

    def way(self, w) -> None:
        self.count += 1


class PointCounter(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.count = 0

    def point(self, p) -> None:
        self.count += 1


class NodeCounter(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.count = 0

    def node(self, n) -> None:
        self.count += 1
