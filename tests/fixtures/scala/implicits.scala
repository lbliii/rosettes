implicit class RichString(s: String) {
  def isPalindrome: Boolean = s == s.reverse
}

implicit val defaultTimeout: Duration = 5.seconds

def fetch(url: String)(implicit timeout: Duration): String = ???