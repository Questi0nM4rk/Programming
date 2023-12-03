data Direction = North | East | South | West deriving (Show, Eq)
data State = State Int Int Direction deriving (Show, Eq)
data Instruction = TurnLeft | TurnRight | Forward Int deriving (Show, Eq)

turn :: Direction -> Instruction -> Direction
turn North TurnLeft = West
turn North TurnRight = East
turn East TurnLeft = North
turn East TurnRight = South
turn South TurnLeft = East
turn South TurnRight = West
turn West TurnLeft = South
turn West TurnRight = North

move :: Direction -> Int -> Int -> Int -> State
move North n x y = State x (y + n) North
move East n x y = State (x + n) y East
move South n x y = State x (y - n) South
move West n x y = State (x - n) y West

instructionHelper :: State -> Instruction -> State
instructionHelper (State x y direction) TurnLeft = State x y (turn direction TurnLeft)
instructionHelper (State x y direction) TurnRight = State x y (turn direction TurnRight)
instructionHelper (State x y direction) (Forward n) = move direction n x y

executeInstructions :: [Instruction] -> State -> State
executeInstructions instructions initialState = foldl instructionHelper initialState instructions