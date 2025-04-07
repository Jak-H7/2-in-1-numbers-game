from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/high_roll', methods=['GET', 'POST'])
def high_roll():
    if request.method == 'POST':
        user_number = int(request.form['number'])
        roll = random.randint(1, 6)
        result = 'win' if user_number > roll else 'lose'
        return render_template('high_roll.html', result=result, roll=roll, user_number=user_number)
    return render_template('high_roll.html', result=None)

@app.route('/low_roll', methods=['GET', 'POST'])
def low_roll():
    if request.method == 'POST':
        user_number = int(request.form['number'])
        roll = random.randint(1, 6)
        result = 'win' if user_number < roll else 'lose'
        return render_template('low_roll.html', result=result, roll=roll, user_number=user_number)
    return render_template('low_roll.html', result=None)

@app.route('/sudoku', methods=['GET', 'POST'])
def sudoku():
    if request.method == 'POST':
        grid = [[int(request.form.get(f'cell_{i}_{j}', 0)) for j in range(4)] for i in range(4)]
        is_valid = is_valid_sudoku(grid)
        return render_template('sudoku.html', grid=grid, result='correct' if is_valid else 'incorrect')
    else:
        grid = generate_random_sudoku()
        return render_template('sudoku.html', grid=grid, result=None)

def generate_random_sudoku():
    base = [1, 2, 3, 4]
    grid = [[0]*4 for _ in range(4)]
    for i in range(4):
        random.shuffle(base)
        grid[i] = base[:]
    for _ in range(6):
        i, j = random.randint(0, 3), random.randint(0, 3)
        grid[i][j] = 0
    return grid

def is_valid_sudoku(grid):
    for i in range(4):
        row = [n for n in grid[i] if n != 0]
        col = [grid[j][i] for j in range(4) if grid[j][i] != 0]
        if len(row) != len(set(row)) or len(col) != len(set(col)):
            return False
    return True

@app.route('/help')
def help_page():
    return render_template('help.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
