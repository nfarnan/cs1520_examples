fn main() {
    let tup1: (i32, f64, u8) = (500, 6.4, 1);
    // Type annotation not needed, but tup2 will have a different types!
    let tup2 = (500, 6.4, 1);

    // Destructuing a tuple:
    let (x, y, z) = tup1;
    println!("x: {}, y: {}, z: {}", x, y, z);

    // Individual access:
    println!("tup2: ({}, {}, {})", tup2.0, tup2.1, tup2.2);

    // Handy way to check a type:
    // Attempt assignment to a known wrong type and check the compiler error
    //let i: char = z;
    //let j: char = tup2.2;

    // Arrays
    let arr1: [i32; 5] = [1, 2, 3, 4, 5];

    // Skip type annotation, succinct sytax to initialize arrays containing
    // a single value at every index
    let arr2 = [3; 5];

    println!("arr1[3]: {}", arr1[3]);
    println!("arr2[0]: {}, arr2[4]: {}", arr2[0], arr2[4]);

    // Out-of-bounds access will panic at runtime
    // By default, compiler will try to warn of this when it can
    //println!("arr2[5]: {}", arr2[5]);
}
