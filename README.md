# Where should you aim in darts?

Code for episode 1 of [The Maths Of It](https://www.youtube.com/@TheMathsOfIt).

**Find your own spread in your browser:** https://themathsofit.github.io/where-to-aim-in-darts/

Everyone aims at treble 20. The best spot depends on how widely your darts land (your spread, σ).

| σ (mm) | Best spot | Points per dart |
|---:|---|---:|
| 10 | Treble 20 | 29.5 |
| 16 | Treble 20 | 20.7 |
| 17 | Treble 19 | 19.7 |
| 30 | Treble 19, slightly inward | 14.7 |
| 60 | Single 8, near the centre | 12.4 |

A pro averaging 34.4 at treble 20 has σ ≈ 8 mm, so they're right to aim there.

## Run it

```
pip install -r requirements.txt
python where_to_aim.py
python where_to_aim.py 22 35
```

## Sources

- [Tibshirani, Price & Taylor, "A statistician plays darts" (2011)](https://www.stat.cmu.edu/~ryantibs/papers/darts-signif.pdf)
- [PDC: To switch or not to switch?](https://www.pdc.tv/node/8057)
- [Darts Orakel: van Gerwen's treble 20 rate](https://dartsorakel.com/blog/?p=4656)
- [PDC: Madars Razma and treble 19](https://pdc.tv/node/18742)

MIT licence.
