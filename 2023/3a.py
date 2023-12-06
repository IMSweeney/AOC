import utils
import os
from dataclasses import dataclass

import aocd

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def parse(input):
  map = {}
  pns = []
  y = 0
  for line in input.split():
    line = line.strip()
    if not line:
      continue
    log.debug(f'{line=}')
    x = 0
    pns += parse_line(line, y)
    for c in line:
      map[utils.Point2D(x, y)] = c
      x+=1
    y+=1
  return map, pns


@dataclass
class PN:
  pts: list[utils.Point2D]
  num: int


def parse_line(line, y):
  pns = []
  pn = []
  pts = []
  for x, c in enumerate(line):
    if c.isdigit():
      pn.append(c)
      pts.append(utils.Point2D(x, y))
    elif pn:
      pn = int(''.join(pn))
      pns.append(PN(pts, pn))
      pn = []
      pts = []
      
  if pn:
    pn = int(''.join(pn))
    pns.append(PN(pts, pn))
  return pns


def is_pn(data, pn, max_x, max_y):
  to_check = set([
    adj
    for pt in pn.pts
    for adj in pt.get_adj(max_x=max_x, max_y=max_y)
  ])
    
  for pt in to_check:
    val = data[pt]
    if not val.isdigit() and val != '.':
      return True
  return False
 
 
def solve(data):
  data, pns = data
  score = 0
  max_x = max([loc.x for loc in data])
  max_y = max([loc.y for loc in data])
  log.info(f'bounds: {max_x}, {max_y}')
  
  for pn in pns:
    log.debug(f'checking {pn}')
    if is_pn(data, pn, max_x, max_y):
      score += pn.num
      log.debug(f'{pn.num} is valid')
    else:
      to_check = set([
        adj for pt in pn.pts
        for adj in pt.get_adj(max_x=max_x, max_y=max_y)
      ])
      num_len = len(str(pn.num))
      log.debug(f'failed {pn}')
      
  return score

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
  
