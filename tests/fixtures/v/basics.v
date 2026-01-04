struct User {
    id int
    name string
    email ?string
}

fn greet(user User) string {
    return "Hello, ${user.name}!"
}

fn main() {
    user := User{
        id: 1
        name: "Alice"
        email: "alice@example.com"
    }
    println(greet(user))
}