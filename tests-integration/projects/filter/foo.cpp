#include "foo.h"

int implication(int x, int y)
{
  // lobster-trace: softreq_example.req_implication
  return (x == 0) || (y != 0);
}

int exclusive_or(int x, int y)
{
  // lobster-trace: softreq_example.req_xor
  return (x == 0) != (y == 0);
}
