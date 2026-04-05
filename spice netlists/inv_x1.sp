.title INVx1 demo

.lib /home/y_kilany/work/pdks/volare/sky130/versions/dd7771c384ed36b91a25e9f8b314355fc26561be/sky130A/libs.tech/ngspice/sky130.lib.spice tt

.param VDD=1.8
.param WN=0.42
.param LCH=0.15
.param RDRV=10k

VDD vdd 0 {VDD}

* Step source through resistor
VSTEP src 0 PWL(0 0 100p 0 101p {VDD} 2n {VDD})
RIN src in {RDRV}

XM_N 0 in 0 0 sky130_fd_pr__nfet_01v8 w={WN} l={LCH}

.tran 1p 0.5n

.control
run
meas tran t_src when v(src)=0.9 rise=1
meas tran t_in  when v(in)=0.9 rise=1
let trc = t_in - t_src
let cn = trc/(0.69*10000)
print trc cn
.endc
.end
