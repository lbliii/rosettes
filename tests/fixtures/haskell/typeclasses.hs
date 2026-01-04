class Show a where
    show :: a -> String

instance Show User where
    show (User id name email) = name

instance Functor Maybe where
    fmap f Nothing = Nothing
    fmap f (Just x) = Just (f x)