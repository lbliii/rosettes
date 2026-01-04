val name: String? = null
val length = name?.length ?: 0
val forced = name!!.length

name?.let { n ->
    println(n.uppercase())
}