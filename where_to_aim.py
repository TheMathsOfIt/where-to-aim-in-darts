"""
Where should you actually aim in darts?
The code behind episode 01 of The Maths Of It.

What it does
  1. Builds a real dartboard as a grid of tiny squares (0.5 mm), each with its score.
  2. Models a throw as a round 2D normal (bell-curve) cloud around the aim point,
     with one number, sigma (mm), for how wide the cloud is.
  3. Slides the cloud over the board (a convolution) to get the average score
     for every aim point at once, then finds the best one.
  4. Works out a pro's sigma from their stage average at treble 20.
  5. Estimates YOUR sigma from 50 darts aimed at the centre (maximum likelihood).

Run:  python where_to_aim.py            (needs numpy and scipy)
      python where_to_aim.py 25         (one spread, in mm)
"""
import sys
import numpy as np
from scipy.signal import fftconvolve

# ---- the board ------------------------------------------------------------
# Standard ring radii in mm, measured from the centre.
BULL, OUTER_BULL = 6.35, 15.9
TREBLE_IN, TREBLE_OUT = 99.0, 107.0
DOUBLE_IN, DOUBLE_OUT = 162.0, 170.0
# Numbers clockwise from the top.
ORDER = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

H = 0.5      # grid step, mm (each square is 0.5 mm across)
R = 230.0    # grid half-width, mm (room for darts that miss the board)

xs = np.arange(-R, R + H / 2, H)
X, Y = np.meshgrid(xs, xs[::-1])            # x to the right, y up, centre at (0, 0)
RAD = np.hypot(X, Y)
ANG = (np.degrees(np.arctan2(X, Y)) + 360) % 360   # degrees clockwise from the top


def segment(angle_deg):
    return np.array(ORDER)[(((angle_deg + 9) % 360) // 18).astype(int)]


def score_grid():
    """Score of a dart landing in every 0.5 mm square."""
    s = np.where(RAD <= DOUBLE_OUT, segment(ANG), 0).astype(float)
    s[(RAD >= TREBLE_IN) & (RAD <= TREBLE_OUT)] *= 3
    s[(RAD >= DOUBLE_IN) & (RAD <= DOUBLE_OUT)] *= 2
    s[RAD <= OUTER_BULL] = 25
    s[RAD <= BULL] = 50
    return s


SCORES = score_grid()


def name(x, y):
    r = np.hypot(x, y)
    n = ORDER[int((((np.degrees(np.arctan2(x, y)) + 360) % 360 + 9) % 360 // 18))]
    if r <= BULL: return 'bull'
    if r <= OUTER_BULL: return 'outer bull'
    if TREBLE_IN <= r <= TREBLE_OUT: return f'treble {n}'
    if DOUBLE_IN <= r <= DOUBLE_OUT: return f'double {n}'
    if r > DOUBLE_OUT: return 'off the board'
    return f'single {n}'


def treble_centre(n):
    a = np.radians(ORDER.index(n) * 18)      # treble 19 is 198 degrees round from the top
    r = (TREBLE_IN + TREBLE_OUT) / 2
    return r * np.sin(a), r * np.cos(a)


# ---- the throw and the convolution ---------------------------------------
def cloud(sigma):
    """Round 2D normal distribution on the same grid, cut at 4 sigma, summing to 1."""
    k = np.arange(-4 * sigma, 4 * sigma + H / 2, H)
    KX, KY = np.meshgrid(k, k)
    g = np.exp(-(KX ** 2 + KY ** 2) / (2 * sigma ** 2))
    return g / g.sum()


def expected_scores(sigma):
    """Average points per dart for every aim point on the grid."""
    return fftconvolve(SCORES, cloud(sigma), mode='same')


def at(E, x, y):
    i = np.unravel_index(np.argmin((X - x) ** 2 + (Y - y) ** 2), X.shape)
    return float(E[i])


def best_aim(sigma):
    E = expected_scores(sigma)
    on_board = RAD <= DOUBLE_OUT             # only aim at points on the board
    i = np.unravel_index(np.where(on_board, E, -1).argmax(), E.shape)
    return dict(sigma=sigma, x=float(X[i]), y=float(Y[i]), best=float(E[i]),
                spot=name(X[i], Y[i]), from_centre_mm=float(RAD[i]),
                T20=at(E, *treble_centre(20)), T19=at(E, *treble_centre(19)),
                bull=at(E, 0, 0), aim_points_tested=int(on_board.sum()))


# ---- real players: sigma from a stage average at treble 20 ---------------
def sigma_from_t20_average(avg, lo=3.0, hi=40.0):
    """Find the sigma whose expected score aiming at the centre of T20 equals avg."""
    for _ in range(40):                       # bisection: the score falls as sigma grows
        mid = (lo + hi) / 2
        if at(expected_scores(mid), *treble_centre(20)) > avg: lo = mid
        else: hi = mid
    return (lo + hi) / 2


# ---- your sigma: 50 darts aimed at the centre ----------------------------
def score_probabilities(sigma):
    """Chance of each score (0 to 60) when aiming at the centre, for this sigma."""
    w = np.exp(-(RAD ** 2) / (2 * sigma ** 2))
    w /= 2 * np.pi * sigma ** 2 / H ** 2      # density times square area
    p = np.bincount(SCORES.astype(int).ravel(), weights=w.ravel(), minlength=61)
    p[0] += max(0.0, 1 - p.sum())             # everything that misses the board scores 0
    return p


def estimate_sigma(scores, grid=np.arange(3, 100.01, 0.5)):
    """Maximum-likelihood sigma from scores of darts aimed at the centre."""
    s = np.asarray(scores, int)
    ll = [np.log(np.maximum(score_probabilities(g)[s], 1e-12)).sum() for g in grid]
    return float(grid[int(np.argmax(ll))])


# ---- run -----------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) > 1:
        sigmas = [float(a) for a in sys.argv[1:]]
    else:
        sigmas = [5, 10, 15, 16, 17, 20, 25, 30, 40, 60, 100]
    print(f"{'sigma':>6}  {'best spot':<16} {'pts/dart':>8} {'T20':>7} {'T19':>7} {'bull':>7}")
    for s in sigmas:
        b = best_aim(s)
        print(f"{s:>6g}  {b['spot']:<16} {b['best']:>8.2f} {b['T20']:>7.2f} {b['T19']:>7.2f} {b['bull']:>7.2f}"
              f"   ({b['from_centre_mm'] / 10:.1f} cm from centre)")
    print(f"\nAim points tested per spread: {best_aim(25)['aim_points_tested']:,}")
    if len(sys.argv) == 1:
        print(f"Pro stage average of 34.36 at T20 -> sigma of about {sigma_from_t20_average(34.36):.1f} mm")
        rng = np.random.default_rng(1)
        test = rng.normal(0, 30, (50, 2))     # 50 pretend darts with a 30 mm spread
        demo = [int(SCORES[np.argmin(np.abs(xs[::-1] - y)), np.argmin(np.abs(xs - x))]) for x, y in test]
        print(f"50 test darts thrown with sigma 30 -> estimated sigma {estimate_sigma(demo):.1f} mm")
