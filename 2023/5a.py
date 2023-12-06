import utils
import os
from dataclasses import dataclass

import aocd

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def parse(input):
  parts = []
  lines = input.split('\n')
  
  seeds = lines.pop(0).split(': ')[1]
  seeds = [int(s) for s in seeds.split()]
  log.debug(f'{seeds=}')
  
  maps = {}
  k1, k2 = None, None
  ranges = []

  for line in lines:
    line = line.strip()
    if not line:
      continue
    log.debug(f'{line=}')
    
    if 'map' in line:
      if k1:
        maps[k1] = Map(k1, k2, ranges)
        k1, k2 = None, None
        ranges = []
      k1, k2 = line.split()[0].split('-to-')
    else:
      ranges.append(Range(*[int(i) for i in line.split()]))
    
  if k1:
    maps[k1] = Map(k1, k2, ranges)
  return seeds, maps


@dataclass
class Range:
  dst: int
  src: int
  length: int


@dataclass
class Map:
  k1: str
  k2: str
  ranges: list[Range]
  
  def find(self, key):
    for range in self.ranges:
      if key > range.src and key < range.src + range.length:
        break
    else:
      return key
    
    return range.dst + key - range.src

 
def solve(data):
  seeds, maps = data
  locations = []
  for s in seeds:
    key = 'seed'
    while key != 'location':
      map = maps[key]
      log.debug(f'looking for {s} in {map.k1}-{map.k2}')
      s = map.find(s)
      key = map.k2
      log.debug(f'found {s} in {key}')
    locations.append(s)
  return min(locations)

if __name__ == '__main__':
  year = int(__file__.split('/')[-2])
  day = int(__file__.split('/')[-1][0])
  part = __file__.split('/')[-1][1]
  log.debug(f'{year}-{day}{part}')
  
  puzzle = aocd.models.Puzzle(day=day, year=year)
  page = aocd.examples.Page.from_raw(puzzle._get_prose())
    
  log.info(f"--- Day {day}: {puzzle.title} ---")
  log.info(f'part: {part}')
  if part == 'a':
    example = page.a_pre[0]
    answer = int(page.a_code[-1])
  else:
    example = page.b_pre[0]
    answer = int(page.b_code[-1])
  
  data = parse(example)
  res = solve(data)
  assert answer == res, 'example failed'
  log.info('Example passed')
  
  input = puzzle.input_data
  data = parse(input)
  res = solve(data)
  
  if part == 'a':
    puzzle.answer_a = res
  else:
    puzzle.answer_b = res
  
