import os
os.environ['AOC_SESSION'] = '53616c7465645f5f7130cb84c6121b9b1cda1dccdf9a49ec5be8cbb445f45003f4e91bf96caae31027cfd5d838613f3cac41427ecef373691bb93c41dccf67b5'

from dataclasses import dataclass

@dataclass
class Point2D:
  # top left 0,0
  x: int
  y: int
  
  def __hash__(self):
    return hash((self.x, self.y))

  def get_adj(self, max_x=None, max_y=None, corners=True):
    x, y = self.x, self.y
    pts = []
    if y > 0:
      pts.append(Point2D(x, y - 1))
      if corners and x > 0:
        pts.append(Point2D(x - 1, y - 1))
      if corners and x < max_x:
        pts.append(Point2D(x + 1, y - 1))
    if x > 0:
      pts.append(Point2D(x - 1, y))
    if x < max_x:
      pts.append(Point2D(x + 1, y))
    if y < max_y:
      pts.append(Point2D(x, y + 1))
      if corners and x > 0:
        pts.append(Point2D(x - 1, y + 1))
      if corners and x < max_x:
        pts.append(Point2D(x + 1, y + 1))
    return pts
      
