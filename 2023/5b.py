import utils
import os
from dataclasses import dataclass
from bisect import bisect_right

import aocd

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def parse(input):
  parts = []
  lines = input.split('\n')
  
  seeds_line = lines.pop(0).split(': ')[1]
  seeds = []
  seed_start = None
  for s in seeds_line.split():
    if not seed_start:
      seed_start = int(s)
    else:
      seeds.append((seed_start, int(s)))
      seed_start = None

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
        maps[k1] = Map(k1, k2, sorted(ranges, key=lambda x: x.src))
        k1, k2 = None, None
        ranges = []
      k1, k2 = line.split()[0].split('-to-')
    else:
      ranges.append(Range(*[int(i) for i in line.split()]))
    
  if k1:
    maps[k1] = Map(k1, k2, sorted(ranges, key=lambda x: x.src))
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
    i = bisect_right(self.ranges, key, key=lambda x: x.src)
    range = self.ranges[i - 1]
    if key < range.src or key > range.src + range.length:
      return key
    return range.dst + key - range.src

 
def solve(data):
  seeds, maps = data
  location_min = None
  for s_start, s_len in seeds:
    log.info(f'working on seeds {s_start}, {s_len}')
    for s in range(s_start, s_start + s_len):
      key = 'seed'
      msg = f'seed-{s} / {s_start + s_len}'
      while key != 'location':
        map = maps[key]
        s = map.find(s)
        key = map.k2
        # msg += f'{key[:3]} {s}, '
      log.debug(msg)
      if not location_min or s < location_min:
        location_min = s
        assert location_min > 0
      
  return location_min


def tests():
  m = Map('light', 'b', [
    Range(81, 45, 19),
    Range(68, 64, 13),
    Range(45, 77, 23),
  ])
  assert m.find(77) == 45
  assert m.find(78) == 46
  assert m.find(1) == 1


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
    example = page.a_pre[0]
    answer = 46
  
  tests()
  
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
  
