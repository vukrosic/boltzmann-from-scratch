"""Step 3. Loschmidt's test. Discs that bounce by the exact laws of motion; then every velocity is turned around."""
import random
from math import comb, cos, log, pi, sin, sqrt
from save import save

W, H, R, N = 2.0, 1.0, 0.01, 40           # box 2 by 1, disc radius, number of discs
T, DT = 3.0, 0.05                         # run length and the time between saved pictures
T_LONG = 10.0                             # a longer run, to see how far exact reversal can go


def start(seed=3):
    rng = random.Random(seed)
    discs = []
    for i in range(N):                     # a grid of 5 by 8 in the left half, each disc with speed 1 in a random direction
        a = rng.uniform(0, 2 * pi)
        discs.append([0.1 + 0.2 * (i % 5), 0.0625 + 0.125 * (i // 5), cos(a), sin(a)])
    return discs


def next_event(d):
    """Time to the next bounce, and what bounces: ('wall', i, axis) or ('pair', i, j)."""
    best, what = 1e18, None
    for i, (x, y, vx, vy) in enumerate(d):
        for axis, p, v, size in ((0, x, vx, W), (1, y, vy, H)):
            if v > 0:
                t = (size - R - p) / v
            elif v < 0:
                t = (R - p) / v
            else:
                continue
            if t < best:
                best, what = t, ('wall', i, axis)
        for j in range(i + 1, N):
            dx, dy, ux, uy = d[j][0] - x, d[j][1] - y, d[j][2] - vx, d[j][3] - vy
            b = dx * ux + dy * uy
            if b >= 0:
                continue                   # moving apart
            uu = ux * ux + uy * uy
            disc = b * b - uu * (dx * dx + dy * dy - 4 * R * R)
            if disc <= 0:
                continue                   # they miss
            t = (-b - sqrt(disc)) / uu
            if t < best:
                best, what = t, ('pair', i, j)
    return max(best, 0.0), what


def run(d, total=T):
    """Move the discs for `total` seconds. Returns the saved pictures, the number of disc-to-disc bounces and a disc from the last one."""
    t, k, frames, bounces, last = 0.0, 0, [], 0, 0
    while True:
        dt, what = next_event(d)
        while k * DT <= min(t + dt, total) + 1e-12:          # save the pictures that fall before the bounce
            s = k * DT - t
            frames.append([(x + vx * s, y + vy * s) for x, y, vx, vy in d])
            k += 1
        if t + dt >= total:
            s = total - t
            for p in d:
                p[0] += p[2] * s
                p[1] += p[3] * s
            return frames, bounces, last
        for p in d:
            p[0] += p[2] * dt
            p[1] += p[3] * dt
        t += dt
        if what[0] == 'wall':
            d[what[1]][2 + what[2]] *= -1
        else:
            a, b = d[what[1]], d[what[2]]
            nx, ny = (b[0] - a[0]) / (2 * R), (b[1] - a[1]) / (2 * R)
            push = (b[2] - a[2]) * nx + (b[3] - a[3]) * ny     # equal discs swap their speed along the line of centres
            a[2] += push * nx; a[3] += push * ny
            b[2] -= push * nx; b[3] -= push * ny
            bounces += 1
            last = what[1]


def left(frame):
    return sum(1 for x, _ in frame if x < W / 2)


def miss(d, home):
    return sum(sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) for p, q in zip(d, home)) / N


home = start()
d = [p[:] for p in home]
fwd, bounces, last = run(d)
mixed = [p[:] for p in d]
print(f'{N} discs start in the left half. {T:.0f} seconds, {bounces} bounces between discs.')
print('   on the left each second:', [left(fwd[int(s / DT)]) for s in range(int(T) + 1)])
print(f'   log W goes from {log(comb(N, left(fwd[0]))):.1f} to {log(comb(N, left(fwd[-1]))):.1f}')

rows, tracks = [], {}
for nudge in (0.0, 1e-12, 1e-9, 1e-6, 1e-3):
    d = [[x, y, -vx, -vy] for x, y, vx, vy in mixed]          # turn every velocity around
    d[last][2] += nudge                                        # and change one disc's speed by this much
    back, _, _ = run(d)
    rows.append([nudge, left(back[-1]), miss(d, home)])
    tracks[str(nudge)] = back
    print(f'   turned around, one disc nudged by {nudge:g}: {left(back[-1])} of {N} end on the left; '
          f'average distance from the starting places {miss(d, home):.2g}')

# The computer itself rounds every number at about the 16th digit. That is a nudge too. How long can a run be?
limit = []
for total in (1.0, 2.0, 3.0, 4.0, 5.0, 7.0, T_LONG):
    d = [p[:] for p in home]
    _, n, _ = run(d, total)
    d = [[x, y, -vx, -vy] for x, y, vx, vy in d]
    back, _, _ = run(d, total)
    limit.append([total, n, left(back[-1]), miss(d, home)])
    print(f'   no nudge at all, {total:.0f} seconds each way, {n} bounces: {left(back[-1])} of {N} end on the left; '
          f'average distance {miss(d, home):.2g}')

rnd = lambda fr: [[round(x, 4), round(y, 4)] for x, y in fr]
save(3, n=N, r=R, w=W, h=H, T=T, dt=DT, bounces=bounces, rows=rows, limit=limit, nudged_disc=last,
     left_fwd=[left(f) for f in fwd], logw=[log(comb(N, left(f))) for f in fwd],
     fwd=[rnd(f) for f in fwd], back=[rnd(f) for f in tracks['0.0']], back_nudged=[rnd(f) for f in tracks['1e-06']],
     left_back=[left(f) for f in tracks['0.0']], left_nudged=[left(f) for f in tracks['1e-06']])
