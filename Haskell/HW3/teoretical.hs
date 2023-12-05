g :: Char -> Float -> Integer
g = undefined

f :: Maybe Char -> Float -> Integer -> Maybe [Integer]
f Nothing _ _ = Nothing
f (Just x) y z = Just [(g x y), z]