local co = coroutine.create(function()
    for i = 1, 10 do
        coroutine.yield(i)
    end
end)

while coroutine.status(co) ~= "dead" do
    local ok, value = coroutine.resume(co)
    if ok then print(value) end
end