import Foundation

struct User: Codable {
    let id: Int
    var name: String
    var email: String?
}

class UserService {
    func fetchUser(id: Int) async throws -> User {
        let url = URL(string: "https://api.example.com/users/\(id)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(User.self, from: data)
    }
}