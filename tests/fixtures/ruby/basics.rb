class User
  attr_accessor :name, :email
  
  def initialize(name, email)
    @name = name
    @email = email
  end
  
  def greet
    puts "Hello, #{@name}!"
  end
end