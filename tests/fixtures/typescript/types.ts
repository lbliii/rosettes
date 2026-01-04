interface User {
    name: string;
    age: number;
}

type Status = "active" | "inactive";

function greet(user: User): string {
    return `Hello ${user.name}`;
}

const numbers: number[] = [1, 2, 3];
const map: Map<string, number> = new Map();

class Service<T> {
    data: T;
}
