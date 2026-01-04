suspend fun fetchData(): Result<String> = coroutineScope {
    val deferred = async {
        delay(100)
        "data"
    }
    Result.success(deferred.await())
}

fun main() = runBlocking {
    launch {
        fetchData().onSuccess { println(it) }
    }
}