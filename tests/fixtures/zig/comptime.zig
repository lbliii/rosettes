fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

const result = max(u32, 10, 20);