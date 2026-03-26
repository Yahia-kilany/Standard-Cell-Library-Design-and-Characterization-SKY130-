.title INVx1 delay demo
.lib /home/y_kilany/work/pdks/volare/sky130/versions/dd7771c384ed36b91a25e9f8b314355fc26561be/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.temp 25

.param VDD=1.8
.param WMIN=0.42
.param LMIN=0.15
.param CLOAD=25f
.param kp=2.372781
.param n = 1
Vdd vdd 0 {VDD}
Vin in 0 PULSE(
    0           ; V1 = low
    {VDD}         ; V2 = high
    0.100p       ; TD = start time
    0.010/0.6p   ; TR = rise time for 0.2→0.8 VDD
    0.010/0.6p   ; TF = fall time for 0.2→0.8 VDD
    50p         ; PW = pulse width (long enough for gate to respond)
    200p        ; PER = total period
)
Xmp vout vin vdd vdd sky130_fd_pr__pfet_01v8 l=0.15 w={n*kp*WMIN}
Xmn vout vin 0 0 sky130_fd_pr__nfet_01v8 l=0.15 w={n*WMIN}
Cload vout 0 {CLOAD}
.tran 1p 1n
.control
run
* Output low-to-high delay (tpLH)
.meas tran tpLH trig v(in) val={0.5*VDD} rise=1 targ v(vout) val={0.5*VDD} rise=1

* Output high-to-low delay (tpHL)
.meas tran tpHL trig v(in) val={0.5*VDD} fall=1 targ v(vout) val={0.5*VDD} fall=1
print tpLH tpHL
plot v(in) v(vout)
.endc
.end    