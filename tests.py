"""Checks. run_all.sh runs them last, on the numbers the seven steps saved in runs/."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
r = {i: json.load(open(os.path.join(HERE, 'runs', 'step%d.json' % i))) for i in range(1, 8)}

# 1. a small box comes back to "all on the left" often; a big one never does and stays near half and half
assert r[1]['10']['back_home'] > 100 and r[1]['100']['back_home'] == 0 and r[1]['10000']['back_home'] == 0
assert 4800 < r[1]['10000']['low'] and r[1]['10000']['high'] < 5200
assert abs(r[1]['10000']['marks']['1000000'] - 5000) < 150

# 2. the ways add up to every arrangement; near-even splits are almost all of them; logs of two boxes add
assert r[2]['by_left'] == [1, 4, 6, 4, 1] and abs(sum(r[2]['ways']) / r[2]['total'] - 1) < 1e-9
assert r[2]['shares']['40-60'] > 0.96 and r[2]['shares']['30-70'] > 0.9999
assert r[2]['logs'][100] == 0 and abs(r[2]['two_boxes'] - 2 * r[2]['logs'][50]) < 1e-9

# 3. the gas spreads; turned around with no nudge it all returns; a nudge of a millionth or a longer run breaks that
assert r[3]['left_fwd'][0] == 40 and r[3]['left_fwd'][-1] < 25 and r[3]['logw'][-1] > 20
assert r[3]['rows'][0][1] == 40 and r[3]['rows'][0][2] < 1e-6
assert r[3]['rows'][-1][1] < 40 and all(a[2] < b[2] for a, b in zip(r[3]['rows'], r[3]['rows'][1:]))
assert r[3]['limit'][2][2] == 40 and r[3]['limit'][-1][2] < 30
assert all(a[3] < b[3] for a, b in zip(r[3]['limit'], r[3]['limit'][1:]))

# 4. shared energy settles into "each unit more is rarer by one multiplier", the split with the most ways
assert abs(r[4]['mult'] - r[4]['q']) < 0.01 and r[4]['gap'] < 0.01
assert all(a <= b + 20 for a, b in zip(r[4]['logw'], r[4]['logw'][1:]))
c = r[4]['compare']
assert c['equal'] < c['bell'] < c['flat'] < c['run'] <= c['rule'] + 1
assert all(abs(h['ratio'] - h['rule']) < 0.02 for h in r[4]['hot'].values())
assert r[4]['hot']['1']['temp'] < r[4]['hot']['5']['temp'] < r[4]['hot']['20']['temp']

# 5. the air rule lands on the textbook numbers, and molecules that only know the rule build the same thinning
rows = {row['name']: row for row in r[5]['rows']}
assert abs(rows['11,000 m']['cold'] - 0.223) < 0.002          # standard atmosphere: 22.3% at 11,000 m
assert rows['Everest']['cold'] < 1 / 3 < rows['Everest']['one']
assert abs(rows['5,500 m']['cold'] - 0.5) < 0.01 and rows['8,000 m']['mbar_cold'] < 356.5
assert abs(r[5]['above'] - r[5]['above_rule']) < 0.02
assert all(abs(m - r[5]['rule2km']) < 0.1 for m in r[5]['measured'])

# 6. allowing worse steps while cooling finds a shorter trip, on this map and on most others
assert r[6]['hot'] < r[6]['cold'] < r[6]['start'] and r[6]['uphill'] > 1000
assert r[6]['wins'] >= 15 and r[6]['hot_mean'] < r[6]['cold_mean']
assert sorted(r[6]['hot_order']) == list(range(r[6]['n']))

# 7. the chatbot knob: low temperature picks the top word, high temperature flattens; the chances add to 1
p = {t: row['p'] for t, row in r[7]['rows'].items()}
assert p['0.2'][0] > 0.99 and p['5.0'][0] < 0.3 and all(abs(sum(x) - 1) < 1e-12 for x in p.values())
assert all(p[a][0] > p[b][0] for a, b in zip(('0.2', '0.5', '1.0', '2.0'), ('0.5', '1.0', '2.0', '5.0')))
assert all(abs(x[1] / x[0] - r[7]['rows'][t]['step']) < 1e-9 for t, x in p.items())
print('all checks passed')
