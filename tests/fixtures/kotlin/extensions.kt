fun String.isPalindrome(): Boolean {
    return this == this.reversed()
}

val String.wordCount: Int
    get() = this.split("\\s+".toRegex()).size