nums :: [Int] = [1,2,3,4,5,1,2,3,4,5,7,8,9]
ltrs = ["a","b","c","d","q","d","r","a","b","c"]

tree1 :: TreTree Int
tree1 = Node (1, 2) 
  ( Node (3, 4) 
    ( Leaf 5
    , Leaf 6
    , Node (7, 8) 
      ( Leaf 9
      , Leaf 10
      , Node (11, 12)
        ( Leaf 13
        , Leaf 14
        , Leaf 15
        )
      )
    )
  , Node (16, 17)
    ( Leaf 18
    , Node (19, 20)
      ( Leaf 21
      , Leaf 22
      , Node (23, 24)
        ( Leaf 25
        , Leaf 26
        , Leaf 27
        )
      )
    , Leaf 28
    )
  , Node (29, 30)
    ( Leaf 31
    , Node (32, 33)
      ( Leaf 34
      , Leaf 35
      , Node (36, 37)
        ( Leaf 38
        , Leaf 39
        , Leaf 40
        )
      )
    , Leaf 41
    )
  )

tree2 :: TreTree Int
tree2 = Node (1, 2) 
    ( Node (3, 4) 
        ( Leaf 1
        , Leaf 1
        , Node (7, 8) 
        ( Leaf 1
        , Leaf 1
        , Node (11, 12)
            ( Leaf 1
            , Leaf 1
            , Leaf 1
            )
        )
        )
    , Node (16, 17)
        ( Leaf 1
        , Node (19, 20)
        ( Leaf 1
        , Leaf 1
        , Node (23, 24)
            ( Leaf 1
            , Leaf 1
            , Leaf 1
            )
        )
        , Leaf 1
        )
    , Node (29, 30)
        ( Leaf 1
        , Node (32, 33)
        ( Leaf 1
        , Leaf 1
        , Node (36, 37)
            ( Leaf 1
            , Leaf 1
            , Leaf 1
            )
        )
        , Leaf 1
        )
    )

-- 1.
-- map fst( zip( replicate 3 ":") ["A", "B", "C"])

createPairs :: [b] -> [String]
createPairs xs = map fst ( zip (replicate (length xs) ":") xs)

createPairs2 :: [b] -> [String]
createPairs2 xs = zipWith const (replicate (length xs) ":") xs

{-
  replicate 3 ":" = [":", ":", ":"]
  zip [":", ":", ":"] ["A", "B", "C"] = [(":","A"),(":","B"),(":","C")]
  map fst [(":","A"),(":","B"),(":","C")] = fst for each item = [":", ":", ":"]

  returns [":", ":", ":"]
-}

-- 2.

-- a)
sumSuffix2 :: [Int] -> [Int]
sumSuffix2 list = init( scanr (+) 0 list)

sumSuffix3 :: [Int] -> [Int]
sumSuffix3 = init . foldr (\curr accum -> (curr + head accum) : accum) [0]

-- b)
sumSuffix :: [Int] -> [Int]
sumSuffix [] = []
sumSuffix list = sum (tail list) : sumSuffix (tail list)

-- 3.
{-
  \y -> (snd y) ((not.fst) y) :: (Bool, Bool -> x) -> x
  snd y :: a -> b - second item is a function
  not.fst :: Bool - by definition not takes only Bool
  y :: (q, e) - because fst and snd are used on tuples
  q :: Bool - as the fst item needs to be Bool for the not
  e :: a -> b - as the second item needs to be a function
  e :: Bool -> b - as the argument is the first alement which is Bool
  y :: (Bool, Bool -> x)

  lambda \y ... :: (Bool, Bool -> x) -> x - as the only output of the lambda is the output of that function
  exm:
  \y -> fun not(fst y)
-}

-- 4.
data TreTree a = Node (a,a) (TreTree a, TreTree a, TreTree a) | Leaf a
-- a)
randomLeaf = Leaf 'a'

-- b)
data TT = NodeChar(Char, Char) (TT, TT, TT) | LeafChar Char

-- c)
monoLeaf :: Int -> TreTree Int -> Bool
monoLeaf match (Leaf a) = match == a
monoLeaf match (Node (_, _) (left, mid, right)) = monoLeaf match left && monoLeaf match mid && monoLeaf match right

-- advanced Part

-- 5.
decodeRLE :: [(Int, Char)] -> IO ()
decodeRLE [] = return ()
decodeRLE ((count, char):xs) = do
    putStr $ replicate count char
    decodeRLE xs

-- 6.
data ITree a = ILeaf | INode a (ITree a) (ITree a)

-- kmIT is a function that takes three arguments:
-- 1. a value of type 'a' (lf), which is the result for the leaf case
-- 2. a function of type (b -> a -> a -> a) (nf), which is applied to each node of the tree
-- 3. a tree of type ITree b
-- The function returns a value of type 'a'.
kmIT :: a -> (b -> a -> a -> a) -> ITree b -> a
-- If the tree is a leaf (ILeaf), the function returns the leaf case value (lf).
kmIT lf nf ILeaf = lf
-- If the tree is a node (INode v x y), the function applies the node function (nf) to the value at the node (v)
-- and the results of recursively applying kmIT to the left and right subtrees (x and y).
kmIT lf nf (INode v x y) = nf v (kmIT lf nf x) (kmIT lf nf y)

{- 
  In the context of sumITree, we use kmIT to sum all the values in an ITree of Ints.
  We pass 0 as the leaf case value, because the sum of an empty tree is 0.
  We pass a lambda function (\v x y -> v + x + y) as the node function, which adds the value at the node to the sum of the left and right subtrees.
-}

-- sumITree is a function that takes an ITree of Ints and returns the sum of its values.
sumITree :: ITree Int -> Int
sumITree = kmIT 0 (\v x y -> v + x + y)

-- 7.
-- Fing prolog idk cryyy

{-
Copilot code:

    take(_, 0, []).
    
    take([H|T], N, [H|R]) :-
      N > 0,
      N1 is N - 1,
      take(T, N1, R).

-} 