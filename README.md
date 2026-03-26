# SKY130 Standard Cell Library Design & NLDM Characterization

##  Overview
This project implements the design and characterization of a standard cell library using the SKY130 process. The primary objective is to generate Non-Linear Delay Model (NLDM) timing tables through SPICE simulations.

The project includes:
- Design of 13 standard cells with multiple drive strengths
- Extraction of delay and slew tables
- Analytical comparison with a first-order RC delay model

---

## Team
- Student 1: Seif-Eldien Elwan
- Student 2: Yahia Kilany

---

## Objectives
- Design CMOS standard cells (INV, NAND2, NOR2, MAJ3)
- Size transistors for balanced rise/fall behavior
- Automate SPICE simulations across multiple conditions
- Generate NLDM tables:
  - `cell_rise`
  - `cell_fall`
  - `rise_transition`
  - `fall_transition`
- Compare SPICE results with RC delay model

---

## Target Library

| Cell Type | Function | Drive Strengths |
|----------|--------|----------------|
| Inverter | Y = A' | invx1, invx2, invx4, invx8 |
| NAND2 | Y = (A·B)' | nand2x1, nand2x2, nand2x4 |
| NOR2 | Y = (A+B)' | nor2x1, nor2x2, nor2x4 |
| MAJ3 | Y = AB + BC + AC | maj3x1, maj3x2, maj3x4 |

Total Cells: **13**

---

## ⚙️ Characterization Setup

- Process Corner: TT
- Temperature: 25°C
- Supply Voltage: 1.8V

### Input Transition (ns)
0.0100, 0.0231, 0.0531, 0.1225, 0.2823, 0.6507, 1.5000

### Output Load Capacitance (pF)
0.0005, 0.0013, 0.0035, 0.0094, 0.0249, 0.0662, 0.1758

---
## 📏 Measurement Definitions

- **Propagation Delay**: 0.5VDD (input) → 0.5VDD (output)
- **Rise Time (Slew)**: 0.2VDD → 0.8VDD
- **Fall Time (Slew)**: 0.8VDD → 0.2VDD

---
