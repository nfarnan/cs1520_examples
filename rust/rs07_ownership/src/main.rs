// Previous example code
struct Point(i32, i32);

struct Rectangle {
    top_left: Point,
    width: i32,
    height: i32,
}

impl Rectangle {
    fn new(top_left: Point, width: i32, height: i32) -> Rectangle {
        Rectangle {
            top_left,
            width,
            height,
        }
    }

    // Note that methods are borrowing the values they're attached to!
    fn identify(&self) {
        println!("I am a Rectangle");
    }
}

trait Shape {
    fn area(&self) -> i32;
    fn contains(&self, p: Point) -> bool;
}

impl Shape for Rectangle {
    fn area(&self) -> i32 {
        self.width * self.height
    }

    fn contains(&self, p: Point) -> bool {
        if p.0 > self.top_left.0
            && p.0 < (self.top_left.0 + self.width)
            && p.1 > self.top_left.1
            && p.1 < (self.top_left.1 + self.height)
        {
            return true;
        }

        false
    }
}

// Ownership example code
fn print_area_own<T: Shape>(some_shape: T) {
    println!("Shape's area: {}", some_shape.area());
}

// The & denotes that we want to borrow a value for some_shape
fn print_area_borrow<T: Shape>(some_shape: &T) {
    println!("Shape's area: {}", some_shape.area());
    // Borrowed reference goes out of scope here, so the value is no longer
    // being borrowed
}

// Creates a dangling reference
// Even including the definition as stated is an error
//fn will_error() -> &Rectangle {
//	let r = Rectangle::new(Point(2, 2), 2, 2);
//	&r
//	// r goes out of scope here, so any returned reference will point to
//	// cleaned up memory!
//}

// Lifetime annotation example
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let r = Rectangle::new(Point(5, 5), 10, 20);

    // This would error
    //print_area_own(r);
    //r.identify();

    // This is OK thanks to the borrow!
    // The & here is creating a reference to r that is passed to the function
    print_area_borrow(&r);
    r.identify();

    // Can't have a reference to cleaned up memory, this will error:
    //let bad = will_error();

    let s = Rectangle::new(Point(0, 0), 10, 10);
    // Can have multiple immutable references to a value
    // Underscores to supress unused variable warnings...
    let _bs1 = &s;
    let _bs2 = &s;
    let _bs3 = &s;

    // If we want to change a borrow item, not only does it need to be
    // mutable, but we need a mutable reference
    let mut t = Rectangle::new(Point(0, 0), 15, 15);
    let _mbt1 = &mut t;

    // We can also have immutable references to a mutable item
    let mut u = Rectangle::new(Point(0, 0), 7, 7);
    let bu = &u;

    // But, we can't create mutable reference if immutables references already
    // exist...
    let mbu = &mut u;
    // ^This^ line won't generate an error unless the mutable borrow is
    // actually used AND the immutable borrow is used after

    mbu.identify();
    // With vthisv line commented out, Rust will drop `bu` so that there is
    // not both a mutable and immutable borrow, given the `bu` isn't needed
    //bu.identify();

    // Can explicitly do something similar with set scopes via blocks
    let mut v = Rectangle::new(Point(0, 0), 8, 8);
    {
        let mbv1 = &mut v;
        mbv1.identify();
        // first mutable reference forced out of scope here
    }
    // so no problem creating another here
    let mbv2 = &mut v;
    mbv2.identify();

    // `l`'s type is `&str`, a string slice
    // Note string literals are stored directly in the program binary
    let l = "this is a string literal";
    let m = &l[10..13];
    println!("l: {}", l);
    println!("m: {}", m);

    // Can use the standard library string to own string data
    let n = String::from("this is owned string data");
    // Can still be sliced to borrow
    let o = &n[8..13];
    println!("n: {}", n);
    println!("o: {}", o);
    // In general, slicing a string is a bad idea

    // String references are string slices (`&str`)
    let p = String::from("short");
    println!("The longest string is: {}", longest(&n, &p));

    let z;
    {
        let q = String::from("also short");
        z = longest(&n, &q);
    }
    // Adding this line will be a compilation error because `q` does not
    // live as long as `z` would. Without this line, `z` can be dropped when
    // `q` is
    //println!("The other longest string is: {}", z);

    // Why does this move:
    let a = Rectangle::new(Point(0, 0), 1, 1);
    let b = a;
    // Will error due to move
    //a.identify();
    b.identify();

    // But this does not?
    let c = 42;
    let d = c;
    println!("c: {}", c);
    println!("d: {}", d);
}
