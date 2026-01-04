auto process(std::vector<int>&& items) -> std::optional<int> {
    if (auto it = std::ranges::find(items, 42); it != items.end()) {
        return *it;
    }
    return std::nullopt;
}

constexpr auto lambda = [](auto x) constexpr { return x * 2; };