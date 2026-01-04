proc swap[T](a, b: var T) =
  let temp = a
  a = b
  b = temp

type
  Container[T] = object
    value: T