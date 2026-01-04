struct User:
    var id: Int
    var name: String
    var email: String
    
    fn __init__(inout self, id: Int, name: String, email: String):
        self.id = id
        self.name = name
        self.email = email

fn main():
    let user = User(1, "Alice", "alice@example.com")
    print("Hello,", user.name)