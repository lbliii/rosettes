class User {
  final int id;
  final String name;
  final String? email;
  
  User(this.id, this.name, this.email);
  
  String greet() {
    return "Hello, $name!";
  }
}

void main() {
  final user = User(1, "Alice", "alice@example.com");
  print(user.greet());
}