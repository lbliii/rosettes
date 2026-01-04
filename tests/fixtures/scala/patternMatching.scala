def process(value: Any): String = value match {
  case i: Int if i > 0 => s"Positive: $i"
  case s: String => s.toUpperCase
  case Some(x) => s"Got: $x"
  case None => "Nothing"
  case (a, b) => s"Tuple: $a, $b"
  case head :: tail => s"List head: $head"
  case _ => "Unknown"
}