template<typename T>
class Container {
public:
    explicit Container(T value) : value_(std::move(value)) {}
    
    T& get() noexcept { return value_; }
    const T& get() const noexcept { return value_; }
    
private:
    T value_;
};