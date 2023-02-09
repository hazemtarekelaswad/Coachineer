class Joint:
    def __init__(self, x: float, y: float, z: float, confidence: float):
        self.x = x
        self.y = y
        self.z = z
        self.confidence = confidence
    
    def parse(self, data: str):
        pass