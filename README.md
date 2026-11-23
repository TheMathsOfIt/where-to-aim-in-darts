# Where should you actually aim in darts?

The code behind episode 01 of **The Maths Of It** on YouTube.

Everyone aims at treble 20. This works out where you *should* aim, for the way you throw.

## The idea

- **Best spot** = the aim point with the most points per dart, on average (the expected value).
- **Your throw** = a round cloud around where you aim (a 2D normal distribution). One number, **σ (sigma)**, in millimetres, says how wide it is.
- **The board** is split into 0.5 mm squares, each with its real score (standard ring sizes and number order).
- Sliding the cloud over the board and averaging the scores underneath is a **convolution**. It gives the average score for all 363,145 aim points in one go.

## Results

| σ (mm) | Best spot | Points per dart | Aim at T20 | Aim at T19 | Aim at bull |
|---:|---|---:|---:|---:|---:|
| 5 | treble 20 | 43.05 | 43.04 | 40.79 | 38.72 |
| 10 | treble 20 | 29.54 | 29.52 | 28.39 | 25.44 |
| 15 | treble 20 | 21.77 | 21.64 | 21.42 | 18.85 |
| 16 | treble 20 | 20.69 | 20.53 | 20.45 | 18.02 |
| 17 | treble 19 | 19.74 | 19.56 | 19.60 | 17.30 |
| 25 | edge of treble 19 | 15.80 | 14.94 | 15.60 | 13.94 |
| 30 | treble 19, slightly inward | 14.70 | 13.65 | 14.48 | 12.99 |
| 60 | single 8, 4.2 cm from centre | 12.43 | 10.25 | 10.89 | 12.13 |
| 100 | outer bull | 9.65 | 7.52 | 7.79 | 9.62 |

The best spot jumps from treble 20 to treble 19 between σ = 16 and 17 mm. Wider than about 30 mm it slides in towards the centre, down and to the left.

A stage average of 34.36 points a dart at treble 20 works out to σ ≈ 8 mm, so professionals are right to aim at treble 20.

## Run it

```
pip install -r requirements.txt
python where_to_aim.py          # the table above, the pro sigma, and a test of the estimator
python where_to_aim.py 22 35    # any spreads you like, in mm
```

## Find your own spread

Open `index.html` (or the live tool linked in the video description). Aim 50 darts at the centre of the board, type in every score, and it estimates your σ by maximum likelihood and draws your own heatmap.

## Sources

- R. J. Tibshirani, A. Price and J. Taylor, "A statistician plays darts", *Journal of the Royal Statistical Society A* (2011). Short version in *Significance*: https://www.stat.cmu.edu/~ryantibs/papers/darts-signif.pdf
- PDC, "To Switch Or Not To Switch?" (stage averages at treble 20 and treble 19): https://www.pdc.tv/node/8057
- Darts Orakel, Michael van Gerwen's 2022 treble 20 rate: https://dartsorakel.com/blog/?p=4656
- PDC, Madars Razma and treble 19: https://pdc.tv/node/18742

## Limits

The cloud is round (same spread in every direction). Real players often scatter more up and down than side to side, so this is a first model, matching the one in the published research.

MIT licence.
