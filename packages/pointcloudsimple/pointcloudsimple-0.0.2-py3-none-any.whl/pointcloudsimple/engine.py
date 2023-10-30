import logging
import numpy as np

class Point:
    def __init__(self, x_bound, y_bound, velocity_max=1, acceleration_max=0.05, acceleration_scale=0.1):
        self.pos = np.array([np.random.randint(0, x_bound), np.random.randint(0, y_bound)], dtype=np.float32)
        self.velocity = np.array([0, 0], dtype=np.float32)
        self.acceleration = np.array([0, 0], dtype=np.float32)
        self.x_bound = x_bound
        self.y_bound = y_bound
        self.acceleration_scale = acceleration_scale
        self.acceleration_max = acceleration_max
        self.velocity_max = velocity_max
    
    def step(self):
        self.pos += self.velocity
        self.pos[0] = self.pos[0] % self.x_bound
        self.pos[1] = self.pos[1] % self.y_bound
        self.velocity = np.clip(self.velocity + self.acceleration, -self.velocity_max, self.velocity_max)
        self.acceleration = np.clip(self.acceleration + np.random.normal(size=(2,)), -self.acceleration_max, self.acceleration_max)
    
    def get_pos_tuple(self):
        return (int(self.pos[0]), int(self.pos[1]))

    @staticmethod
    def _clip(value, bound):
        return np.clip(value, -bound, bound)
    
class Engine:
    def __init__(self, x_bound, y_bound, number_of_points=100):
        self.logger = logging.getLogger('engine')
        self.logger.info("Initialised")
        self.x_bound = x_bound
        self.y_bound = y_bound

        self.point_cloud = [Point(x_bound, y_bound) for _ in range(number_of_points)]
        self.logger.info("Created point cloud")

    def step(self):
        self.logger.debug("Stepping")
        for point in self.point_cloud:
            point.step()

    @staticmethod
    def distance_between_points(point1, point2):
        return np.linalg.norm(point1.pos - point2.pos)