options = {
  name: "test",
  :legacy => "value",
  enabled: true
}

def method(arg, *args, **kwargs, &block)
  yield if block_given?
end