pub fn hi() {
    println!("Shy module doesn't want to say hi, asked nested module to do so instead...");
    print!("\t");
    crate::nester::nested_b::hi();
}
