type
  User = object
    id: int
    name: string
    email: Option[string]

proc greet(user: User): string =
  "Hello, " & user.name & "!"

let user = User(id: 1, name: "Alice", email: some("alice@example.com"))
echo greet(user)