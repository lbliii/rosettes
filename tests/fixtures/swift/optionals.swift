var name: String? = nil
let unwrapped = name ?? "default"
if let n = name {
    print(n)
}
guard let n = name else { return }