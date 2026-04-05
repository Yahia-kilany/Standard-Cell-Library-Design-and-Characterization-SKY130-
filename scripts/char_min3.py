"""
char_min3.py
------------
Characterise sky130 MIN3 cells (MIN3x1).
All shared logic lives in utils.py.
"""

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_F, u_V, u_ns, u_ps, u_s
from src.utils import PDK_LIB, VDD, characterise 
from src.circuit_gen import MIN3_N
# ── Sweep parameters ──────────────────────────────────────────────────────────

LOAD_CAPS_F = [
    0.0005e-12, 0.0013e-12, 0.0035e-12, 0.0094e-12,
    0.0249e-12, 0.0662e-12, 0.1758e-12,
]  # Farads
SLEW_20_80_S = [
    0.0100e-9, 0.0231e-9, 0.0531e-9, 0.1225e-9,
    0.2823e-9, 0.6507e-9, 1.5000e-9,
]  # seconds

DRIVE_STRENGTHS = [1, 2, 4]
PINS = ["A", "B", "C"]

# Inactive pin assignment:
#   one non-driven pin → GND, the other → VDD  (creates minority-logic condition)
_TIE_LOW  = {"A": "B", "B": "A", "C": "A"}   # pin tied LOW per active pin
_TIE_HIGH = {"A": "C", "B": "C", "C": "B"}   # pin tied HIGH per active pin


# ── Circuit builder ───────────────────────────────────────────────────────────

def build_min3(n: int, cload_f: float, trans_time_s: float, pin: str = "A") -> Circuit:
    """Build a MIN3x{n} testbench.

    The two inactive inputs are tied one-low / one-high so the minority gate
    switches on every input transition of the active pin.
    """
    assert pin in ("A", "B", "C"), "pin must be 'A', 'B', or 'C'"

    c = Circuit(f"MIN3x{n} delay demo (pin={pin})")
    c.lib(PDK_LIB, "tt")

    c.V("dd", "vdd", c.gnd, VDD @ u_V)
    c.PulseVoltageSource(
        "in", pin, c.gnd,
        initial_value = 0   @ u_V,
        pulsed_value  = VDD @ u_V,
        delay_time    = 100 @ u_ps,
        rise_time     = trans_time_s @ u_s,
        fall_time     = trans_time_s @ u_s,
        pulse_width   = 20  @ u_ns,
        period        = 40  @ u_ns,
    )

    tie_low  = _TIE_LOW[pin]
    tie_high = _TIE_HIGH[pin]
    c.V(f"tie_{tie_low}",  tie_low,  c.gnd, c.gnd @ u_V)
    c.V(f"tie_{tie_high}", tie_high, c.gnd, VDD   @ u_V)

    c.subcircuit(MIN3_N(N=n))
    # Port order: A, B, C, VGND, VNB, VPB, VPWR, Y
    c.X("min3", f"min3_x{n}", "A", "B", "C", c.gnd, c.gnd, "vdd", "vdd", "Y")
    c.C("load", "Y", c.gnd, cload_f @ u_F)

    return c


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    characterise(
        cell_name       = "MIN3",
        build_fn        = build_min3,
        drive_strengths = DRIVE_STRENGTHS,
        load_caps_f     = LOAD_CAPS_F,
        slew_20_80_s    = SLEW_20_80_S,
        pins            = PINS,
        excel_filename  = "min3_delay_tables.xlsx",
    )