package main

import (
    "fmt"
    "net/http"
)

type User struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func (u *User) Greet() string {
    return fmt.Sprintf("Hello, %s!", u.Name)
}

func main() {
    user := &User{Name: "John", Age: 30}
    fmt.Println(user.Greet())
    
    for i := 0; i < 10; i++ {
        fmt.Println(i)
    }
    
    switch user.Age {
    case 0:
        fmt.Println("newborn")
    default:
        fmt.Println("older")
    }
}
