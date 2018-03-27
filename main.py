import sys
from bot import *

groupid = ''

if __name__ == '__main__':
  global groupid
  if sys.argv[1] == 'test':
    groupid = testgroup
  elif sys.argv[1] == 'news':
    groupid = bzsgroup
  init_bot()
  run_bot()