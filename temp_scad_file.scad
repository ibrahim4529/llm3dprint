$fn=50;

module chair_leg() {
    difference() {
        cylinder(h = 90, r1 = 20, r2 = 0, center = true);
        translate([0, 0, -5])
        cylinder(h = 100, r1 = 16, r2 = 16, center = true);
    }
}

module chair_back() {
    difference() {
        cube([40, 3, 60]);
        translate([0, 0, 60])
        cube([40, 30, 3]);
    }
}

module chair_seat() {
    cube([40, 40, 3]);
}

module chair() {
    union() {
        translate([-8, -8, 0]) chair_leg();
        translate([32, -8, 0]) chair_leg();
        translate([-8, 32, 0]) chair_leg();
        translate([32, 32, 0]) chair_leg();
        
        translate([12, 0, 99]) chair_back();
        translate([0, 0, 72]) chair_seat();
    }
}

chair();