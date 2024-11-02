
module ring(outer_diameter=20, thickness=2, width=5) {
    difference() {
        // Outer cylinder
        cylinder(h=width, r=outer_diameter/2, $fn=100);

        // Inner cylinder
        translate([0, 0, -1])
        cylinder(h=width + 2, r=(outer_diameter - thickness*2)/2, $fn=100);
    }
}

// Create a ring with a 20 mm outer diameter
ring(outer_diameter=20);
