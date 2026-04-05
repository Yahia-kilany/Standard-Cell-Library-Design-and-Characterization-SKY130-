.title NOR2 demo
.include circuit.sp
.temp 25
.param VDD=1.8
Vdd vdd 0 {VDD}

* Inputs
Va A 0 PULSE(0 {VDD} 0ns 1n 1n 20n 40n)
Vb B 0 PULSE(0 {VDD} 40ns 1n 1n 40n 80n)
Xnor2 A B 0 0 vdd vdd Y nor2_x1

.tran 0.5n 80n
.control
run

plot v(A) v(Y)
plot v(B) v(Y)
.endc
.end