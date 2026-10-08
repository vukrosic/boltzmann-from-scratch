"""Step 6. Borrowing the rule. Shortest round trip through 60 towns: allow a worse step with chance e^(-rise / T)."""
import random
from math import exp, sqrt
from save import save


def dist(p, q):
    """Straight-line distance between two towns. Written out by hand instead of math.hypot: Python versions round
    hypot's last digit differently, and in 200,000 random tries one different digit changes the whole search.
    These few lines round the same way everywhere, so everybody gets the film's numbers."""
    dx, dy = abs(p[0] - q[0]), abs(p[1] - q[1])
    big = max(dx, dy)
    if big == 0:
        return 0.0
    total, lost = 1.0, 0.0
    for x in (dx, dy):
        x = (x / big) ** 2
        before = total
        total += x
        lost += (before - total) + x
    return big * sqrt(total - 1.0 + lost)


def length(towns, order):
    total = 0.0
    for i in range(len(order)):
        total += dist(towns[order[i]], towns[order[i - 1]])
    return total


def search(towns, tries, seed, t_start, t_end):
    """Pick two points of the trip and reverse the part between them. Keep it if shorter; if longer, keep it
    with chance e^(-rise / T). With t_start = 0 a longer trip is never kept."""
    rng = random.Random(seed)
    n = len(towns)
    order = list(range(n))
    cur = length(towns, order)
    best, best_order, uphill = cur, order[:], 0
    trace = []

    def d(a, b):
        return dist(towns[a], towns[b])

    for t in range(tries):
        if t % (tries // 200) == 0:
            trace.append(cur)
        temp = t_start * (t_end / t_start) ** (t / tries) if t_start > 0 else 0.0
        i, j = sorted(rng.sample(range(n), 2))
        if j - i < 1 or (i == 0 and j == n - 1):
            continue
        a, b, c, e = order[i - 1], order[i], order[j], order[(j + 1) % n]
        rise = d(a, c) + d(b, e) - d(a, b) - d(c, e)
        if rise < 0 or (temp > 0 and rng.random() < exp(-rise / temp)):
            if rise > 0:
                uphill += 1
            order[i:j + 1] = reversed(order[i:j + 1])
            cur += rise
            if cur < best:
                best, best_order = cur, order[:]
    return best, best_order, uphill, trace


N, TRIES = 60, 200_000
rng = random.Random(1983)
towns = [(rng.random(), rng.random()) for _ in range(N)]
start = length(towns, list(range(N)))
cold, cold_order, _, cold_trace = search(towns, TRIES, seed=1, t_start=0, t_end=0)
hot, hot_order, uphill, hot_trace = search(towns, TRIES, seed=1, t_start=0.3, t_end=0.001)
print(f'{N} towns scattered at random. Visiting them in the order they were listed: {start:.2f}.')
print(f'   never accept a longer trip: {cold:.3f} after {TRIES:,} tries')
print(f'   accept a longer trip with chance e^(-rise / T), T cooled from 0.3 to 0.001: {hot:.3f} '
      f'({100 * (cold - hot) / cold:.1f}% shorter), {uphill:,} longer trips accepted on the way')

wins, gains, colds, hots = 0, [], [], []
for s in range(20):
    r2 = random.Random(100 + s)
    tw = [(r2.random(), r2.random()) for _ in range(N)]
    c = search(tw, TRIES, seed=s, t_start=0, t_end=0)[0]
    h = search(tw, TRIES, seed=s, t_start=0.3, t_end=0.001)[0]
    colds.append(c)
    hots.append(h)
    wins += h < c - 1e-9
    gains.append(100 * (c - h) / c)
print(f'   20 other maps: cooling won on {wins}; average trip {sum(colds) / 20:.3f} against {sum(hots) / 20:.3f}; '
      f'average gain {sum(gains) / 20:.1f}%, best {max(gains):.1f}%, worst {min(gains):.1f}%')

save(6, n=N, tries=TRIES, towns=towns, start=start, cold=cold, hot=hot, cold_order=cold_order, hot_order=hot_order,
     uphill=uphill, cold_trace=cold_trace, hot_trace=hot_trace, gain=100 * (cold - hot) / cold, wins=wins,
     gains=gains, cold_mean=sum(colds) / 20, hot_mean=sum(hots) / 20)
