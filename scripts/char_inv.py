"""
char_inv.py
-----------
Characterise sky130 inverter cells (INVx1, INVx2, INVx4, INVx8).
All shared logic lives in utils.py.
"""
 
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_F, u_V, u_s, u_ps, u_ns
from src.utils import PDK_LIB, VDD, characterise 
from src.circuit_gen import INV_N
 
# ── Sweep parameters ──────────────────────────────────────────────────────────
 
LOAD_CAPS_F = [
    0.0005e-12, 0.0013e-12, 0.0035e-12, 0.0094e-12,
    0.0249e-12, 0.0662e-12, 0.1758e-12,
]  # Farads
 
SLEW_20_80_S = [
    0.0100e-9, 0.0231e-9, 0.0531e-9, 0.1225e-9,
    0.2823e-9, 0.6507e-9, 1.5000e-9,
]  # seconds
 
DRIVE_STRENGTHS = [1, 2, 4, 8]
 
# INV has one input; we expose it as "A" so the common sweep loop stays uniform
PINS = ["A"]
 
 
# ── Circuit builder ───────────────────────────────────────────────────────────
 
def build_inv(n: int, cload_f: float, trans_time_s: float, pin: str = "A") -> Circuit:
    """Build an INVx{n} testbench.  ``pin`` is accepted but always "A"."""
    c = Circuit(f"INVx{n} delay demo")
    c.lib(PDK_LIB, "tt")
 
    c.V("dd", "vdd", c.gnd, VDD @ u_V)
    c.PulseVoltageSource(
        "in", "A", c.gnd,
        initial_value = 0   @ u_V,
        pulsed_value  = VDD @ u_V,
        delay_time    = 10 @ u_ns,
        rise_time     = trans_time_s @ u_s,
        fall_time     = trans_time_s @ u_s,
        pulse_width   = 20  @ u_ns,
        period        = 40  @ u_ns,
    )
 
    c.subcircuit(INV_N(n))
    # Port order: A, VGND, VNB, VPB, VPWR, Y
    c.X("inv", f"inv_x{n}", "A", c.gnd, c.gnd, "vdd", "vdd", "Y")
    c.C("load", "Y", c.gnd, cload_f @ u_F)
 
    return c
 
 
# ── Entry point ───────────────────────────────────────────────────────────────
 
if __name__ == "__main__":
    characterise(
        cell_name       = "INV",
        build_fn        = build_inv,
        drive_strengths = DRIVE_STRENGTHS,
        load_caps_f     = LOAD_CAPS_F,
        slew_20_80_s    = SLEW_20_80_S,
        pins            = PINS,
        excel_filename  = "inv_delay_tables.xlsx",
    )