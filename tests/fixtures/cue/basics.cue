package example

#User: {
    id: int
    name: string
    email?: string
}

user: #User & {
    id: 1
    name: "Alice"
}