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
  for line in input.split():
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
  
  def score(self):
    return 0
 
def parse_line(line):
  pass

 
def solve(data):
  score = 0
  for d in data:
    score += d.score()
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
  
