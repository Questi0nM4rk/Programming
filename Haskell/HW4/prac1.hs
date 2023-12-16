
ascendingBySteps :: Integer -> Integer -> [Integer]
ascendingBySteps maxStep bound = [i | step <- [1..maxStep], i <- [1,1+step..bound]]