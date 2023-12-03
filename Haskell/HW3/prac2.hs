data BinTree a = Empty
               | Node a (BinTree a) (BinTree a)
               deriving (Show, Eq)

data TreeDirection = LeftChild
               | RightChild
               deriving (Show, Eq)


t1 = Node 1
    (Node 4
        (Node 5 Empty Empty)
        (Node 6 Empty Empty))
    (Node 5
        (Node 8 Empty Empty)
        (Node 1 Empty Empty))

t2 = Node "Elwing"
    (Node "Dior"
        (Node "Beren"
            (Node "Barahir" Empty Empty)
            (Node "Emeldir" Empty Empty))
        (Node "Luthien"
            (Node "Elwe" Empty Empty)
            (Node "Melian" Empty Empty)))
    (Node "Nimloth" Empty Empty)


isNothing :: Maybe a -> Bool
isNothing Nothing = True
isNothing (Just _) = False

treeFind :: (Eq a) => a -> BinTree a -> Maybe [TreeDirection]
treeFind v tree = findPath v tree []

findPath :: (Eq a) => a -> BinTree a -> [TreeDirection] -> Maybe [TreeDirection]
findPath _ Empty _ = Nothing
findPath v (Node x left right) path
    | v == x = Just path
    | otherwise = let leftPath = findInSubtree v left (path ++ [LeftChild])
                      rightPath = findInSubtree v right (path ++ [RightChild])
                  in if (isNothing leftPath) then rightPath else leftPath

findInSubtree :: (Eq a) => a -> BinTree a -> [TreeDirection] -> Maybe [TreeDirection]
findInSubtree v subtree path = findPath v subtree path