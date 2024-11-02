difference() {
    union() {
        cube([40,40,2]); // seat
        translate([0,0,-2])
            cube([32,32,2]); // seat outline
        translate([0,0,-35])
            cube([2,2,35]); // front left leg
        translate([38,0,-35])
            cube([2,2,35]); // front right leg
        translate([38,38,-35])
            cube([2,2,35]); // back right leg
        translate([0,38,-35])
            cube([2,2,35]); // back left leg
    }
    translate([5,5,0])
        cylinder(h=35, r=1.5, center=true); // front left leg
    translate([35,5,0])
        cylinder(h=35, r=1.5, center=true); // front right leg
    translate([35,35,0])
        cylinder(h=35, r=1.5, center=true); // back right leg
    translate([5,35,0])
        cylinder(h=35, r=1.5, center=true); // back left leg
    translate([20,35,5])
        rotate([90,0,0])
            cube([20,2,25]); // back rest
}