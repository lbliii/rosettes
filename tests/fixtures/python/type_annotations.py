from typing import List, Dict, Optional, Union

def greet(name: str) -> str:
    return f"Hello, {name}"

def process(items: List[int]) -> Dict[str, int]:
    return {"count": len(items)}

x: int = 42
y: Optional[str] = None
z: Union[int, str] = "hello"

class User:
    name: str
    age: int
