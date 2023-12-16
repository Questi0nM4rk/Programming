f :: Eq a => a -> [[a]] -> [[a]]
f currentElement [] = [[currentElement]]
f currentElement (group:remainingGroups)
  | currentElement == head group = (currentElement:group):remainingGroups
  | otherwise = [currentElement]:group:remainingGroups

initialValue :: [[a]]
initialValue = []

group :: Eq a => [a] -> [[a]]
group xs = foldr f initialValue xs