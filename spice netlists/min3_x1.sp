.title MIN3 demo
.include circuit.sp
.temp 25
.param VDD=1.8
Vdd vdd 0 {VDD}

* Inputs
Va A 0 PULSE(0 {VDD} 0ns 1n 1n 20n 40n)
Vb B 0 PULSE(0 {VDD} 40ns 1n 1n 40n 80n)
Vc C 0 PULSE(0 {VDD} 80ns 1n 1n 80n 160n)
Xnand2 A B C 0 0 vdd vdd Y min3_x1

.tran 1n 160n
.control
run

plot v(A) v(Y)
plot v(B) v(Y)
plot v(C) v(Y)
.endc
.end