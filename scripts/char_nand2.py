"""
char_nand2.py
-------------
Characterise sky130 NAND2 cells (NAND2x1, NAND2x2, NAND2x4).
All shared logic lives in utils.py.
"""

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_F, u_V, u_ns, u_ps, u_s
from src.utils import PDK_LIB, VDD, characterise 
from src.circuit_gen import NAND2_N

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
PINS = ["A", "B"]


# ── Circuit builder ───────────────────────────────────────────────────────────

def build_nand2(n: int, cload_f: float, trans_time_s: float, pin: str = "A") -> Circuit:
    """Build a NAND2x{n} testbench; the inactive pin is tied to VDD."""
    assert pin in ("A", "B"), "pin must be 'A' or 'B'"

    other = "B" if pin == "A" else "A"

    c = Circuit(f"NAND2x{n} delay demo (pin={pin})")
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
    c.V(f"tie_{other}", other, c.gnd, VDD @ u_V)

    c.subcircuit(NAND2_N(n))
    # Port order: A, B, VGND, VNB, VPB, VPWR, Y
    c.X("nand2", f"nand2_x{n}", "A", "B", c.gnd, c.gnd, "vdd", "vdd", "Y")

    c.C("load", "Y", c.gnd, cload_f @ u_F)

    return c


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    characterise(
        cell_name       = "NAND2",
        build_fn        = build_nand2,
        drive_strengths = DRIVE_STRENGTHS,
        load_caps_f     = LOAD_CAPS_F,
        slew_20_80_s    = SLEW_20_80_S,
        pins            = PINS,
        excel_filename  = "nand2_delay_tables.xlsx",
    )