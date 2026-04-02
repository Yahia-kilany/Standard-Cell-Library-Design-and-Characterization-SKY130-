.title INVx1 delay demo

.lib /home/y_kilany/work/pdks/volare/sky130/versions/dd7771c384ed36b91a25e9f8b314355fc26561be/sky130A/libs.tech/ngspice/sky130.lib.spice tt
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
Vin vin 0 PULSE(0 {VDD} 1n 1n 1n 20n 40n)

Xmp vout vin vdd vdd sky130_fd_pr__pfet_01v8 l={LMIN} w={n*kp*WMIN}
Xmn vout vin 0   0   sky130_fd_pr__nfet_01v8 l={LMIN} w={n*WMIN}

Cload vout 0 {CLOAD}

.ic v(vin)=0 v(vout)={VDD}

.tran 10p 80n

.control
run

meas tran tpHL trig v(vin) val={0.9} rise=1 targ v(vout) val={0.9} fall=1 

meas tran tpLH trig v(vin) val={0.9} fall=1 targ v(vout) val={0.9} rise=1

let tp = (tpHL + tpLH) / 2
print tpHL tpLH tp
plot v(vin) v(vout)

.endc
.end