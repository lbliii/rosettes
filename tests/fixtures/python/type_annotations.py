

def greet(name: str) -> str:
    return f"Hello, {name}"

def process(items: list[int]) -> dict[str, int]:
    return {"count": len(items)}

x: int = 42
y: str | None = None
z: int | str = "hello"

class User:
    name: str
    age: int
