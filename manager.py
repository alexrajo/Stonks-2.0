from strategies import test, golden_cross, ema_rsi
from strategies import rsi as rsi_strat
from strategies import vix as vix_strat

from indicators import vix, rsi, sma, ema, vwap

s = {
    "test": test,
    "golden_cross": golden_cross,
    "rsi": rsi_strat,
    "vix": vix_strat,
    "ema + rsi": ema_rsi
}

i = {
    "vix": vix,
    "rsi": rsi,
    "sma": sma,
    "ema": ema,
    "vwap": vwap
}
