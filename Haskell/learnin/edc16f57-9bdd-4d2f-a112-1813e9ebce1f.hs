elemm :: (Eq a) => a -> [a] -> Bool
elemm _ [] = False
elemm el (x:xs) = (el == x) || elemm el xs

nubb :: (Eq a) => [a] -> [a]
nubb [] = []
nubb (x:xs)
    | x `elem` xs = nubb xs
    | otherwise = x : nubb xs

isAsc :: [Int] -> Bool
isAsc [] = True
isAsc [x] = True
isAsc [x,y] = x <= y
isAsc (x:y:xs)
    | x <= y = isAsc xs
    | otherwise = False
