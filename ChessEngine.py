import numpy

class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]

        self.board_extend = [
            [56,57,58,59,60,61,62,63],
            [48,49,50,51,52,53,54,55],
            [40,41,42,43,44,45,46,47],
            [32,33,34,35,36,37,38,39],
            [24,25,26,27,28,29,30,31],
            [16,17,18,19,20,21,22,23],
            [ 8, 9,10,11,12,13,14,15],
            [ 0, 1, 2, 3, 4, 5, 6, 7]]

        self.board_notation = [
            ["a8","b8","c8","d8","e8","f8","g8","h8"],
            ["a7","b7","c7","d7","e7","f7","g7","h7"],
            ["a6","b6","c6","d6","e6","f6","g6","h6"],
            ["a5","b5","c5","d5","e5","f5","g5","h5"],
            ["a4","b4","c4","d4","e4","f4","g4","h4"],
            ["a3","b3","c3","d3","e3","f3","g3","h3"],
            ["a2","b2","c2","d2","e2","f2","g2","h2"],
            ["a1","b1","c1","d1","e1","f1","g1","h1"]]
        self.whiteMove = True

    def openingMove(self, move, forward):
        if forward:
            startNotation = move[0:2]
            endNotation = move[2:4]
        else:
            startNotation = move[2:4]
            endNotation = move[0:2]

        for i in range(8):
            for j in range(8):
                if self.board_notation[i][j] == startNotation:
                    startSQ = (i, j)
                elif self.board_notation[i][j] == endNotation:
                    endSQ = (i, j)
                    
        if startSQ != endSQ:
            piece = self.board[startSQ[0]][startSQ[1]]
            self.board[startSQ[0]][startSQ[1]] = "--"
            self.board[endSQ[0]][endSQ[1]] = piece

    def makeMove(self, startSQ, endSQ):
        piece = self.board[startSQ[0]][startSQ[1]]
        if piece == "bp" or piece == "wp":
            self.pawnMove(piece, startSQ, endSQ)
        elif piece == "bR" or piece == "wR":
            self.rookMove(piece, startSQ, endSQ)
        elif piece == "bN" or piece == "wN":
            self.knightmove(piece, startSQ, endSQ)
        elif piece == "bB" or piece == "wB":
            self.bishopMove(piece, startSQ, endSQ)
        elif piece == "bK" or piece == "wK":
            self.kingMove(piece, startSQ, endSQ)
        elif piece == "bQ" or piece == "wQ":
            self.queenMove(piece, startSQ, endSQ)
        
    def pawnMove(self, piece, startSQ, endSQ):
        legal_moves = []
        white_pieces = ["wp","wB","wN","wR","wK","wQ"]
        black_pieces = ["bp","bB","bN","bR","bK","bQ"]
        value_init = self.board_extend[startSQ[0]][startSQ[1]]
        value_final = self.board_extend[endSQ[0]][endSQ[1]]

        if self.whiteMove == True:
            pos_left = numpy.subtract(startSQ,(1,1))
            pos_right = numpy.add(startSQ,(-1,1))
            pos_ahead = numpy.add(startSQ,(-1,0))
            pos_ahead_2 = numpy.add(startSQ,(-2,0))

            if 7 < value_init and value_init < 16:
                if self.board[pos_ahead[0]][pos_ahead[1]] == "--":
                    legal_moves.append(value_init + 8)

                if self.board[pos_ahead_2[0]][pos_ahead_2[1]] == "--":
                    legal_moves.append(value_init + 16)

                if pos_left[1] != -1 and pos_right[1] != 8:
                    if self.board[pos_right[0]][pos_right[1]] in black_pieces:
                        legal_moves.append(value_init + 9)
                    if self.board[pos_left[0]][pos_left[1]] in black_pieces:
                        legal_moves.append(value_init + 7)

            elif value_init >= 16:
                if self.board[pos_ahead[0]][pos_ahead[1]] == "--":
                    legal_moves.append(value_init + 8)

                if pos_left[1] != -1 and pos_right[1] != 8:
                    if self.board[pos_right[0]][pos_right[1]] in black_pieces:
                        legal_moves.append(value_init + 9)
                    if self.board[pos_left[0]][pos_left[1]] in black_pieces:
                        legal_moves.append(value_init + 7)

            if value_final in legal_moves:
                self.board[startSQ[0]][startSQ[1]] = "--"
                self.board[endSQ[0]][endSQ[1]] = piece
                self.whiteMove = False
                legal_moves.clear()
        
        elif self.whiteMove == False:
            pos_right = numpy.subtract(startSQ,(-1,1))
            pos_left = numpy.add(startSQ,(1,1))
            pos_ahead = numpy.add(startSQ,(1,0))
            pos_ahead_2 = numpy.add(startSQ,(2,0))

            if 47 < value_init and value_init < 56:
                if self.board[pos_ahead[0]][pos_ahead[1]] == "--":
                    legal_moves.append(value_init - 8)

                if self.board[pos_ahead_2[0]][pos_ahead_2[1]] == "--":
                    legal_moves.append(value_init - 16)

                if pos_left[1] != 8 and pos_right[1] != -1:
                    if self.board[pos_right[0]][pos_right[1]] in white_pieces:
                        legal_moves.append(value_init - 9)
                    if self.board[pos_left[0]][pos_left[1]] in white_pieces:
                        legal_moves.append(value_init - 7)
            elif value_init <= 47:
                if self.board[pos_ahead[0]][pos_ahead[1]] == "--":
                    legal_moves.append(value_init - 8)
                if pos_left[1] != 8 and pos_right[1] != -1:
                    if self.board[pos_right[0]][pos_right[1]] in white_pieces:
                        legal_moves.append(value_init - 9)
                    if self.board[pos_left[0]][pos_left[1]] in white_pieces:
                        legal_moves.append(value_init - 7)

            if value_final in legal_moves:
                self.board[startSQ[0]][startSQ[1]] = "--"
                self.board[endSQ[0]][endSQ[1]] = piece
                self.whiteMove = True
                legal_moves = []

    def knightmove(self, piece, startSQ, endSQ):
        white_pieces = ["wp","wB","wN","wR","wK","wQ"]
        black_pieces = ["bp","bB","bN","bR","bK","bQ"]
        legal_moves = []
        legal_pos = []

        if self.whiteMove == True:
            legal_pos.append(numpy.add(startSQ,(-2,-1)))
            legal_pos.append(numpy.add(startSQ,(-2,1)))
            legal_pos.append(numpy.add(startSQ,(-1,2)))
            legal_pos.append(numpy.add(startSQ,(1,2)))
            legal_pos.append(numpy.add(startSQ,(2,1)))
            legal_pos.append(numpy.add(startSQ,(2,-1)))
            legal_pos.append(numpy.add(startSQ,(1,-2)))
            legal_pos.append(numpy.add(startSQ,(-1,-2)))

            for pos in legal_pos:
                if pos[0] not in range(8):
                    continue
                elif pos[1] not in range(8):
                    continue
                elif self.board[pos[0]][pos[1]] in white_pieces:
                    continue
                else:
                    legal_moves.append(pos)
                
            if piece == "bN": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = False
                    legal_moves.clear()

        elif self.whiteMove == False:
            legal_pos.append(numpy.add(startSQ,(-2,-1)))
            legal_pos.append(numpy.add(startSQ,(-2,1)))
            legal_pos.append(numpy.add(startSQ,(-1,2)))
            legal_pos.append(numpy.add(startSQ,(1,2)))
            legal_pos.append(numpy.add(startSQ,(2,1)))
            legal_pos.append(numpy.add(startSQ,(2,-1)))
            legal_pos.append(numpy.add(startSQ,(1,-2)))
            legal_pos.append(numpy.add(startSQ,(-1,-2)))

            for pos in legal_pos:
                if pos[0] not in range(8):
                    continue
                elif pos[1] not in range(8):
                    continue
                elif self.board[pos[0]][pos[1]] in black_pieces:
                    continue
                else:
                    legal_moves.append(pos)
                
            if piece == "wN": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = True
                    legal_moves.clear()

    def rookMove(self, piece, startSQ, endSQ):
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        white_pieces = ["wp","wB","wN","wR","wK","wQ"]
        black_pieces = ["bp","bB","bN","bR","bK","bQ"]
        legal_moves = []
        end_pos = {}
        
        if self.whiteMove == True:
            for direc in directions:
                for i in range(1,8):
                    end_pos[0] = startSQ[0] + direc[0] * i
                    end_pos[1] = startSQ[1] + direc[1] * i
                    if 0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8:
                        if self.board[end_pos[0]][end_pos[1]] == "--":
                            legal_moves.append((end_pos[0], end_pos[1]))
                        elif self.board[end_pos[0]][end_pos[1]] in black_pieces:
                            legal_moves.append((end_pos[0], end_pos[1]))
                            break
                        else: break
                    else: break
            
            if piece == "bR": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = False
                    legal_moves.clear()

        if self.whiteMove == False:
            for direc in directions:
                for i in range(1,8):
                    end_pos[0] = startSQ[0] + direc[0] * i
                    end_pos[1] = startSQ[1] + direc[1] * i
                    if 0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8:
                        if self.board[end_pos[0]][end_pos[1]] == "--":
                            legal_moves.append((end_pos[0], end_pos[1]))
                        elif self.board[end_pos[0]][end_pos[1]] in white_pieces:
                            legal_moves.append((end_pos[0], end_pos[1]))
                            break
                        else: break
                    else: break
            
            if piece == "wR": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = True
                    legal_moves.clear()

    def bishopMove(self, piece, startSQ, endSQ):
        directions = ((-1,1), (1,-1), (1,1), (-1,-1))
        white_pieces = ["wp","wB","wN","wR","wK","wQ"]
        black_pieces = ["bp","bB","bN","bR","bK","bQ"]
        legal_moves = []
        end_pos = {}
        
        if self.whiteMove == True:
            for direc in directions:
                for i in range(1,8):
                    end_pos[0] = startSQ[0] + direc[0] * i
                    end_pos[1] = startSQ[1] + direc[1] * i
                    if 0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8:
                        if self.board[end_pos[0]][end_pos[1]] == "--":
                            legal_moves.append((end_pos[0], end_pos[1]))
                        elif self.board[end_pos[0]][end_pos[1]] in black_pieces:
                            legal_moves.append((end_pos[0], end_pos[1]))
                            break
                        else: break
                    else: break
            
            if piece == "bB": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = False
                    legal_moves.clear()

        if self.whiteMove == False:
            for direc in directions:
                for i in range(1,8):
                    end_pos[0] = startSQ[0] + direc[0] * i
                    end_pos[1] = startSQ[1] + direc[1] * i
                    if 0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8:
                        if self.board[end_pos[0]][end_pos[1]] == "--":
                            legal_moves.append((end_pos[0], end_pos[1]))
                        elif self.board[end_pos[0]][end_pos[1]] in white_pieces:
                            legal_moves.append((end_pos[0], end_pos[1]))
                            break
                        else: break
                    else: break
            
            if piece == "wB": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = True
                    legal_moves.clear()
                
    def kingMove(self, piece, startSQ, endSQ):
        directions = ((-1,1), (1,-1), (1,1), (-1,-1),(-1,0), (0,-1), (1,0), (0,1))
        white_pieces = ["wp","wB","wN","wR","wK","wQ"]
        black_pieces = ["bp","bB","bN","bR","bK","bQ"]
        legal_moves = []
        end_pos = {}
        
        if self.whiteMove == True:
            for direc in directions:
                for i in range(1,8):
                    end_pos[0] = startSQ[0] + direc[0]
                    end_pos[1] = startSQ[1] + direc[1]
                    if 0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8:
                        if self.board[end_pos[0]][end_pos[1]] == "--":
                            legal_moves.append((end_pos[0], end_pos[1]))
                        elif self.board[end_pos[0]][end_pos[1]] in black_pieces:
                            legal_moves.append((end_pos[0], end_pos[1]))
                            break
                        else: break
                    else: break

            if piece == "bK": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = False
                    legal_moves.clear()
        elif self.whiteMove == False:
            for direc in directions:
                for i in range(1,8):
                    end_pos[0] = startSQ[0] + direc[0] * i
                    end_pos[1] = startSQ[1] + direc[1] * i
                    if 0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8:
                        if self.board[end_pos[0]][end_pos[1]] == "--":
                            legal_moves.append((end_pos[0], end_pos[1]))
                        elif self.board[end_pos[0]][end_pos[1]] in white_pieces:
                            legal_moves.append((end_pos[0], end_pos[1]))
                            break
                        else: break
                    else: break
            
            if piece == "wK": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = True
                    legal_moves.clear()

    def queenMove(self, piece, startSQ, endSQ):
        directions = ((-1,1), (1,-1), (1,1), (-1,-1),(-1,0), (0,-1), (1,0), (0,1))
        white_pieces = ["wp","wB","wN","wR","wK","wQ"]
        black_pieces = ["bp","bB","bN","bR","bK","bQ"]
        legal_moves = []
        end_pos = {}
        
        if self.whiteMove == True:
            for direc in directions:
                end_pos[0] = startSQ[0] + direc[0] 
                end_pos[1] = startSQ[1] + direc[1]
                if 0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8:
                    if self.board[end_pos[0]][end_pos[1]] == "--":
                        legal_moves.append((end_pos[0], end_pos[1]))
                    elif self.board[end_pos[0]][end_pos[1]] in black_pieces:
                        legal_moves.append((end_pos[0], end_pos[1]))
                        break
                    else: break
                    
            
            if piece == "bK": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = False
                    legal_moves.clear()

        if self.whiteMove == False:
            for direc in directions:
                end_pos[0] = startSQ[0] + direc[0]
                end_pos[1] = startSQ[1] + direc[1]
                if 0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8:
                    if self.board[end_pos[0]][end_pos[1]] == "--":
                        legal_moves.append((end_pos[0], end_pos[1]))
                    elif self.board[end_pos[0]][end_pos[1]] in white_pieces:
                        legal_moves.append((end_pos[0], end_pos[1]))
                        break
                    else: break
            
            if piece == "wK": legal_moves = []
            for pos in legal_moves:
                if endSQ[0] == pos[0] and endSQ[1] == pos[1]:
                    self.board[startSQ[0]][startSQ[1]] = "--"
                    self.board[endSQ[0]][endSQ[1]] = piece
                    self.whiteMove = True
                    legal_moves.clear()
