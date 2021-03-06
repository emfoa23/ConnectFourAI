# 착수 가능한 곳을 찾아주는 함수
def declareAvailableBettingPoint(map, available_betting_point_address, option):
    new_available_betting_point_address = []
    # initial state이 주어지지 않았을때
    if option == 0:
        for point in available_betting_point_address:
            if map[point[0]][point[1]-1] == 0:
                new_available_betting_point_address.append(point)
            elif point[0] + 1 < 6:
                new_available_betting_point_address.append([point[0]+1, point[1]])
    # initial state이 주어졌을때
    elif option == 1:
        for i in range(7):
            for j in range(6):
                if map[j][i] == 0:
                    new_available_betting_point_address.append([j,i+1])
                    break
        option = 0
    return new_available_betting_point_address, option

# 선택한 열에 착수하는 함수
def betting(turn, map, available_betting_point_address, is_first_turn, turn_count, state, last_betting_point):
    # Import
    from random import randint
    from .AI import connect4AI

    human_bet = 0
    # 사람 차례
    if turn == 1:
        while human_bet != '1' and human_bet != '2' and human_bet != '3' and human_bet != '4' and human_bet != '5' and human_bet != '6' and human_bet != '7':
            human_bet = input("Where do you want to bet? (1~7) : ")
            if human_bet != '1' and human_bet != '2' and human_bet != '3' and human_bet != '4' and human_bet != '5' and human_bet != '6' and human_bet != '7':
                print("Wrong Input. Please try it again.")
            else:
                for point in available_betting_point_address:
                    if int(human_bet) == point[1]:
                        map[point[0]][int(human_bet)-1] = 1
                        # 마지막 착수점 저장
                        last_betting_point[0] = point[0]
                        last_betting_point[1] = int(human_bet) - 1
                        if is_first_turn:
                            available_betting_point_address.insert(3,[0,4])
                            is_first_turn = False
                        return map, True, last_betting_point, is_first_turn, available_betting_point_address
                if is_first_turn:
                    print("You can't bet in column 4 at the first turn")
                else:
                    print("Column " + human_bet + " is already full. Please select another column.")
                return map, False, last_betting_point, is_first_turn, available_betting_point_address
    # 컴퓨터 차례
    else:
        cpu_bet_row, cpu_bet_column = connect4AI(available_betting_point_address, map, turn, turn_count, state, last_betting_point)
        map[cpu_bet_row][cpu_bet_column-1] = -1
        # 마지막 착수점 저장
        last_betting_point[0] = cpu_bet_row
        last_betting_point[1] = cpu_bet_column - 1
        if is_first_turn:
            available_betting_point_address.insert(3, [0, 4])
            is_first_turn = False
        if last_betting_point[0] == 0:
            alphabet = 'A'
        elif last_betting_point[0] == 1:
            alphabet = 'B'
        elif last_betting_point[0] == 2:
            alphabet = 'C'
        elif last_betting_point[0] == 3:
            alphabet = 'D'
        elif last_betting_point[0] == 4:
            alphabet = 'E'
        else:
            alphabet = 'F'
        print("( CPU betted",alphabet+str(cpu_bet_column),")")
        return map, True, last_betting_point, is_first_turn, available_betting_point_address

# 착수할 열을 선택하고 착수 결과를 보여주는 함수
def gameProgressing(map, turn, state ,available_betting_point_address, is_first_turn, turn_count, last_betting_point):
    success_betting = False
    dot = [['.'] * 7 for i in range(6)]
    if turn == -1:
        whos_turn = "CPU"
    else:
        whos_turn = "Human"
    print("---------------------------------------")
    print("("+whos_turn+")","Turn",int((turn_count/2)+1))
    while not success_betting:
        map, success_betting, last_betting_point, is_first_turn, available_betting_point_address = betting(turn, map, available_betting_point_address, is_first_turn, turn_count, state, last_betting_point)
    state.append(last_betting_point[1]+1)
    for i in range(6):
        for j in range(7):
            if map[i][j] == 1:
                dot[i][j] = '○'
            elif map[i][j] == -1:
                dot[i][j] = '●'
            else:
                dot[i][j] = '.'
    print()
    print("# 1 2 3 4 5 6 7 #")
    print('F', dot[5][0], dot[5][1], dot[5][2], dot[5][3], dot[5][4], dot[5][5], dot[5][6], '#')
    print('E', dot[4][0], dot[4][1], dot[4][2], dot[4][3], dot[4][4], dot[4][5], dot[4][6], '#')
    print('D', dot[3][0], dot[3][1], dot[3][2], dot[3][3], dot[3][4], dot[3][5], dot[3][6], '#')
    print('C', dot[2][0], dot[2][1], dot[2][2], dot[2][3], dot[2][4], dot[2][5], dot[2][6], '#')
    print('B', dot[1][0], dot[1][1], dot[1][2], dot[1][3], dot[1][4], dot[1][5], dot[1][6], '#')
    print('A', dot[0][0], dot[0][1], dot[0][2], dot[0][3], dot[0][4], dot[0][5], dot[0][6], '#')
    print("# # # # # # # # #")
    print()
    print("You: ○ , CPU: ●")
    turn *= -1  # 턴 바꾸기
    turn_count += 1
    return map, turn, last_betting_point, state, is_first_turn, turn_count    # 맵, 누구턴인지, 마지막 착수점, state 리턴