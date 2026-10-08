# Boltzmann from scratch

Code for the video **Become Ludwig Boltzmann in 17 Minutes**.
Milk mixes into coffee and never unmixes, yet every single hit between two atoms can run backward. In 1877 Ludwig Boltzmann answered with counting: a mixed picture can be made in far more ways than a tidy one.
These seven small programs test that idea, then follow the same rule into air pressure, a route puzzle and a chatbot's temperature dial. 537 lines of Python 3, standard library only, nothing to install.

```bash
python3 tests.py      # checks every step
./run_all.sh          # runs all seven, about 4 minutes; expected output is in demo-output.txt
```

| File | Idea | What the run shows |
| --- | --- | --- |
| `step1_box.py` | A box with two halves | One random particle hops per tick. 10 particles return to "all on the left" 984 times in a million ticks. 100 particles never do and stay between 28 and 73 on the left. 10,000 stay between 4,850 and 5,164. |
| `step2_count.py` | Count the ways | 100 particles: 1 way to be all left, 1.009e+29 ways to be 50 and 50. 96.48% of all arrangements have 40 to 60 on the left. At a billion arrangements a second, "all left" comes up once in 2,911 ages of the universe. For a litre of air the odds are 1 in a number with 8.1e+21 digits. |
| `step3_reverse.py` | Run the film backward | 40 bouncing discs spread from the left half: 40, 27, 17, 16 on the left. Turn every speed around and all 40 come back. Nudge one disc by a millionth and 39 come back; by a thousandth, 36. |
| `step4_share.py` | Sharing energy | 10,000 particles pass single units of energy at random. From 5 units each they settle to 1,667 holding nothing, 660 holding 5, the richest 52. Each step up the ladder multiplies the share by about 0.833: the rule e^(-energy / T). |
| `step5_air.py` | The same rule in air | Height costs energy, so each kilometre up multiplies the air by 0.888. On top of Everest: 35.0% of sea-level air at one temperature, 31.0% with colder air higher up. 6,000 hopping molecules give 34.4% above that height. |
| `step6_anneal.py` | Borrowing the rule | Round trip through 60 towns. Never accepting a longer trip: 6.854. Accepting one with chance e^(-rise / T) while T cools: 6.230, 9.1% shorter. On 20 other maps cooling wins 18 times, by 6.3% on average. |
| `step7_softmax.py` | A chatbot's temperature | Five example scores for the next word. T = 0.2: "mat" in 992 of 1,000 draws. T = 5: "moon" in 113. The chatbot formula and Boltzmann's, with energy = minus the score, agree to 12 places. |

`save.py` writes each step's numbers to `runs/`, and the animation reads them from there, so every number on screen comes from these runs.

`step6_anneal.py` writes its distance function out by hand instead of calling `math.hypot`. Python versions round the last digit of `hypot` differently, and in 200,000 random tries one different digit changes the whole search. With the hand-written version Python 3.9, 3.12 and 3.13 print the same trips.

## What this is not

- The boxes hold at most 10,000 particles and the gas has 40 discs. A litre of air has about 2.7e+22 molecules. The idea is tested small.
- `step3_reverse.py` comes back because the computer keeps 16 digits. After about 5 seconds of bouncing even that is not enough, with no nudge at all.
- `step5_air.py` is still air: no wind, no weather. The mountain numbers are for a standard day.
- `step6_anneal.py` finds short trips, not the shortest. Nobody checked the best possible trip for these maps, and on 2 of the 20 maps cooling lost (by 1.3% and 0.2%).
- `step7_softmax.py` uses five made-up scores. No real chatbot was run.
- Why the universe started in a picture with so few ways is not answered here. Physicists have ideas and no settled answer.
