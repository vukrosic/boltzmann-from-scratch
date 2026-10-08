"""Step 7. The temperature knob of a chatbot is the same rule: chance = e^(score / T), shared out."""
import random
from math import exp
from save import save

# Example scores a language model might give to the next word after "The cat sat on the".
# These five scores are made up for the example; the rule applied to them is the real one.
WORDS = ['mat', 'sofa', 'floor', 'roof', 'moon']
SCORES = [5.0, 4.0, 3.5, 2.0, 0.0]


def softmax(scores, temp):
    w = [exp(s / temp) for s in scores]
    return [x / sum(w) for x in w]


def boltzmann(energies, temp):
    """Boltzmann's rule for sharing: chance proportional to e^(-energy / T)."""
    w = [exp(-e / temp) for e in energies]
    return [x / sum(w) for x in w]


rows = {}
print('Next word after "The cat sat on the", with example scores ' + ', '.join(f'{w} {s}' for w, s in zip(WORDS, SCORES)))
for temp in (0.2, 0.5, 1.0, 2.0, 5.0):
    p = softmax(SCORES, temp)
    b = boltzmann([-s for s in SCORES], temp)
    assert max(abs(x - y) for x, y in zip(p, b)) < 1e-12
    rng = random.Random(int(temp * 10))
    draws = rng.choices(WORDS, weights=p, k=1000)
    counts = [draws.count(w) for w in WORDS]
    rows[str(temp)] = dict(p=p, counts=counts, step=exp(-1 / temp), first20=draws[:20])
    print(f'   T = {temp}: ' + ', '.join(f'{w} {100 * x:.1f}%' for w, x in zip(WORDS, p))
          + f'   one point of score less multiplies the chance by {exp(-1 / temp):.3f}')
    print(f'            1,000 draws: ' + ', '.join(f'{w} {c}' for w, c in zip(WORDS, counts)))
print('   softmax of the scores and Boltzmann sharing with energy = minus the score: the same numbers to 12 places')

save(7, words=WORDS, scores=SCORES, rows=rows)
