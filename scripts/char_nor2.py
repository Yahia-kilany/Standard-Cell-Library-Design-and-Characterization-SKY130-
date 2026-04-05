"""
char_nor2.py
------------
Characterise sky130 NOR2 cells (NOR2x1, NOR2x2, NOR2x4).
All shared logic lives in utils.py.
"""

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_F, u_V, u_ns, u_ps, u_s
from src.utils import PDK_LIB, VDD, characterise 
from src.circuit_gen import NOR2_N

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

def build_nor2(n: int, cload_f: float, trans_time_s: float, pin: str = "A") -> Circuit:
    """Build a NOR2x{n} testbench; the inactive pin is tied to GND."""
    assert pin in ("A", "B"), "pin must be 'A' or 'B'"

    other = "B" if pin == "A" else "A"

    c = Circuit(f"NOR2x{n} delay demo (pin={pin})")
    c.lib(PDK_LIB, "tt")

    c.V("dd", "vdd", c.gnd, VDD @ u_V)
    c.PulseVoltageSource(
        "in", pin, c.gnd,
        initial_value = 0   @ u_V,
        pulsed_value  = VDD @ u_V,
        delay_time    = 10 @ u_ns,
        rise_time     = trans_time_s @ u_s,
        fall_time     = trans_time_s @ u_s,
        pulse_width   = 20  @ u_ns,
        period        = 40  @ u_ns,
    )
    # NOR2: inactive input held LOW so the gate can switch
    c.V(f"tie_{other}", other, c.gnd, c.gnd @ u_V)

    c.subcircuit(NOR2_N(N=n))
    # Port order: A, B, VGND, VNB, VPB, VPWR, Y
    c.X("nor2", f"nor2_x{n}", "A", "B", c.gnd, c.gnd, "vdd", "vdd", "Y")
    c.C("load", "Y", c.gnd, cload_f @ u_F)

    return c


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    characterise(
        cell_name       = "NOR2",
        build_fn        = build_nor2,
        drive_strengths = DRIVE_STRENGTHS,
        load_caps_f     = LOAD_CAPS_F,
        slew_20_80_s    = SLEW_20_80_S,
        pins            = PINS,
        excel_filename  = "nor2_delay_tables.xlsx",
    )