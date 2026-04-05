.title INVx1 demo

.include circuit.sp
.temp 25

* ---- Parameters ----
.param VDD=1.8
.param WMIN=0.42
.param LMIN=0.15
.param CLOAD=0.0005p
.param kp=2.372781
.param n=1

* ---- Sources ----
Vdd vdd 0 {VDD}
Vin vin 0 PULSE(0 {VDD} 10n 1n 1n 20n 40n)

Xinv vin 0 0 vdd vdd vout inv_x4
.tran 0.5n 80n

.control
run
plot v(vin) v(vout)

.endc
.end