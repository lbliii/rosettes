struct User
    id::Int
    name::String
    email::Union{String, Nothing}
end

function greet(user::User)
    println("Hello, $(user.name)!")
end

user = User(1, "Alice", "alice@example.com")
greet(user)