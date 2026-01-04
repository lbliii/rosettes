def numbers = [1, 2, 3, 4, 5]
def doubled = numbers.collect { it * 2 }
def filtered = numbers.findAll { it > 2 }

numbers.each { n ->
    println n
}