data User = User
    { userId :: Int
    , userName :: String
    , userEmail :: Maybe String
    }

greet :: User -> String
greet user = "Hello, " ++ userName user ++ "!"

main :: IO ()
main = do
    let user = User 1 "Alice" (Just "alice@example.com")
    putStrLn $ greet user