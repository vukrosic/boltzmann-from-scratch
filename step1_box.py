"""Step 1. A box with two halves. Each tick, one particle picked at random hops to the other half."""
import random
from save import save

MARKS = [0, 10, 100, 1_000, 10_000, 100_000, 1_000_000]


def run(n, ticks, seed):
    rng = random.Random(seed)
    left = [True] * n                      # every particle starts in the left half
    count = n
    marks, track, back_home = {}, [], 0
    low, high = n, 0
    for t in range(ticks + 1):
        if t in MARKS:
            marks[str(t)] = count
        if t <= 600:
            track.append(count)
        if t > 0 and count == n:
            back_home += 1                 # all of them on the left again
        if t >= 20 * n:                    # after the mixing: how far does the count wander?
            low, high = min(low, count), max(high, count)
        i = rng.randrange(n)
        count += -1 if left[i] else 1
        left[i] = not left[i]
    return dict(n=n, marks=marks, track=track, back_home=back_home, low=low, high=high)


out = {}
for n in (10, 100, 10_000):
    r = run(n, 1_000_000, seed=n)
    out[str(n)] = r
    print(f'{n:,} particles, all start on the left')
    print('   left side after ' + ', '.join(f'{int(t):,} ticks: {c:,}' for t, c in r['marks'].items()))
    print(f'   back to "all on the left" {r["back_home"]:,} times in a million ticks')
    print(f'   after mixing the left side holds between {r["low"]:,} and {r["high"]:,} '
          f'({100 * r["low"] / n:.1f}% to {100 * r["high"] / n:.1f}%)')
save(1, **out)
