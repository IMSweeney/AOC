import utils
import os

import aocd

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


valid = {
  'one': 1,
  'two': 2,
  'three': 3,
  'four': 4,
  'five': 5,
  'six': 6,
  'seven': 7,
  'eight': 8,
  'nine': 9,
}
valid.update({str(i): i for i in range(1, 10)})

def parse(input):
  parts = []
  for line in input.split():
    line = line.strip()
    if not line:
      continue
    log.debug(f'{line=}')

    ints = []
    for i in range(len(line)):
      for k in valid:
        if line[i:].startswith(k):
          ints.append(valid[k])
    log.debug(f'{ints=}')
    parts.append(ints)
  return parts
 
def solve(data):
  s = 0
  for ints in data:
    a = int(f'{ints[0]}{ints[-1]}')
    log.debug(f'{a=}')
    s += a
  return s
  

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
  
