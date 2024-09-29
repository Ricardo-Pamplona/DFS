import time
import tracemalloc
import numpy as np

def is_valid(board, row, col, num, rows, cols, grids):
    grid = (row // 3) * 3 + (col // 3)  
    # Verifica se o número `num` não está presente na linha, coluna ou bloco atual
    return not (num in rows[row] or num in cols[col] or num in grids[grid])

def is_board_valid(board):
    # Inicializa conjuntos para rastrear números em linhas, colunas e blocos
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    grids = [set() for _ in range(9)]
    
    # Preenche os conjuntos com os números já presentes no tabuleiro
    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num:
                grid = (r // 3) * 3 + (c // 3)
                if num in rows[r] or num in cols[c] or num in grids[grid]:
                    return False
                rows[r].add(num)
                cols[c].add(num)
                grids[grid].add(num)
    return True

def solver(board):
    def dfs():
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for n in range(1, 10):
                        if is_valid(board, r, c, n, rows, cols, grids):
                            board[r][c] = n
                            rows[r].add(n)
                            cols[c].add(n)
                            grids[(r // 3) * 3 + (c // 3)].add(n)
                            if dfs():
                                return True
                            board[r][c] = 0
                            rows[r].remove(n)
                            cols[c].remove(n)
                            grids[(r // 3) * 3 + (c // 3)].remove(n)
                    return False
        return True
    
    # Inicializa conjuntos para rastrear números em linhas, colunas e blocos
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    grids = [set() for _ in range(9)]
    
    # Preenche os conjuntos com os números já presentes no tabuleiro
    for r in range(9):
        for c in range(9):
            n = board[r][c]
            if n:
                rows[r].add(n)
                cols[c].add(n)
                grids[(r // 3) * 3 + (c // 3)].add(n)
    
    # Verifica se o tabuleiro é válido antes de iniciar a resolução
    if not is_board_valid(board):
        print("Tabuleiro inválido")
        return
    
    # Inicia a resolução do Sudoku
    dfs()

def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        row_str = ""
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += str(num) if num != 0 else "."
            row_str += " "
        print(row_str)

# Exemplo de quebra-cabeça Sudoku (0 representa células vazias)
sudoku_boards = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
] * 50

times = []
memories = []

for sudoku_board in sudoku_boards:
    tracemalloc.start()
    start_time = time.time()

    solver(sudoku_board)

    end_time = time.time()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time
    memory_usage = peak_memory / 1024  # Converte para KB

    times.append(execution_time)
    memories.append(memory_usage)

# Calcula e exibe as estatísticas
mean_time = np.mean(times)
std_time = np.std(times)
mean_memory = np.mean(memories)
std_memory = np.std(memories)

print(f"Média de tempo: {mean_time:.4f} segundos")
print(f"Desvio padrão do tempo: {std_time:.4f} segundos")
print(f"Média de memória: {mean_memory:.2f} KB")
print(f"Desvio padrão da memória: {std_memory:.2f} KB")
