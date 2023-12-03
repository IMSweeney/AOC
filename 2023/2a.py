import utils
from dataclasses import dataclass

import aocd

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


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
  rounds: list


def parse_line(line):
  id, rounds = line.split(': ')
  id = int(id.replace('Game ', ''))
  
  p_rounds = []
  for round in rounds.split('; '):
    cubes = round.split(', ')
    p_round = {}
    for cube in cubes:
      num, key = cube.split()
      p_round[key] = int(num)
    p_rounds.append(p_round)
  return Parsed(id=id, rounds=p_rounds)

 
def solve(data):
  score = 0
  max = {'red': 12, 'green': 13, 'blue': 14}
  for game in data:
    for round in game.rounds:
      if any([round[k] > max[k] for k in round]):
        log.info(f'impossible round: {round}')
        break  
    else:
      log.info(f'scoring {game}')
      score += game.id
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
  
