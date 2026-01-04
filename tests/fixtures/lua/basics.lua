local function greet(name)
    name = name or "World"
    print("Hello, " .. name .. "!")
end

local items = {1, 2, 3, 4, 5}
local config = {
    host = "localhost",
    port = 8080,
    enabled = true
}

for i, v in ipairs(items) do
    print(i, v)
end

for k, v in pairs(config) do
    print(k .. " = " .. tostring(v))
end