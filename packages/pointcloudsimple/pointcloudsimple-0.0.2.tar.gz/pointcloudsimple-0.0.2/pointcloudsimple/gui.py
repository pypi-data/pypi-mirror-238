import logging
import pygame

BACKGROUND_COLOUR = (47, 56, 112)
POINT_COLOUR = (227, 171, 129)

class GUI:
    def __init__(self, engine):
        self.logger = logging.getLogger('gui')
        self.engine = engine

        # Basic pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.engine.x_bound, self.engine.y_bound))
        pygame.display.set_caption("Point Cloud")
        self.clock = pygame.time.Clock()

        # Set up some constants for drawing
        self.max_line_distance = self.engine.x_bound * 0.1
        self.max_line_thickness = 7
        self.point_size = 10
        
        
        self.logger.info("Initialised")

    def run(self, steps=500):
        self.logger.info("Running")

        for _ in range(steps):
            self.engine.step()
            self.draw()

    def draw(self):
        self.logger.debug("Drawing")
        # Draw the points from  the engine onto the screen using pygame
        self.screen.fill(BACKGROUND_COLOUR)
        self.draw_points(self.engine.point_cloud)
        self.draw_lines(self.engine.point_cloud)
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def draw_points(self, points):
        for point in points:
            pygame.draw.circle(self.screen, POINT_COLOUR, point.get_pos_tuple(), self.point_size)
    
    def draw_lines(self, points):
        for point in points:
            for other_point in points:
                if point is other_point:
                    continue

                distance = self.engine.distance_between_points(point, other_point)
                if distance < self.max_line_distance:
                    line_thickness = int(-(0.05)*distance + self.max_line_thickness)
                    pygame.draw.line(self.screen, POINT_COLOUR, point.get_pos_tuple(), other_point.get_pos_tuple(), line_thickness)

    def __del__(self):
        self.logger.info("Quitting")
        pygame.quit()
