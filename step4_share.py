"""Step 4. Sharing energy. Particles pass single units of energy at random. Which split of the energy wins?"""
import random
from math import exp, lgamma, log
from save import save


def log_ways(counts, n):
    """log W for a picture: how many particles hold 0, 1, 2, ... units. W = n! / (n0! n1! n2! ...)."""
    return lgamma(n + 1) - sum(lgamma(c + 1) for c in counts)


def share(n, each, ticks, seed, marks):
    rng = random.Random(seed)
    e = [each] * n                          # everyone starts with the same amount
    out = {}
    for t in range(ticks + 1):
        if t in marks:
            top = max(e)
            counts = [0] * (top + 1)
            for v in e:
                counts[v] += 1
            out[t] = (counts, log_ways(counts, n))
        i, j = rng.randrange(n), rng.randrange(n)
        if i != j and e[i] > 0:             # particle i hands one unit to particle j
            e[i] -= 1
            e[j] += 1
    return out


def fit(counts):
    """The multiplier from one level to the next, as a straight-line fit of log(count) against the level."""
    pts = [(k, log(c), c) for k, c in enumerate(counts) if c >= 30]
    sw = sum(w for _, _, w in pts)
    mk = sum(k * w for k, _, w in pts) / sw
    my = sum(y * w for _, y, w in pts) / sw
    slope = sum(w * (k - mk) * (y - my) for k, y, w in pts) / sum(w * (k - mk) ** 2 for k, _, w in pts)
    return exp(slope)


N, EACH = 10_000, 5
MARKS = [0, 10_000, 100_000, 1_000_000, 5_000_000]
res = share(N, EACH, MARKS[-1], seed=1877, marks=MARKS)
print(f'{N:,} particles, {EACH} units of energy each, {N * EACH:,} units in all. One unit moves per tick.')
for t in MARKS:
    counts, lw = res[t]
    print(f'   after {t:>9,} ticks: with 0 units {counts[0]:>5,}   with {EACH} units {counts[EACH]:>5,}   '
          f'richest holds {len(counts) - 1:>2}   log W = {lw:,.0f}')

final, lw_final = res[MARKS[-1]]
shares = [c / N for c in final]
ratios = [final[k + 1] / final[k] for k in range(8)]
mult = fit(final)
print('   share holding 0..8 units: ' + ', '.join(f'{100 * s:.1f}%' for s in shares[:9]))
print('   each step up, the share is multiplied by: ' + ', '.join(f'{r:.2f}' for r in ratios) + f'   (one fitted multiplier: {mult:.3f})')

# the rule that this shape follows: share(k) = (1 - q) * q**k, with q = mean / (mean + 1)
q = EACH / (EACH + 1)
rule = [(1 - q) * q ** k for k in range(len(final))]
print(f'   the rule (1 - q) q^k with q = {EACH}/{EACH + 1} = {q:.3f}: ' + ', '.join(f'{100 * s:.1f}%' for s in rule[:9]))
print(f'   largest gap between the run and the rule: {100 * max(abs(a - b) for a, b in zip(shares, rule)):.2f} points')

# is that shape really the one with the most ways? compare it with other splits of the same energy
flat = [0] * 11
for k in range(11):
    flat[k] = N // 11                       # everyone equally likely to hold 0..10: same mean of 5
flat[5] += N - sum(flat)
bell = [0] * 11
for k, w in zip(range(11), (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)):
    bell[k] = round(N * w / 1024)           # a bell around 5
bell[5] += N - sum(bell)
ideal = [round(N * r) for r in rule]
print(f'   log W: all equal 0   bell {log_ways(bell, N):,.0f}   flat {log_ways(flat, N):,.0f}   '
      f'the rule {log_ways(ideal, N):,.0f}   the run {lw_final:,.0f}')

# more energy per particle = hotter: the multiplier moves toward 1
hot = {}
for each in (1, 5, 20):
    counts, _ = share(N, each, 400_000 * each * each // 4 + 2_000_000, seed=each, marks=[400_000 * each * each // 4 + 2_000_000])[400_000 * each * each // 4 + 2_000_000]
    r = fit(counts)
    hot[each] = dict(zero=counts[0] / N, ratio=r, rule=each / (each + 1), temp=-1 / log(r))
    print(f'   {each:>2} units each: {100 * counts[0] / N:.1f}% hold nothing; multiplier {r:.3f} (rule {each / (each + 1):.3f}); '
          f'as e^(-1/T) that is T = {-1 / log(r):.2f}')

save(4, n=N, each=EACH, marks=MARKS, logw=[res[t][1] for t in MARKS], zero=[res[t][0][0] for t in MARKS],
     top=[len(res[t][0]) - 1 for t in MARKS],
     same=[res[t][0][EACH] if len(res[t][0]) > EACH else 0 for t in MARKS], hist={str(t): res[t][0][:31] for t in MARKS},
     shares=shares[:31], ratios=ratios, mult=mult, q=q, rule=rule[:31], gap=max(abs(a - b) for a, b in zip(shares, rule)),
     compare=dict(equal=0.0, bell=log_ways(bell, N), flat=log_ways(flat, N), rule=log_ways(ideal, N), run=lw_final),
     hot={str(k): v for k, v in hot.items()})
