.title subckts
.lib /home/y_kilany/work/pdks/volare/sky130/versions/dd7771c384ed36b91a25e9f8b314355fc26561be/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.subckt inv_x1 A VGND VNB VPB VPWR Y
Xmp Y A VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=0.9965680199999999
Xmn Y A VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.42
.ends inv_x1

.subckt inv_x2 A VGND VNB VPB VPWR Y
Xmp Y A VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=1.9931360399999998
Xmn Y A VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
.ends inv_x2

.subckt inv_x4 A VGND VNB VPB VPWR Y
Xmp Y A VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=3.9862720799999996
Xmn Y A VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
.ends inv_x4

.subckt inv_x8 A VGND VNB VPB VPWR Y
Xmp Y A VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=7.972544159999999
Xmn Y A VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=3.36
.ends inv_x8

.subckt nand2_x1 A B VGND VNB VPB VPWR Y
Xmp1 Y A VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=0.9965680199999999
Xmp2 Y B VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=0.9965680199999999
Xmn1 Y A n1 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
Xmn2 n1 B VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
.ends nand2_x1

.subckt nand2_x2 A B VGND VNB VPB VPWR Y
Xmp1 Y A VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=1.9931360399999998
Xmp2 Y B VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=1.9931360399999998
Xmn1 Y A n1 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
Xmn2 n1 B VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
.ends nand2_x2

.subckt nand2_x4 A B VGND VNB VPB VPWR Y
Xmp1 Y A VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=3.9862720799999996
Xmp2 Y B VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=3.9862720799999996
Xmn1 Y A n1 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=3.36
Xmn2 n1 B VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=3.36
.ends nand2_x4

.subckt nor2_x1 A B VGND VNB VPB VPWR Y
Xmp1 n1 B VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=1.9931360399999998
Xmp2 Y A n1 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=1.9931360399999998
Xmn1 Y A VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.42
Xmn2 Y B VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.42
.ends nor2_x1

.subckt nor2_x2 A B VGND VNB VPB VPWR Y
Xmp1 n1 B VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=3.9862720799999996
Xmp2 Y A n1 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=3.9862720799999996
Xmn1 Y A VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
Xmn2 Y B VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
.ends nor2_x2

.subckt nor2_x4 A B VGND VNB VPB VPWR Y
Xmp1 n1 B VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=7.972544159999999
Xmp2 Y A n1 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=7.972544159999999
Xmn1 Y A VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
Xmn2 Y B VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
.ends nor2_x4

.subckt min3_x1 A B C VGND VNB VPB VPWR Y
Xmp1 Y A n4 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=2.49142005
Xmp2 Y B n4 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=2.49142005
Xmp3 n4 A n5 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=2.49142005
Xmp4 n4 C n5 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=2.49142005
Xmp5 n5 B VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=2.49142005
Xmp6 n5 C VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=2.49142005
Xmn1 Y A n1 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
Xmn2 n1 B VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
Xmn3 Y A n2 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
Xmn4 n2 C VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
Xmn5 Y B n3 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
Xmn6 n3 C VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=0.84
.ends min3_x1

.subckt min3_x2 A B C VGND VNB VPB VPWR Y
Xmp1 Y A n4 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=4.9828401
Xmp2 Y B n4 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=4.9828401
Xmp3 n4 A n5 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=4.9828401
Xmp4 n4 C n5 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=4.9828401
Xmp5 n5 B VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=4.9828401
Xmp6 n5 C VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=4.9828401
Xmn1 Y A n1 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
Xmn2 n1 B VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
Xmn3 Y A n2 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
Xmn4 n2 C VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
Xmn5 Y B n3 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
Xmn6 n3 C VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=1.68
.ends min3_x2

.subckt min3_x4 A B C VGND VNB VPB VPWR Y
Xmp1 Y A n4 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=9.9656802
Xmp2 Y B n4 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=9.9656802
Xmp3 n4 A n5 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=9.9656802
Xmp4 n4 C n5 VPB sky130_fd_pr__pfet_01v8 l=0.15 w=9.9656802
Xmp5 n5 B VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=9.9656802
Xmp6 n5 C VPWR VPB sky130_fd_pr__pfet_01v8 l=0.15 w=9.9656802
Xmn1 Y A n1 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=3.36
Xmn2 n1 B VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=3.36
Xmn3 Y A n2 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=3.36
Xmn4 n2 C VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=3.36
Xmn5 Y B n3 VNB sky130_fd_pr__nfet_01v8 l=0.15 w=3.36
Xmn6 n3 C VGND VNB sky130_fd_pr__nfet_01v8 l=0.15 w=3.36
.ends min3_x4


