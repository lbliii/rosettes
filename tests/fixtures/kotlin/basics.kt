data class User(
    val id: Int,
    val name: String,
    val email: String?
)

fun main() {
    val user = User(1, "Alice", "alice@example.com")
    println("Hello, ${user.name}!")
}