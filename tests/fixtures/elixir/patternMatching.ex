def process(value) do
  case value do
    {:ok, result} -> result
    {:error, reason} -> raise reason
    [head | _tail] -> head
    %{key: value} -> value
    _ -> nil
  end
end

def handle_message({:ping, sender}), do: send(sender, :pong)
def handle_message({:data, payload}), do: process(payload)
def handle_message(_), do: :ignore