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
  for line in input.split('\n'):
    line = line.strip()
    if not line:
      continue
    log.debug(f'{line=}')
    parsed = parse_line(line)
    log.debug(f'{parsed=}')
    parts.append(parsed)
  return parts


@dataclass
class Parsed:
  id: int
  l: list
  r: list
  
  def score(self):
    scoring = set(self.r).intersection(set(self.l))
    if scoring:
      return 2 ** (len(list(scoring)) - 1)
    else:
      return 0
 
def parse_line(line):
  id, dat = line.split(': ')
  id = id.split()[1]
  l, r = dat.split('|')
  l = [int(c) for c in l.split() if c.strip()]
  r = [int(c) for c in r.split() if c.strip()]
  return Parsed(id, l, r)

 
def solve(data):
  score = 0
  for d in data:
    s = d.score()
    log.info(f'{d}, scored {s}')
    score += s
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
  
