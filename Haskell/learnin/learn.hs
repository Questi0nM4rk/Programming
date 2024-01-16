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

addTwoOffset :: Num a => [a] -> [a] -> [a]
addTwoOffset fst snd = zipWith (+) (tail fst) (init snd)

rev :: [a] -> [a]
rev = foldl (flip (:)) []
-- foldl (\acc x -> x : acc) []

lst :: [Int] = [1,2,3,4,5,6,7,8,9]

prefixes :: [a] -> [[a]]
prefixes = foldr (\x acc -> [x] : map (x :) acc) []

max3 :: Int -> Int -> Int -> Int
max3 x y z= max x (max y z)

f :: String -> String
f = filter (`elem` "M!o")

fn :: [Int] -> [Int]
fn list = zipWith (-) (tail list) (init list)

fnr :: [Int] -> [Int]
fnr [] = []
fnr [x] = []
fnr (x:y:xs) = x + y : fnr (y:xs)

type Code = (Char, Int)
data Allowed = Doors Code | Section Code [Allowed]

allAD :: Allowed -> [Int]
allAD (Doors ('A', nm)) = [nm]
allAD (Doors (_, nm)) = []
allAD (Section (_,_) []) = []
allAD (Section (_,_) (x:xs)) = allAD x ++ allAD (Section ('a', 0) xs)