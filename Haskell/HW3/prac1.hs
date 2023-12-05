data Filesystem = Folder String [Filesystem]
                | File String
                  deriving (Show)

helperRemoveStartingByA :: Filesystem -> [Filesystem]
helperRemoveStartingByA (File name)
    | head name == 'a' = []
    | otherwise = [File name]
helperRemoveStartingByA (Folder name content)
    | head name == 'a' = []
    | otherwise = [Folder name (concatMap helperRemoveStartingByA content)]

removeStartingByA :: Filesystem -> Filesystem
removeStartingByA item = head (helperRemoveStartingByA item)