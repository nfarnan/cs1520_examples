fn main() {
    let strings = vec![
        String::from("first string"),
        String::from("a"),
        String::from("b"),
        String::from("fourth string"),
        String::from("c"),
    ];

    let big_strings: Vec<_> = strings.iter().filter(|x| x.len() > 5).collect();

    println!("Big strings:");
    for s in big_strings.iter() {
        println!("\t{}", s);
    }
    println!("big_strings[0]: {}\n", big_strings[0]);

    let mut little_strings: Vec<_> = strings.into_iter().filter(|x| x.len() < 5).collect();

    println!("Little strings:");
    for s in little_strings.iter_mut() {
        s.push('!');
        println!("\t{}", s);
    }
    println!("little_strings[0]: {}\n", little_strings[0]);

    println!("Little strings again:");
    // By default, for uses `.into_iter()`
    for s in little_strings {
        println!("\t{}", s);
    }
    // This will error
    //println!("little_strings[0]: {}", little_strings[0]);

    println!();
    let ints = vec![5, 10, 15, 20, 25, 30];
    for i in ints {
        println!("int: {}", i);
    }
    // Still moved, even though i types implement Copy, Vec<i32> does not
    //println!("first int again: {}", ints[0]);

    let mut captured = 10;

    // Has to implement Fn trait due to immutable borrow
    let c1 = |x| x + captured;
    println!("c1(5): {}", c1(5));
    println!("c1(15): {}", c1(15));

    captured = 20;
    // Disallowed by borrow check, can't mutate while mutably borrowed
    //println!("c1(15): {}", c1(15));

    // Has to implement FnMut trait due to mutable borrow
    let mut c2 = |x| captured += x;
    c2(10);
    // Can't print in-between calls, because it is mutably borrowed
    // println!() would borrow as well
    // Can't even assign `captured` to another variable, also
    // disallowed by the borrow checker
    c2(5);
    println!("After c2(10); cs(5): {}", captured);

    // Instead of having the compiler infer how capture the var in the closure,
    // can specify `move` to force a move instead of borrow
    let cap2 = vec![1, 2, 3];
    let c3 = move |v| v == cap2;
    println!("c3([1, 2, 3]): {}", c3(vec![1, 2, 3]));
    println!("c3([4, 2, 3]): {}", c3(vec![4, 2, 3]));
    // Won't compile, cap2 moved into closure
    //println!("After c3: {}", cap2);

    // This is ok because ints implement Copy
    let c4 = move |x| x + captured;
    println!("c4(5): {}", c4(5));
    println!("c4(15): {}", c4(15));
    println!("After all: {}", captured);
}
