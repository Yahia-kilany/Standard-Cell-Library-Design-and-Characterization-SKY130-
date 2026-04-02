import yaml
import os
from PySpice.Spice.Netlist import Circuit, SubCircuit, SubCircuitFactory
from PySpice.Unit import *

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

PDK_LIB = os.path.join(cfg["pdk_root"], "libs.tech/ngspice/sky130.lib.spice")

circuits = [("INV", 8), ("NAND2", 4), ("NOR2", 4), ("MAJ3", 4)]

VDD  = 1.8
LMIN = 0.15
KP   = 2.372781     
W_N  = 0.42          
W_P  = KP * W_N

PDK_LIB = (
    "/home/y_kilany/work/pdks/volare/sky130/versions/"
    "dd7771c384ed36b91a25e9f8b314355fc26561be/"
    "sky130A/libs.tech/ngspice/sky130.lib.spice"
)

class INV_N(SubCircuitFactory):
    __nodes__ = ('vin', 'vout','vdd','vss')
    def __init__(self, N=1 ):
        SubCircuit.__init__(self, f"inv_x{N}", *self.__nodes__)
        self.__name__ = f'inv_x{N}'
        # PMOS  — Xmp vout vin vdd vdd sky130_fd_pr__pfet_01v8 l=LMIN w=WPMOS
        self.X(
            "mp", "sky130_fd_pr__pfet_01v8",
            "vout", "vin", "vdd", "vdd",
            w=N*W_P, l=LMIN,
        )
        # NMOS  — Xmn vout vin 0 0 sky130_fd_pr__nfet_01v8 l=LMIN w=WNMOS
        self.X(
            "mn", "sky130_fd_pr__nfet_01v8",
            "vout", "vin", "vss", "vss",
            w=N*W_N, l=LMIN,
        )

class NAND2_N(SubCircuitFactory):
    __nodes__ = ('vin1', 'vin2', 'vout','vdd','vss',)
    def __init__(self, N=1 ):
        SubCircuit.__init__(self, f"nand2_x{N}", *self.__nodes__)
        self.__name__ = f"nand2_x{N}"
        self.X(
            "mp1", "sky130_fd_pr__pfet_01v8",
            "vout", "vin1", "vdd", "vdd",
            w=N*W_P, l=LMIN,
        )
        self.X(
            "mp2", "sky130_fd_pr__pfet_01v8",
            "vout", "vin2", "vdd", "vdd",
            w=N*W_P, l=LMIN,
        )
        self.X(
            "mn1", "sky130_fd_pr__nfet_01v8",
            "vout", "vin1", "n1", "n1",
            w=2*N*W_N, l=LMIN,
        )
        self.X(
            "mn2", "sky130_fd_pr__nfet_01v8",
            "n1", "vin2", "vss", "vss",
            w=2*N*W_N, l=LMIN,
        )

class NOR2_N(SubCircuitFactory):
    __nodes__ = ('vin1', 'vin2', 'vout','vdd','vss')
    def __init__(self, N = 1 ):
        SubCircuit.__init__(self, f"nor2_x{N}", *self.__nodes__)
        self.__name__ = f"nor2_x{N}"
        self.X(
            "mp1", "sky130_fd_pr__pfet_01v8",
            "n1", "vin1", "vdd", "vdd",
            w=2*N*W_P, l=LMIN,
        )
        self.X(
            "mp2", "sky130_fd_pr__pfet_01v8",
            "vout", "vin2", "n1", "n1",
            w=2*N*W_P, l=LMIN,
        )
        self.X(
            "mn1", "sky130_fd_pr__nfet_01v8",
            "vout", "vin1", "gnd", "gnd",
            w=N*W_N, l=LMIN,
        )
        self.X(
            "mn2", "sky130_fd_pr__nfet_01v8",
            "vout", "vin2", "gnd", "gnd",
            w=N*W_N, l=LMIN,
        )

class MAJ3_N(SubCircuitFactory):
    __nodes__ = ('vdd', 'vout','gnd', 'vin1', 'vin2', 'vin3')
    def __init__(self, N=1 ):
        SubCircuit.__init__(self, f"maj3_x{N}", *self.__nodes__)
        self.__name__ = f"maj3_x{N}"
        self.X(
            "mp1", "sky130_fd_pr__pfet_01v8",
            "vout", "vin1", "n4", "n4",
            w=2.5*N*W_P, l=LMIN,
        )
        self.X(
            "mp2", "sky130_fd_pr__pfet_01v8",
            "vout", "vin2", "n4", "n4",
            w=2.5*N*W_P, l=LMIN,
        )
        self.X(
            "mp3", "sky130_fd_pr__pfet_01v8",
            "n4", "vin1", "n5", "n5",
            w=2.5*N*W_P, l=LMIN,
        )
        self.X(
            "mp4", "sky130_fd_pr__pfet_01v8",
            "n4", "vin3", "n5", "n5",
            w=2.5*N*W_P, l=LMIN,
        )
        self.X(
            "mp5", "sky130_fd_pr__pfet_01v8",
            "n5", "vin2", "vdd", "vdd",
            w=2.5*N*W_P, l=LMIN,
        )
        self.X(
            "mp6", "sky130_fd_pr__pfet_01v8",
            "n5", "vin3", "vdd", "vdd",
            w=2.5*N*W_P, l=LMIN,
        )
        self.X(
            "mn1", "sky130_fd_pr__nfet_01v8",
            "vout", "vin1", "n1", "n1",
            w=2*N*W_N, l=LMIN,
        )
        self.X(
            "mn2", "sky130_fd_pr__nfet_01v8",
            "n1", "vin2", "gnd", "gnd",
            w=2*N*W_N, l=LMIN,
        )
        self.X(
            "mn3", "sky130_fd_pr__nfet_01v8",
            "vout", "vin1", "n2", "n2",
            w=2*N*W_N, l=LMIN,
        )
        self.X(
            "mn4", "sky130_fd_pr__nfet_01v8",
            "n2", "vin3", "gnd", "gnd",
            w=2*N*W_N, l=LMIN,
        )
        self.X(
            "mn5", "sky130_fd_pr__nfet_01v8",
            "vout", "vin2", "n3", "n3",
            w=2*N*W_N, l=LMIN,
        )
        self.X(
            "mn6", "sky130_fd_pr__nfet_01v8",
            "n3", "vin3", "gnd", "gnd",
            w=2*N*W_N, l=LMIN,
        )


circuit = Circuit("subckt test")
circuit.lib(PDK_LIB, "tt")
for name, N in circuits:
        i = 1
        while i <= N:
            if(name == "INV"):
                circuit.subcircuit(INV_N(N=i))
            if(name == "NAND2"):
                circuit.subcircuit(NAND2_N(N=i))
            if(name == "NOR2"):
                circuit.subcircuit(NOR2_N(N=i))
            if(name == "MAJ3"):
                circuit.subcircuit(MAJ3_N(N=i))
            i *=2
            
print(circuit)
with open("circuit.sp", "w") as f:
    print(circuit, file=f)