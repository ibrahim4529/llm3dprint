
difference() {
    cube([20, 20, 20]);
    translate([10, 10, 0]) {
        cylinder(h=20, r=5, center=false);
    }
}
