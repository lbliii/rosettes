abstract type Shape end

struct Circle <: Shape
    radius::Float64
end

struct Rectangle <: Shape
    width::Float64
    height::Float64
end

area(s::Circle) = π * s.radius^2
area(s::Rectangle) = s.width * s.height