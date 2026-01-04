class User {
    String name
    String email
    
    User(String name, String email) {
        this.name = name
        this.email = email
    }
    
    String greet() {
        "Hello, ${name}!"
    }
}

def user = new User("Alice", "alice@example.com")
println user.greet()