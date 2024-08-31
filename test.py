from collections import deque

def route_exists(from_row, from_column, to_row, to_column, map_matrix):
    rows = len(map_matrix)
    columns = len(map_matrix[0])
    # Check if input is invalid
    if (not (0 <= from_row < rows and 0 <= from_column < columns)) or (not (0 <= to_row < rows and 0 <= to_column < columns)):
        return False
    if not map_matrix[from_row][from_column] or  not map_matrix[to_row][to_column]:
        return False

    directions = [(1,0),(-1,0),(0,-1),(0,1)]

    queue = deque([(from_row, from_column)])
    visited =set()
    visited.add((from_row, from_column))

    while queue:
        r, c = queue.popleft()

        if (r, c ) == (to_row, to_column):
            return True
        for dr, dc in directions:
            nr,nc = r+dr, r+dc
            if ((nr, nc) not in visited and map_matrix[nr][nc] and 0 <= nr < rows and 0 <= nc < columns):
                queue.append((nr, nc))
                visited.add((nr, nc))
    return False

    
if __name__ == '__main__':
    map_matrix = [
        [True, False, False],
        [True, True, False],
        [False, True, True]
    ];

    print(route_exists(0, 0, 2, 2, map_matrix))

# from datetime import datetime
# def convert_to_date(date_string):
#    return datetime.strptime(date_string, "%Y/%m")
# class Problem:
#   def convert_to_date(date_string):
#    return datetime.strptime(date_string, "%Y/%m")
#   def findMax(history):
#     # curr_date = datetime.now().date
#     count = 0
#     for i in range(len(history)):
#         date1 = convert_to_date(history[i][2])
#         date2 = convert_to_date(history[i][1])
#         diff = date1 - date2
#         if diff.days < 0:
#            continue
#         else:
#            count+=1
#     return count
        
    

# history = [[1, "1997/01", "1007/01"], [2, "1998/03", "2009/04"], [3, "2005/04", "2005/05"]]
# print(Problem.findMax(history))