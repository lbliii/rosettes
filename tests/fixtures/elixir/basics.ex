defmodule User do
  @moduledoc "User module"
  
  defstruct [:id, :name, :email]
  
  def new(name, email) do
    %__MODULE__{id: UUID.uuid4(), name: name, email: email}
  end
  
  def greet(%__MODULE__{name: name}) do
    "Hello, #{name}!"
  end
end