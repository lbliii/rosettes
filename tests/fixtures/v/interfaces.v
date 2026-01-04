interface Drawable {
    draw()
}

struct Circle {
    radius f64
}

fn (c Circle) draw() {
    println("Drawing circle")
}