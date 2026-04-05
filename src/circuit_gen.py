from ast import main

import yaml
import os
from PySpice.Spice.Netlist import Circuit, SubCircuit, SubCircuitFactory
from PySpice.Unit import *

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

PDK_LIB = os.path.join(cfg["pdk_root"], "libs.tech/ngspice/sky130.lib.spice")

circuits = [("INV", 8), ("NAND2", 4), ("NOR2", 4), ("MIN3", 4)]

VDD  = 1.8
LMIN = 0.15
KP   = 2.372781     
W_N  = 0.42          
W_P  = KP * W_N


#A, VGND, VNB, VPB, VPWR, Y
class INV_N(SubCircuitFactory):

    __nodes__ = ('A', 'VGND', 'VNB', 'VPB', 'VPWR', 'Y') 
    def __init__(self, N=1 ):
        SubCircuit.__init__(self, f"inv_x{N}", *self.__nodes__)
        self.__name__ = f'inv_x{N}'
        self.X(
            "mp", "sky130_fd_pr__pfet_01v8",
            "Y", "A", "VPWR", "VPB",
            w=N*W_P, l=LMIN,
        )
        self.X(
            "mn", "sky130_fd_pr__nfet_01v8",
            "Y", "A", "VGND", "VNB",
            w=N*W_N, l=LMIN,
        )

class NAND2_N(SubCircuitFactory):
    __nodes__ = ('A', 'B', 'VGND', 'VNB', 'VPB', 'VPWR', 'Y')
    def __init__(self, N=1 ):
        SubCircuit.__init__(self, f"nand2_x{N}", *self.__nodes__)
        self.__name__ = f"nand2_x{N}"
        self.X(
            "mp1", "sky130_fd_pr__pfet_01v8",
            "Y", "A", "VPWR", "VPB",
            w=N*W_P, l=LMIN,
        )
        self.X(
            "mp2", "sky130_fd_pr__pfet_01v8",
            "Y", "B", "VPWR", "VPB",
            w=N*W_P, l=LMIN,
        )
        self.X(
            "mn1", "sky130_fd_pr__nfet_01v8",
            "Y", "A", "n1", "VNB",
            w=2*N*W_N, l=LMIN,
        )
        self.X(
            "mn2", "sky130_fd_pr__nfet_01v8",
            "n1", "B", "VGND", "VNB",
            w=2*N*W_N, l=LMIN,
        )

class NOR2_N(SubCircuitFactory):
    __nodes__ = ('A', 'B', 'VGND', 'VNB', 'VPB', 'VPWR', 'Y')
    def __init__(self, N = 1 ):
        SubCircuit.__init__(self, f"nor2_x{N}", *self.__nodes__)
        self.__name__ = f"nor2_x{N}"
        self.X(
            "mp1", "sky130_fd_pr__pfet_01v8",
            "n1", "A", "VPWR", "VPB",
            w=2*N*W_P, l=LMIN,
        )
        self.X(
            "mp2", "sky130_fd_pr__pfet_01v8",
            "Y", "B", "n1", "VPB",
            w=2*N*W_P, l=LMIN,
        )
        self.X(
            "mn1", "sky130_fd_pr__nfet_01v8",
            "Y", "A", "VGND", "VNB",
            w=N*W_N, l=LMIN,
        )
        self.X(
            "mn2", "sky130_fd_pr__nfet_01v8",
            "Y", "B", "VGND", "VNB",
            w=N*W_N, l=LMIN,
        )


class MIN3_N(SubCircuitFactory):
    __nodes__ = ('A', 'B', 'C', 'VGND', 'VNB', 'VPB', 'VPWR', 'Y')
    def __init__(self, N=1):
        SubCircuit.__init__(self, f"min3_x{N}", *self.__nodes__)
        self.__name__ = f"min3_x{N}"

        # -------- PMOS (Pull-Up: (A'+B')(A'+C')(B'+C')) --------
        self.X(
            "mp1", "sky130_fd_pr__pfet_01v8",
            "Y", "A", "n4", "VPB",
            w=2.5 * N * W_P, l=LMIN,
        )
        self.X(
            "mp2", "sky130_fd_pr__pfet_01v8",
            "Y", "B", "n4", "VPB",
            w=2.5 * N * W_P, l=LMIN,
        )
        self.X(
            "mp3", "sky130_fd_pr__pfet_01v8",
            "n4", "A", "n5", "VPB",
            w=2.5 * N * W_P, l=LMIN,
        )
        self.X(
            "mp4", "sky130_fd_pr__pfet_01v8",
            "n4", "C", "n5", "VPB",   # matches: Xmp4 n4 C n5 ...
            w=2.5 * N * W_P, l=LMIN,
        )
        self.X(
            "mp5", "sky130_fd_pr__pfet_01v8",
            "n5", "B", "VPWR", "VPB", # matches: Xmp5 n5 B vdd vdd ...
            w=2.5 * N * W_P, l=LMIN,
        )
        self.X(
            "mp6", "sky130_fd_pr__pfet_01v8",
            "n5", "C", "VPWR", "VPB",
            w=2.5 * N * W_P, l=LMIN,
        )
        # -------- NMOS (pull-down: AB + AC + BC) --------
        # AB branch
        self.X(
            "mn1", "sky130_fd_pr__nfet_01v8",
            "Y", "A", "n1", "VNB",
            w=2 * N * W_N, l=LMIN,
        )
        self.X(
            "mn2", "sky130_fd_pr__nfet_01v8",
            "n1", "B", "VGND", "VNB",
            w=2 * N * W_N, l=LMIN,
        )
        # AC branch
        self.X(
            "mn3", "sky130_fd_pr__nfet_01v8",
            "Y", "A", "n2", "VNB",
            w=2 * N * W_N, l=LMIN,
        )
        self.X(
            "mn4", "sky130_fd_pr__nfet_01v8",
            "n2", "C", "VGND", "VNB",
            w=2 * N * W_N, l=LMIN,
        )
        # BC branch
        self.X(
            "mn5", "sky130_fd_pr__nfet_01v8",
            "Y", "B", "n3", "VNB",
            w=2 * N * W_N, l=LMIN,
        )
        self.X(
            "mn6", "sky130_fd_pr__nfet_01v8",
            "n3", "C", "VGND", "VNB",
            w=2 * N * W_N, l=LMIN,
        )


def main():
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
                if(name == "MIN3"):
                    circuit.subcircuit(MIN3_N(N=i))
                i *=2
                
    print(circuit)
    with open("circuit.sp", "w") as f:
        print(circuit, file=f)

if __name__ == "__main__":
    SystemExit(main())