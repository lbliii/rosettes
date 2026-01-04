import gleam/io

pub type User {
  User(id: Int, name: String, email: Option(String))
}

pub fn greet(user: User) {
  case user {
    User(_, name, _) -> "Hello, " <> name <> "!"
  }
}

pub fn main() {
  let user = User(1, "Alice", Some("alice@example.com"))
  io.println(greet(user))
}