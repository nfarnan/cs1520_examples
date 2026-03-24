mod indirect;
mod nester;
mod shy;

mod direct {
    pub fn hi() {
        println!("Direct says hi!");
    }
}

fn main() {
    direct::hi();

    indirect::hi();

    // Will error unless we use mod to add ignored to the crate
    //ignored::hi();

    nester::hi();

    // Can't access, not a public module
    //nester::nested_a::hi();

    nester::nested_b::hi();

    shy::hi();
}
