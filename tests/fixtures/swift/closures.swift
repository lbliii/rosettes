let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }
let sorted = numbers.sorted { $0 > $1 }

func process(completion: @escaping (Result<Int, Error>) -> Void) {
    DispatchQueue.main.async {
        completion(.success(42))
    }
}