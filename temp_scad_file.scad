
// Chair Design with Beveled Top Backrest and Higher Legs

module chair() {
    translate([0, 0, 1]) {
        // Seat
        cube([30, 30, 2]);

        // Backrest with Top Bevel
        translate([0, 28, 2]) {
            // Main backrest
            cube([30, 2, 35]);

            // Bevel 30% from top
            translate([0, 0, 24])
                scale([1, 1, 0.3])
                cube([30, 2, 11]);
        }

        // Higher Legs
        translate([1, 1, -25])
            cube([4, 4, 27]);
        translate([25, 1, -25])
            cube([4, 4, 27]);
        translate([1, 25, -25])
            cube([4, 4, 27]);
        translate([25, 25, -25])
            cube([4, 4, 27]);
    }
}

chair();
