#include <stdint.h>
#include <assert.h>

int main()
{
  uint32_t a = 446374322 >> 5;
  uint32_t b = 2269612274 >> 6;
  double x = (a * 67108864.0 + b) * (1.0 / 9007199254740992.0);

  // We only know x. Goal is to recover a and b.
  // Note: 9007199254740992 == 2 ** 53
  // Note: 67108864 == 2 ** 26
  uint64_t y = (uint64_t)(x * 9007199254740992.0);
  assert(((uint64_t)a * 67108864 + b) == y);

  uint32_t a_recovered = y >> 26;
  uint32_t b_recovered = y & 0x3ffffff; // y % (2 ** 26)
  assert(a == a_recovered);
  assert(b == b_recovered);

  return 0;
}
