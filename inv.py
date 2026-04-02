import yaml
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl.workbook import Workbook
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_F, u_V, u_ns, u_ps, u_s

# PDK 
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

PDK_LIB = os.path.join(cfg["pdk_root"], "libs.tech/ngspice/sky130.lib.spice")

VDD  = 1.8
LMIN = 0.15
KP   = 2.372781     
W_N  = 0.42          
W_P  = KP * W_N

# Sweep values
LOAD_CAPS_F = [
    0.0005e-12, 0.0013e-12, 0.0035e-12, 0.0094e-12,
    0.0249e-12, 0.0662e-12, 0.1758e-12,
]  # Farads

SLEW_20_80_S = [
    0.0100e-9, 0.0231e-9, 0.0531e-9, 0.1225e-9,
    0.2823e-9, 0.6507e-9, 1.5000e-9,
]  # seconds

SLEW_0_100_S = [ t/0.6 for t in SLEW_20_80_S ]  #scaled from 20-80% to 0-100% rise time

DRIVE_STRENGTHS = [1, 2, 4, 8]


# Helpers 
def first_crossing(
    time_s: np.ndarray,
    wave_v: np.ndarray,
    threshold_v: float,
    edge: str,
    t_min_s: float = 0.0,
) -> float:
    """Interpolated time of the first threshold crossing at/after t_min_s."""
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


# Build circuit 
def build_inv(n: int, cload_f: float, trans_time_s: float) -> Circuit:
    """
    Parameters
    ----------
    n            : drive strength multiplier (integer)
    cload_f      : load capacitance in **Farads**
    trans_time_s : input rise/fall time in **seconds**
    """
    c = Circuit(f"INVx{n} delay demo")
    c.lib(PDK_LIB, "tt")

    c.V("dd", "vdd", c.gnd, VDD @ u_V)

    c.PulseVoltageSource(
        "in", "vin", c.gnd,
        initial_value = 0   @ u_V,
        pulsed_value  = VDD @ u_V,
        delay_time    = 100 @ u_ps,       
        rise_time     = trans_time_s @ u_s, 
        fall_time     = trans_time_s @ u_s,  
        pulse_width   = 20  @ u_ns,
        period        = 40  @ u_ns,
    )

    # PMOS — source/bulk to vdd
    c.X(
        "mp", "sky130_fd_pr__pfet_01v8",
        "vout", "vin", "vdd", "vdd",
        w=n * W_P, l=LMIN,
    )

    # NMOS — source/bulk to gnd
    c.X(
        "mn", "sky130_fd_pr__nfet_01v8",
        "vout", "vin", c.gnd, c.gnd,
        w=n * W_N, l=LMIN,
    )

    c.C("load", "vout", c.gnd, cload_f @ u_F)

    return c


# Simulate 
def simulate(c: Circuit):
    sim = c.simulator(temperature=25, nominal_temperature=25)
    sim.initial_condition(vin=0, vout=VDD)

    return sim.transient(step_time=10 @ u_ps, end_time=80 @ u_ns)


# Measure propagation delays 
def measure_delays(t, vin, vout):
    v50 = 0.5 * VDD
    v20 = 0.2 * VDD
    v80 = 0.8 * VDD
    # tpHL: vin rising 50% -> vout falling 50%
    t_in_rise  = first_crossing(t, vin,  v50, "rising")
    t_out_fall = first_crossing(t, vout, v50, "falling", t_min_s=t_in_rise)
    cell_fall = (t_out_fall - t_in_rise) * 1e9   # → ns

    # tpLH: vin falling 50% -> vout rising 50%
    t_in_fall  = first_crossing(t, vin,  v50, "falling")
    t_out_rise = first_crossing(t, vout, v50, "rising",  t_min_s=t_in_fall)
    cell_rise = (t_out_rise - t_in_fall) * 1e9   # → ns

    # rise_transition: 20% -> 80% on vout
    t_rise_20 = first_crossing(t, vout, v20, "rising")
    t_rise_80 = first_crossing(t, vout, v80, "rising", t_min_s=t_rise_20)
    rise_trans = (t_rise_80 - t_rise_20) * 1e9

    # fall_transition: 80% -> 20% on vout
    t_fall_80 = first_crossing(t, vout, v80, "falling")
    t_fall_20 = first_crossing(t, vout, v20, "falling", t_min_s=t_fall_80)
    fall_trans = (t_fall_20 - t_fall_80) * 1e9
    return  cell_fall, cell_rise, rise_trans, fall_trans


# Run sweep & collect results 
def run_sweep(n: int):
    """
    Returns two DataFrames (tpHL, tpLH) indexed by transition-time (rows)
    and load capacitance (columns).
    """
    # Label strings for axes
    load_labels  = [f"{c*1e15:.4f} fF" for c in LOAD_CAPS_F]
    trans_labels = [f"{t*1e9:.4f} ns"  for t in SLEW_20_80_S]

    cell_fall_mat = np.full((len(SLEW_20_80_S), len(LOAD_CAPS_F)), np.nan)
    cell_rise_mat = np.full((len(SLEW_20_80_S), len(LOAD_CAPS_F)), np.nan)
    rise_trans_mat = np.full((len(SLEW_20_80_S), len(LOAD_CAPS_F)), np.nan)
    fall_trans_mat = np.full((len(SLEW_20_80_S), len(LOAD_CAPS_F)), np.nan)
    for ti, trans_s in enumerate(SLEW_0_100_S):
        for ci, cload_f in enumerate(LOAD_CAPS_F):
            try:
                circ = build_inv(n, cload_f, trans_s)
                tr   = simulate(circ)

                t    = np.array(tr.time,    dtype=float)
                vin  = np.array(tr["vin"],  dtype=float)
                vout = np.array(tr["vout"], dtype=float)

                cell_fall, cell_rise, rise_trans, fall_trans = measure_delays(t, vin, vout)

                cell_fall_mat[ti, ci] = cell_fall
                cell_rise_mat[ti, ci] = cell_rise
                rise_trans_mat[ti, ci] = rise_trans
                fall_trans_mat[ti, ci] = fall_trans

                print(
                    f"  n={n}  tr={trans_s*0.6*1e9:.4f}ns  "
                    f"CL={cload_f*1e15:.4f}fF  "
                    f"tPHL={cell_fall:.3f}ns  tPLH={cell_rise:.3f}ns"
                )

            except Exception as exc:
                print(f"  [WARN] n={n} tr={trans_s*0.6*1e9:.4f}ns "
                      f"CL={cload_f*1e15:.4f}fF → {exc}")

    df_cell_fall = pd.DataFrame(cell_fall_mat, index=trans_labels, columns=load_labels)
    df_cell_rise = pd.DataFrame(cell_rise_mat, index=trans_labels, columns=load_labels)
    df_rise_trans = pd.DataFrame(rise_trans_mat, index=trans_labels, columns=load_labels)
    df_fall_trans = pd.DataFrame(fall_trans_mat, index=trans_labels, columns=load_labels)

    df_cell_fall.index.name   = "Transition Time \\ Load Cap"
    df_cell_rise.index.name   = "Transition Time \\ Load Cap"
    df_rise_trans.index.name = "Transition Time \\ Load Cap"
    df_fall_trans.index.name = "Transition Time \\ Load Cap"

    return df_cell_fall, df_cell_rise, df_rise_trans, df_fall_trans


# Pretty-print table 
def print_table(df: pd.DataFrame, title: str):
    print(f"\n{'═'*80}")
    print(f"  {title}")
    print(f"{'═'*80}")
    print(df.to_string())
    print()



def main():
    all_results = {}

    for n in DRIVE_STRENGTHS:
        print(f"\n{'#'*60}")
        print(f"  Sweeping INVx{n}")
        print(f"{'#'*60}")

        df_HL, df_LH, df_rise_trans, df_fall_trans = run_sweep(n)
        all_results[n] = (df_HL, df_LH, df_rise_trans, df_fall_trans)

        print_table(df_HL, f"tPHL (ns)  —  INVx{n}")
        print_table(df_LH, f"tPLH (ns)  —  INVx{n}")
        print_table(df_rise_trans, f"Rise Transition (ns)  —  INVx{n}")
        print_table(df_fall_trans, f"Fall Transition (ns)  —  INVx{n}")

    with pd.ExcelWriter("inv_delay_tables.xlsx") as xw:
        for n, (df_HL, df_LH, df_rise_trans, df_fall_trans) in all_results.items():
            df_HL.to_excel(xw, sheet_name=f"INVx{n}_cell_fall")
            df_LH.to_excel(xw, sheet_name=f"INVx{n}_cell_rise")
            df_rise_trans.to_excel(xw, sheet_name=f"INVx{n}_rise_transition")
            df_fall_trans.to_excel(xw, sheet_name=f"INVx{n}_fall_transition")
    #TODO : Plotting

    print("\nDone. Excel tables saved to inv_delay_tables.xlsx")


if __name__ == "__main__":
    raise SystemExit(main())