func swap<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

protocol Container {
    associatedtype Item
    var count: Int { get }
    mutating func append(_ item: Item)
}