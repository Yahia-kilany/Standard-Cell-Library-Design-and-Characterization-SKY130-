"""
utils.py
---------------
Shared constants, helpers, and sweep logic for SPICE cell characterisation
scripts (INV, NAND2, NOR2, min3, …).
"""
  
import os
import yaml
import numpy as np
import pandas as pd
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_F, u_V, u_ns, u_ps, u_s
 
 
# ── PDK / process constants ──────────────────────────────────────────────────
 
with open("config.yaml") as _f:
    _cfg = yaml.safe_load(_f)
 
PDK_LIB: str = os.path.join(
    _cfg["pdk_root"], "libs.tech/ngspice/sky130.lib.spice"
)
 
VDD:  float = 1.8
LMIN: float = 0.15
KP:   float = 2.372781
W_N:  float = 0.42
W_P:  float = KP * W_N
 
 
# ── Waveform helpers ─────────────────────────────────────────────────────────
 
def first_crossing(
    time_s: np.ndarray,
    wave_v: np.ndarray,
    threshold_v: float,
    edge: str,
    t_min_s: float = 0.0,
) -> float:
    """Return the interpolated time of the first threshold crossing.
 
    Parameters
    ----------
    time_s      : time array [s]
    wave_v      : voltage array [V]
    threshold_v : crossing level [V]
    edge        : ``"rising"`` or ``"falling"``
    t_min_s     : ignore crossings before this time [s]
    """
    start = np.searchsorted(time_s, t_min_s)
    d = wave_v - threshold_v
 
    for i in range(start, len(time_s) - 1):
        y0, y1 = d[i], d[i + 1]
        if edge == "rising"  and not (y0 < 0 <= y1):
            continue
        if edge == "falling" and not (y0 > 0 >= y1):
            continue
        frac = 0.0 if y1 == y0 else -y0 / (y1 - y0)
        return float(time_s[i] + frac * (time_s[i + 1] - time_s[i]))
 
    raise RuntimeError(
        f"No {edge} crossing of {threshold_v:.4f} V found after {t_min_s*1e9:.3f} ns"
    )
 
 
def measure_delays(
    t: np.ndarray,
    vin: np.ndarray,
    vout: np.ndarray,
) -> tuple[float, float, float, float]:
    """Measure cell_fall, cell_rise, rise_transition, fall_transition [ns].
 
    Thresholds follow the Liberty convention:
      - propagation delay  : 50 % of VDD
      - transition time    : 20 %–80 % of VDD
    """
    v50 = 0.5 * VDD
    v20 = 0.2 * VDD
    v80 = 0.8 * VDD
 
    # Find input edges first
    t_in_rise = first_crossing(t, vin, v50, "rising")
    t_in_fall = first_crossing(t, vin, v50, "falling", t_min_s=t_in_rise)

    # cell_fall: vin rising 50% → vout falling 50%
    t_out_fall = first_crossing(t, vout, v50, "falling", t_min_s=t_in_rise)
    cell_fall  = (t_out_fall - t_in_rise) * 1e9

    # cell_rise: vin falling 50% → vout rising 50%
    t_out_rise = first_crossing(t, vout, v50, "rising",  t_min_s=t_in_fall)
    cell_rise  = (t_out_rise - t_in_fall) * 1e9

    # fall_transition: anchored after t_in_rise to skip IC artifact
    t_fall_80  = first_crossing(t, vout, v80, "falling")
    t_fall_20  = first_crossing(t, vout, v20, "falling", t_min_s=t_fall_80)
    fall_trans = (t_fall_20 - t_fall_80) * 1e9

    # rise_transition: anchored after t_in_fall
    t_rise_20  = first_crossing(t, vout, v20, "rising")
    t_rise_80  = first_crossing(t, vout, v80, "rising",  t_min_s=t_rise_20)
    rise_trans = (t_rise_80 - t_rise_20) * 1e9
    return cell_fall, cell_rise, rise_trans, fall_trans
 
 
# ── Simulation ───────────────────────────────────────────────────────────────
 
def simulate(c: Circuit):
    """Run a standard transient simulation (10 ps step, 40 ns window)."""
    sim = c.simulator(temperature=25, nominal_temperature=25)
    return sim.transient(step_time=10 @ u_ps, end_time=80 @ u_ns)
 
 
# ── Sweep ────────────────────────────────────────────────────────────────────
 
def run_sweep(
    cell_name: str,
    n: int,
    build_fn,
    load_caps_f: list[float],
    slew_20_80_s: list[float],
    pins: list[str],
    *,
    vin_node_fn=None,
) -> dict[str, tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """Sweep (transition time × load cap) for every pin and one drive strength.
 
    Parameters
    ----------
    cell_name     : for labeling only
    n            : drive-strength multiplier
    build_fn     : callable ``(n, cload_f, trans_time_s, pin) -> Circuit``
    load_caps_f  : list of load capacitances [F]
    slew_20_80_s : list of 20–80 % slew times [s]
    pins         : list of pin names to characterise (e.g. ``["A", "B"]``)
    vin_node_fn  : optional ``(pin) -> str`` that maps a pin name to the
                   ngspice node name used for ``vin``.  Defaults to
                   ``pin.lower()``.
 
    Returns
    -------
    dict mapping pin name → (df_cell_fall, df_cell_rise,
                              df_rise_trans, df_fall_trans)
    """
    slew_0_100_s = [t / 0.6 for t in slew_20_80_s]
    load_labels  = [f"{c * 1e15:.4f} fF" for c in load_caps_f]
    trans_labels = [f"{t * 1e9:.4f} ns"  for t in slew_20_80_s]
 
    if vin_node_fn is None:
        vin_node_fn = lambda pin: pin.lower()
 
    pin_results: dict = {}
 
    for pin in pins:
        shape = (len(slew_20_80_s), len(load_caps_f))
        cell_fall_mat  = np.full(shape, np.nan)
        cell_rise_mat  = np.full(shape, np.nan)
        rise_trans_mat = np.full(shape, np.nan)
        fall_trans_mat = np.full(shape, np.nan)
 
        for ti, trans_s in enumerate(slew_0_100_s):
            for ci, cload_f in enumerate(load_caps_f):
                try:
                    circ = build_fn(n, cload_f, trans_s, pin)
                    tr   = simulate(circ)
 
                    t    = np.array(tr.time,                   dtype=float)
                    vin  = np.array(tr[vin_node_fn(pin)],      dtype=float)
                    vout = np.array(tr["Y"],                   dtype=float)
 
                    cell_fall, cell_rise, rise_trans, fall_trans = measure_delays(
                        t, vin, vout
                    )
 
                    cell_fall_mat[ti, ci]  = cell_fall
                    cell_rise_mat[ti, ci]  = cell_rise
                    rise_trans_mat[ti, ci] = rise_trans
                    fall_trans_mat[ti, ci] = fall_trans
 
                    print(
                        f"cell {cell_name} n={n}  pin={pin}  "
                        f"tr={trans_s * 0.6 * 1e9:.4f} ns  "
                        f"CL={cload_f * 1e15:.4f} fF  "
                        f"tPHL={cell_fall:.3f} ns  tPLH={cell_rise:.3f} ns  "
                        f"rise_trans={rise_trans:.3f} ns  fall_trans={fall_trans:.3f} ns"
                    )
 
                except Exception as exc:
                    print(
                        f"  [WARN] cell {cell_name} n={n} pin={pin} "
                        f"tr={trans_s * 0.6 * 1e9:.4f} ns "
                        f"CL={cload_f * 1e15:.4f} fF → {exc}"
                    )
 
        def _make_df(mat: np.ndarray) -> pd.DataFrame:
            df = pd.DataFrame(mat, index=trans_labels, columns=load_labels)
            df.index.name = "Transition Time \\ Load Cap"
            return df
 
        pin_results[pin] = (
            _make_df(cell_fall_mat),
            _make_df(cell_rise_mat),
            _make_df(rise_trans_mat),
            _make_df(fall_trans_mat),
        )
 
    return pin_results
 
 
# ── Output helpers ────────────────────────────────────────────────────────────
 
def print_table(df: pd.DataFrame, title: str) -> None:
    """Pretty-print a timing table to stdout."""
    print(f"\n{'═' * 80}")
    print(f"  {title}")
    print(f"{'═' * 80}")
    print(df.to_string())
    print()
 
 
def save_excel(
    all_results: dict,
    filename: str,
    cell_name: str,
) -> None:
    """Write all timing tables to an Excel workbook."""
    with pd.ExcelWriter(filename, engine="openpyxl") as xw:
        for n, pin_results in all_results.items():
            for pin, (df_HL, df_LH, df_rt, df_ft) in pin_results.items():
                sheet_name = f"{cell_name}x{n}_pin{pin}"
                start_row = 0

                for name, df in [
                    ("cell_fall", df_HL),
                    ("cell_rise", df_LH),
                    ("rise_trans", df_rt),
                    ("fall_trans", df_ft),
                ]:
                    pd.DataFrame([[name]]).to_excel(
                        xw,
                        sheet_name=sheet_name,
                        startrow=start_row,
                        startcol=0,
                        header=False,
                        index=False,
                    )

                    # table below title
                    df.to_excel(
                        xw,
                        sheet_name=sheet_name,
                        startrow=start_row + 1,
                        index=True,
                    )

                    start_row += len(df) + 3

    print(f"\nDone. Excel tables saved to {filename}")
 
 
def characterise(
    cell_name: str,
    build_fn,
    drive_strengths: list[int],
    load_caps_f: list[float],
    slew_20_80_s: list[float],
    pins: list[str],
    excel_filename: str,
    *,
    vin_node_fn=None,
) -> None:
    """Top-level entry point: sweep all drive strengths, print tables, save Excel.
 
    This is the function that each cell script calls from ``if __name__ == "__main__"``.
    """
    all_results: dict = {}
 
    for n in drive_strengths:
        print(f"\n{'#' * 60}")
        print(f"  Sweeping {cell_name}x{n}")
        print(f"{'#' * 60}")
 
        pin_results = run_sweep(
            cell_name, n , build_fn, load_caps_f, slew_20_80_s, pins,
            vin_node_fn=vin_node_fn,
        )
        all_results[n] = pin_results
 
        for pin, (df_HL, df_LH, df_rt, df_ft) in pin_results.items():
            print_table(df_HL, f"tPHL (ns)            — {cell_name}x{n}  pin={pin}")
            print_table(df_LH, f"tPLH (ns)            — {cell_name}x{n}  pin={pin}")
            print_table(df_rt,  f"Rise Transition (ns) — {cell_name}x{n}  pin={pin}")
            print_table(df_ft,  f"Fall Transition (ns) — {cell_name}x{n}  pin={pin}")
        save_excel(all_results, excel_filename, cell_name)