pub fn process(value: Result(String, String)) {
  case value {
    Ok(result) -> result
    Error(reason) -> "Error: " <> reason
  }
}