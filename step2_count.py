"""Step 2. Count the ways. W = the number of arrangements that give the same picture."""
from math import comb, log, log10
from save import save

# four particles: every arrangement, written as L and R
four = [''.join('L' if (i >> k) & 1 else 'R' for k in range(4)) for i in range(16)]
by_left = [sum(1 for a in four if a.count('L') == k) for k in range(5)]
print('4 particles, 16 arrangements; ways to have 0..4 on the left:', by_left)

N = 100
ways = [comb(N, k) for k in range(N + 1)]
total = 2 ** N
print(f'{N} particles: {total:.3e} arrangements in all')
print(f'   all on the left: {ways[N]} way      50 and 50: {ways[50]:.3e} ways')
for a, b in ((45, 55), (40, 60), (35, 65), (30, 70)):
    share = sum(ways[a:b + 1]) / total
    print(f'   between {a} and {b} on the left: {100 * share:.2f}% of all arrangements')
shares = {f'{a}-{b}': sum(ways[a:b + 1]) / total for a, b in ((45, 55), (40, 60), (35, 65), (30, 70))}

# the wait for "all on the left", if the box tried a new arrangement a billion times a second
YEAR = 365.25 * 24 * 3600
wait_years = total / 1e9 / YEAR
print(f'   one arrangement in {total:.2e} is "all left"; at a billion arrangements a second that is one every {wait_years:.1e} years')
UNIVERSE = 13.8e9                       # age of the universe in years
print(f'   the universe is {UNIVERSE:.3g} years old: the wait is {wait_years / UNIVERSE:,.0f} times that')

# the logarithm: ways multiply, logarithms add
s = [log(w) for w in ways]
print(f'   log W: all left {s[N]:.2f}, 75 left {s[75]:.2f}, 50 left {s[50]:.2f}')
two_boxes = log(ways[50] * ways[50])
print(f'   two such boxes side by side: ways multiply to {ways[50] ** 2:.2e}; log W = {two_boxes:.2f} = {s[50]:.2f} + {s[50]:.2f}')

# a litre of air: the number of molecules (Loschmidt's number for a litre, see the sources)
LITRE = 2.6868e22
digits = LITRE * log10(2)
print(f'a litre of air, {LITRE:.2e} molecules: the chance that all sit in the left half is 1 in a number with {digits:.1e} digits')

save(2, four=four, by_left=by_left, ways=[float(w) for w in ways], total=float(total), mid=float(ways[50]),
     shares=shares, wait_years=wait_years, universes=wait_years / UNIVERSE, logs=s, two_boxes=two_boxes, litre=LITRE, digits=digits)
