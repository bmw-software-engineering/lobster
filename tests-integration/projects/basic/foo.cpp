#include "foo.h"

int implication(int x, int y)
{
  // lobster-trace: example.req_implication
  return (x == 0) || (y != 0);
}

int exclusive_or(int x, int y)
{
  return (x == 0) != (y == 0);
}

int potato(int x, int y)
{
  // lobster-trace: example.doesnt_exist
  return x < y;
}
