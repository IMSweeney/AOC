import shutil
import aocd
import os

YEAR = 2023
day = 3

if __name__ == "__main__":
    os.makedirs(f"{YEAR}", exist_ok=True)
    patha = f"{YEAR}/{day}a.py"
    pathb = f"{YEAR}/{day}b.py"
    if not os.path.exists(patha):
      print(f'copy template file for {patha}')
      shutil.copyfile("template.py", patha)
    elif not os.path.exists(pathb):
      print(f'copy part a file to {pathb}')
      shutil.copyfile(patha, pathb)
    else:
      print('already created part a and part b files for day {day}, please pick a new day')
