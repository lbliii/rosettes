result =
  data
  |> Enum.filter(&(&1 > 0))
  |> Enum.map(&(&1 * 2))
  |> Enum.reduce(0, &+/2)