from collections.abc import Callable
from functools import wraps

from .tcr_color import color as c


def test(func: Callable) -> Callable:
  """A decorator for adding """
  @wraps(func)
  def wrapper(*args, **kwargs):
    name = func.__name__
    print(f"""
{c('White')}####{len(name)*"#"}####
{""}### {c('Gold')}{    name     }{c('White')} ###
{""}####{len(name)*"#"}####{c('reset')}
"""[1:-1])
    return func(*args, **kwargs)

  return wrapper