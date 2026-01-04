fn main() {
    let x = 42;
    let mut y = 0;
    
    if x > 0 {
        println!("positive");
    } else {
        println!("non-positive");
    }
    
    for i in 0..10 {
        continue;
    }
    
    loop {
        break;
    }
    
    match x {
        0 => println!("zero"),
        _ => println!("other"),
    }
}

struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }
}

trait Drawable {
    fn draw(&self);
}

async fn async_fn() {
    do_something().await;
}
