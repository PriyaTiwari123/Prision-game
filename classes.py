class game_map:
    def __init__(self, map_file, guard_file):
        # initalizes the game map class and stores its attributes.
        self.direction = None
        self.map_file = map_file
        self.guard_file = guard_file
        # stores the 2d list of the grid
        self.current_grid = []
        # stores the guard objects in a list
        self.guard_object_list = []
        self.player_row = 0
        self.player_col = 0
        try:
            # opens the map file
            map_file = open(map_file)
            # reads the first line from the map file
            file_line_map = map_file.readline()
            # reads the file until the last line in the file.
            while file_line_map != "":
                file_line_map = file_line_map.rstrip()  # removes any character at the end of the string
                grid = [item for item in file_line_map]  # places each item in the line in a list
                self.current_grid.append(grid)  # adds the list into another list to form a 2d list.
                file_line_map = map_file.readline()
                # looks for the escape point in the 2d list and stores its value in a variable for future use.
            for row in range(12):
                for col in range(16):
                    if self.current_grid[row][col] == "E":
                        self.exit_row = row
                        self.exit_col = col
            # opens the guard file.
            guard_file = open(guard_file)
            file_line_guard = guard_file.readline()
            # reads the file until the last line in the file.
            while file_line_guard != "":
                file_line_guard = file_line_guard.rstrip()  # removes any character at the end of the string.
                file_line_guard = file_line_guard.split()
                # stores the first split value as row of the guard
                row = int(file_line_guard[0])
                # stores the second split value as colum of the guard
                col = int(file_line_guard[1])
                # stores the third split value as the attack range of the guard
                attack_range = int(file_line_guard[2])
                # stores any character from the fourth to the last value in the list as the movement of the guard.
                movements = file_line_guard[3:len(file_line_guard)]

                # creates each guard as an object of the guard class and adds it to a list.
                obj = guard(row, col, attack_range, movements)
                self.guard_object_list.append(obj)
                # Places Guard on the grid based on their row and column location.
                self.current_grid[row][col] = "G"

                file_line_guard = guard_file.readline()

        # File cannot be opened.
        except FileNotFoundError:
            print("Sorry, file not found")

    def get_grid(self):
        # returns the 2d list which is used to create the grid of the map containing wall, player, guard, exit,
        # and empty space.
        return self.current_grid

    def get_guards(self):
        # returns a list containing objects, where each object represents a guard.
        return self.guard_object_list

    def update_player(self, direction):
        self.direction = direction
        # searches the 2d list for the player and replaces the player with an empty space.
        for row in range(len(self.current_grid)):
            for col in range(len(self.current_grid[row])):
                if self.current_grid[row][col] == "P":
                    self.current_grid[row][col] = " "
                    self.player_row = row
                    self.player_col = col

        # based on the direction movement of the player, the new player position is placed on the 2d list if a wall
        # does not exist in that place.
        if (self.direction == "U") and (self.current_grid[self.player_row - 1][self.player_col] != "#"):
            self.current_grid[self.player_row - 1][self.player_col] = "P"
            self.player_row = self.player_row - 1
        elif (self.direction == "D") and (self.current_grid[self.player_row + 1][self.player_col] != "#"):
            self.current_grid[self.player_row + 1][self.player_col] = "P"
            self.player_row = self.player_row + 1
        elif (self.direction == "R") and (self.current_grid[self.player_row][self.player_col + 1] != "#"):
            self.current_grid[self.player_row][self.player_col + 1] = "P"
            self.player_col = self.player_col + 1
            print(f"self.playerrow{self.player_row},self.playercol{self.player_col}")
        elif (self.direction == "L") and (self.current_grid[self.player_row][self.player_col - 1] != "#"):
            self.current_grid[self.player_row][self.player_col - 1] = "P"
            self.player_col = self.player_col - 1
        else:
            # if there is a wall, then the player skips the turn and stays at its current location.
            self.current_grid[self.player_row][self.player_col] = "P"


    def update_guards(self):
        # the current location of each guard and the new location based on the move method is obtained.
        for ob in self.guard_object_list:
            current_row, current_col = ob.get_location()
            ob_location = ob.move(self.current_grid)

            # removes the guard against its current position and places it in the new location based on its movement,
            # if the new location is within the gird's range.
            if 0 <= ob_location[0] < len(self.current_grid) and 0 <= ob_location[1] < len(self.current_grid[1]):
                self.current_grid[current_row][current_col] = " "
                self.current_grid[ob_location[0]][ob_location[1]] = "G"

    def player_wins(self):
        # check's if the player's position is on the position of the exit to determine whether the player wins or not.
        for row in range(12):
            for col in range(16):
                if (self.player_row == self.exit_row) and (self.player_col == self.exit_col):
                    return True
                else:
                    return False
                # returns a boolean value to determine if the player wins or not.

    def player_loses(self):
        # stores the boolean value obtained from the enemy_in_range method in a list that determines if the player
        # has stepped into the guards attack range. checks if a "True" value exit in the list to determine whether a
        # player lost, and then returns a boolean value to determine that.
        num = []
        for i, ob in enumerate(self.guard_object_list):
            num.append(ob.enemy_in_range(self.player_row, self.player_col))
        if True in num:
            return True
        else:
            return False


class guard:
    def __init__(self, row, col, attack_range, movements):
        # initializes the guard class and stores its attributes.
        self.current_grid = None
        self.row = int(row)
        self.col = int(col)
        self.attack_range = int(attack_range)
        self.movements = movements
        self.num = 0

    def get_location(self):
        # returns the current location of the guard as a tuple(row,col).
        return self.row, self.col

    def move(self, current_grid):
        self.current_grid = current_grid
        #  Goes through the movement list for the guard and updates the guards row and col position accordingly.
        if self.movements[self.num] == "U" and self.current_grid[self.row - 1][self.col] == " ":
            self.num += 1
            self.row -= 1
        elif self.movements[self.num] == "D" and self.current_grid[self.row + 1][self.col] == " ":
            self.num += 1
            self.row += 1
        elif self.movements[self.num] == "L" and self.current_grid[self.row][self.col - 1] == " ":
            self.num += 1
            self.col -= 1
        elif self.movements[self.num] == "R" and self.current_grid[self.row][self.col + 1] == " ":
            self.num += 1
            self.col += 1
        else:
            # skips the guards movement turn, if the guard does not have an empty space to move onto.
            self.num += 1
        # resets the index of the movement list to the start of the list when the end of the list is reached.
        if self.num >= len(self.movements):
            self.num = 0

        # returns the new row and column to the update guard method in class game_map, based on the guards movement
        # that is determined by the movement list.
        return self.row, self.col

    def enemy_in_range(self, enemy_row, enemy_col):
        # checks whether the player(enemy) is within the guard's attack range.
        self.player_x = enemy_row
        self.player_y = enemy_col
        # calculates the lower and higher range for the row and column of the guard based on the attack range.
        num = (self.row - self.attack_range)
        num_1 = (self.row + self.attack_range)
        col_num = (self.col - self.attack_range)
        col_num_1 = (self.col + self.attack_range)

        # calculates the manhattan distance based on the guards and players position.
        distance = abs(self.row - self.player_x) + abs(self.col - self.player_y)

        # if the player is in the row and the column within the guard's attack range.
        if ((enemy_row in range(num, num_1 + 1)) and (enemy_col == self.col)) or (
                (enemy_col in range(col_num, col_num_1)) and (enemy_row == self.row)):
            return True
        # checks if the value obtained from the manhattan distance is smaller than the attack range, to determine if
        # the player is in guards attack range.
        elif distance <= self.attack_range:
            return True
        else:
            return False

        # a boolean value is returned that determines whether the player is in guards attach range or not.
