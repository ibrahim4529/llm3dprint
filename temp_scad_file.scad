// Chair

module chair() {
    difference() {
        // Seat
        cube([20,20,2]);
        
        // Backrest
        translate([0,18,18])
        cube([20,2,18]);
        
        // Backrest crossbars
        translate([0,18,8])
        cube([20,20,2]);
        translate([0,18,8])
        cube([20,2,18]);
        translate([0,18,28])
        cube([20,2,18]);
        
        // Legs
        for (i = [0:1:1]){
            for (j = [0:1:1]){
                translate([i*18,j*18,-18])
                cube([2,2,20]);
            }
        }
    }
}

chair();