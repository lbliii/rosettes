const std = @import("std");

const User = struct {
    id: u32,
    name: []const u8,
    email: ?[]const u8,
};

pub fn main() !void {
    const user = User{
        .id = 1,
        .name = "Alice",
        .email = "alice@example.com",
    };
    std.debug.print("Hello, {s}!\n", .{user.name});
}