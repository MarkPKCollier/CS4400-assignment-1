data KillServiceMsg = KillService
                    deriving (Show)

data HelloMsg = Hello
            deriving (Show)

data HelloMsgRsp = HelloRsp String Int String
            deriving (Show)

data JoinChatroomMsg = JoinChatroom String String Int String
            deriving (Show)

data JoinChatroomMsgRsp = JoinChatroomRsp String String Int Int Int
            deriving (Show)

data ErrorMsg = Error Int String
            deriving (Show)

data LeaveChatroomMsg = LeaveChatroom Int Int String
            deriving (Show)

data LeaveChatroomMsgRsp = LeaveChatroomRsp Int Int
            deriving (Show)

data DisconnectMsg = Disconnect String Int String
            deriving (Show)

data ChatMsg = Chat Int Int String String
            deriving (Show)

data ChatMsgRsp = ChatRsp Int String String
            deriving (Show)

