# SKY130 Standard Cell Library Design & NLDM Characterization

## Overview

This project implements the design and characterization of a standard cell library using the SKY130 process. The primary objective is to generate Non-Linear Delay Model (NLDM) timing tables through automated SPICE simulations using PySpice and ngspice.

The project includes:

- Design of 13 standard cells with multiple drive strengths
- Extraction of delay and slew tables via transient SPICE simulation
- Analytical comparison with a first-order Elmore delay model

---

## Team

- Seif-Eldien Elwan
- Yahia Kilany

---

## Repository Structure

```
.
├── results/              # Generated Excel NLDM table outputs
├── scripts/              # Characterization scripts (char_inv.py, char_nand2.py, etc.)
├── spice netlists/       # contains circuits.sp, and several spice netlists to verify the functions
├── src/                  # Shared source modules (circuit_gen.py, utils.py)
├── environment.yml       # Conda environment specification
└── README.md
```

---

## Target Library

| Cell Type | Function            | Drive Strengths            |
| --------- | ------------------- | -------------------------- |
| Inverter  | Y = A'              | invx1, invx2, invx4, invx8 |
| NAND2     | Y = (A·B)'          | nand2x1, nand2x2, nand2x4  |
| NOR2      | Y = (A+B)'          | nor2x1, nor2x2, nor2x4     |
| MIN3      | Y = (AB + BC + AC)' | min3x1, min3x2, min3x4     |

**Total Cells: 13**

---

## Characterization Setup

- **Process Corner:** TT
- **Temperature:** 25 °C
- **Supply Voltage:** 1.8 V

### NLDM Index Vectors

**Input Transition (ns):**
0.0100, 0.0231, 0.0531, 0.1225, 0.2823, 0.6507, 1.5000

**Output Load Capacitance (pF):**
0.0005, 0.0013, 0.0035, 0.0094, 0.0249, 0.0662, 0.1758

### Measurement Definitions

| Metric            | Definition                                        |
| ----------------- | ------------------------------------------------- |
| `cell_rise`       | 0.5 VDD (input rising) → 0.5 VDD (output rising)  |
| `cell_fall`       | 0.5 VDD (input rising) → 0.5 VDD (output falling) |
| `rise_transition` | 0.2 VDD → 0.8 VDD on output rising edge           |
| `fall_transition` | 0.8 VDD → 0.2 VDD on output falling edge          |

---

## Environment Setup

### 1. Clone the repository

```bash
git clone https://github.com/Yahia-kilany/Standard-Cell-Library-Design-and-Characterization-SKY130-
cd Standard-Cell-Library-Design-and-Characterization-SKY130-
```

### 2. Create the Conda environment

```bash
conda env create -f environment.yml
conda activate sky130-char
```

### 3. Install the SKY130 PDK via Volare

Volare is the recommended PDK version manager for open-source PDKs. This project uses a specific verified version of the SKY130 PDK.

**Install volare:**

```bash
pip install volare
```

**Choose a PDK root and create it:**

```bash
export PDK_ROOT="$HOME/work/pdks"
mkdir -p "$PDK_ROOT"
```

**Install the required SKY130 version:**

```bash
volare enable --pdk sky130 --pdk-root "$PDK_ROOT" dd7771c384ed36b91a25e9f8b314355fc26561be
```

**Resolve and export the active SKY130 path:**

```bash
export SKY130_ROOT="$(volare path --pdk sky130 --pdk-root "$PDK_ROOT" \
  $(volare output --pdk sky130 --pdk-root "$PDK_ROOT"))/sky130A"
```

**Verify the installation:**

```bash
test -f "$SKY130_ROOT/libs.tech/ngspice/sky130.lib.spice" && echo "SKY130 model library found"
```

### 4. Configure the project

Create a `config.yaml` file at the project root pointing to your PDK root:

```yaml
pdk_root: /home/<your-username>/work/pdks
```

---

## Running the Characterization

To run all cell characterizations in parallel:

```bash
bash scripts/char_all.sh
```

To run a single cell:

```bash
python -m scripts.char_inv
python -m scripts.char_nand2
python -m scripts.char_nor2
python -m scripts.char_min3
```

## Results are saved as Excel workbooks.
