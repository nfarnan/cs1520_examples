fn main() {
    // This will error
    //let x = 5;
    //x = 6;

    let mut x = 5;
    x = 6;

    println!("This is integer x: {}", x);

    // This will error
    //x = 6.1;

    // We can shadow x, however
    let x = 6.1;

    println!("This is float x: {}", x);

    // Compiler can still infer a type without same-line initialization
    let b;
    // Won't compile without this line, with or with type annotation
    b = true;

    println!("boolean test: {}", b);

    let y: u8 = 254;

    // This will panic at runtime during development, overflow in a release
    let z: u8 = y + 3;

    println!("y: {}, z: {}", y, z);
}
