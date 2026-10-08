"""Step 5. Air. Height costs energy, so the same multiplier thins the air as you climb."""
import random
from math import exp
from save import save

K = 1.380649e-23            # Boltzmann constant, joules per kelvin
AVOGADRO = 6.02214076e23    # molecules in a mole
MOLAR_MASS = 0.0289644      # kilograms in a mole of air
G = 9.80665                 # metres per second squared
MASS = MOLAR_MASS / AVOGADRO        # one air molecule, kilograms
T0 = 288.15                 # 15 degrees Celsius, in kelvin
EVEREST = 8848.86


def multiplier(metres, temp):
    """Share of the air that is left after climbing this many metres at this temperature."""
    return exp(-MASS * G * metres / (K * temp))


def colder_with_height(top, drop_per_m=0.0065, step=1.0):
    """The same rule, one metre at a time, while the temperature falls 6.5 degrees per kilometre."""
    share, h = 1.0, 0.0
    while h < top - 1e-9:
        d = min(step, top - h)
        share *= multiplier(d, T0 - drop_per_m * (h + d / 2))
        h += d
    return share


print(f'One air molecule weighs {MASS:.3e} kilograms.')
print(f'Lifting it 1 km costs {MASS * G * 1000:.3e} joules. Its heat energy scale at 15 C, k times T, is {K * T0:.3e} joules.')
per_km = multiplier(1000, T0)
print(f'So each kilometre up multiplies the air by {per_km:.3f}. Height for 1/e of the air: {K * T0 / (MASS * G):,.0f} m.')
rows = []
for name, h in (('5,500 m', 5500), ('8,000 m', 8000), ('Everest', EVEREST), ('11,000 m', 11000)):
    one, cold = multiplier(h, T0), colder_with_height(h)
    rows.append(dict(name=name, h=h, one=one, cold=cold, mbar_one=1013.25 * one, mbar_cold=1013.25 * cold))
    print(f'   {name:>9}: one temperature {100 * one:.1f}% ({1013.25 * one:.0f} mbar)   '
          f'colder with height {100 * cold:.1f}% ({1013.25 * cold:.0f} mbar)')

# the same thing by brute force: molecules that only know "a step up costs energy"
N, STEP, SWEEPS = 6000, 500.0, 4000
MARKS = [0, 10, 100, 1000, SWEEPS]
rng = random.Random(1906)
up = multiplier(STEP, T0)               # chance that a step up is allowed
h = [0] * N                             # heights in steps; all the air starts on the ground
profiles = {}
for sweep in range(SWEEPS + 1):
    if sweep in MARKS:
        layers = [0] * 12               # how many molecules in each 2 km layer, up to 24 km
        for v in h:
            if v * STEP < 24000:
                layers[int(v * STEP // 2000)] += 1
        profiles[sweep] = layers
    for i in range(N):
        if rng.random() < 0.5:
            if rng.random() < up:
                h[i] += 1
        elif h[i] > 0:
            h[i] -= 1
print(f'{N:,} molecules start on the ground. Each tries a {STEP:.0f} m step up or down; a step up is allowed with chance {up:.3f}.')
for s in MARKS:
    print(f'   after {s:>5,} rounds, molecules in each 2 km layer: {profiles[s][:8]}')
last = profiles[SWEEPS]
measured = [last[i + 1] / last[i] for i in range(4)]
print(f'   layer to layer the count is multiplied by: ' + ', '.join(f'{r:.2f}' for r in measured)
      + f'   (the rule for 2 km: {multiplier(2000, T0):.2f})')
above = sum(1 for v in h if v * STEP >= EVEREST) / N
print(f'   share of molecules above the height of Everest: {100 * above:.1f}% (the rule: {100 * multiplier(EVEREST, T0):.1f}%)')

save(5, mass=MASS, lift_km=MASS * G * 1000, kt=K * T0, per_km=per_km, scale=K * T0 / (MASS * G), rows=rows,
     n=N, step_m=STEP, up=up, marks=MARKS, profiles={str(k): v for k, v in profiles.items()}, measured=measured,
     rule2km=multiplier(2000, T0), above=above, above_rule=multiplier(EVEREST, T0))
