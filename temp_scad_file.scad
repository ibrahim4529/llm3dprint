difference() {
    cube([20, 20, 20]);
    translate([10, 10, -10]) {
        cylinder(h = 30, r = 5);
    }
    translate([10, 10, 20]) {
        sphere(r = 10);
    }
}