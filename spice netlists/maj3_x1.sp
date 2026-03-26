.title MAJ3 delay demo
.lib /home/y_kilany/work/pdks/volare/sky130/versions/dd7771c384ed36b91a25e9f8b314355fc26561be/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.temp 25

.param VDD=1.8
.param WMIN=0.42
.param LMIN=0.15
.param CLOAD=25f
.param kp=2.372781
.param n = 1
Vdd vdd 0 {VDD}

* Inputs
Va A 0 PULSE(0 {VDD} 100ps 20ps 20ps 300ps 700ps)
Vb B 0 PULSE(0 {VDD} 200ps 20ps 20ps 300ps 700ps)
Vc C 0 PULSE(0 {VDD} 300ps 20ps 20ps 300ps 700ps)


* -------- PMOS (Pull-Up: (A'+B')(A'+C')(B'+C')) --------

Xmp1 vout A n4 n4 sky130_fd_pr__pfet_01v8 l={LMIN} w={n*2.5*kp*WMIN}
Xmp2 vout B n4 n4 sky130_fd_pr__pfet_01v8 l={LMIN} w={n*2.5*kp*WMIN}

Xmp3 n4 A n5 n5 sky130_fd_pr__pfet_01v8 l={LMIN} w={n*2.5*kp*WMIN}
Xmp4 n4 C n5 n5 sky130_fd_pr__pfet_01v8 l={LMIN} w={n*2.5*kp*WMIN}

Xmp5 n5 B vdd vdd sky130_fd_pr__pfet_01v8 l={LMIN} w={n*2.5*kp*WMIN}
Xmp6 n5 C vdd vdd sky130_fd_pr__pfet_01v8 l={LMIN} w={n*2.5*kp*WMIN}

* -------- NMOS (pull-down: AB + AC + BC) --------
* AB branch
Xmn1 vout A n1 n1 sky130_fd_pr__nfet_01v8 l={LMIN} w={n*2*WMIN}
Xmn2 n1   B 0  0 sky130_fd_pr__nfet_01v8 l={LMIN} w={n*2*WMIN}

* AC branch
Xmn3 vout A n2 n1 sky130_fd_pr__nfet_01v8 l={LMIN} w={n*2*WMIN}
Xmn4 n2   C 0  0 sky130_fd_pr__nfet_01v8 l={LMIN} w={n*2*WMIN}

* BC branch
Xmn5 vout B n3 n3 sky130_fd_pr__nfet_01v8 l={LMIN} w={n*2*WMIN}
Xmn6 n3   C 0  0 sky130_fd_pr__nfet_01v8 l={LMIN} w={n*2*WMIN}
Cload vout 0 {CLOAD}
.tran 1p 1n
.control
run

* Output low-to-high delay (tpLH)
.meas tran tpLH trig v(A) val={0.5*VDD} rise=1 targ v(vout) val={0.5*VDD} rise=1

* Output high-to-low delay (tpHL)
.meas tran tpHL trig v(A) val={0.5*VDD} fall=1 targ v(vout) val={0.5*VDD} fall=1
print tpLH tpHL
plot v(A) v(vout)  
.endc
.end