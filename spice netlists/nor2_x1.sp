.title NOR2 delay demo
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

* PMOS (series)
Xmp1 n1   A vdd vdd sky130_fd_pr__pfet_01v8 l={LMIN} w={n*2*kp*WMIN}
Xmp2 vout B n1 n1 sky130_fd_pr__pfet_01v8 l={LMIN} w={n*2*kp*WMIN}

* NMOS (parallel)
Xmn1 vout A 0 0 sky130_fd_pr__nfet_01v8 l={LMIN} w={n*WMIN}
Xmn2 vout B 0 0 sky130_fd_pr__nfet_01v8 l={LMIN} w={n*WMIN}

Cload vout 0 {CLOAD}


* Output low-to-high delay (tpLH)
.meas tran tpLH trig v(A) val={0.5*VDD} rise=1 targ v(vout) val={0.5*VDD} rise=1

* Output high-to-low delay (tpHL)
.meas tran tpHL trig v(A) val={0.5*VDD} fall=1 targ v(vout) val={0.5*VDD} fall=1