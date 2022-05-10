import requests
import json

class sudoku():
    def __init__(self, matrix):
        matrix[0][0] = 1

def main():
    print("Ciao!")
    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
    """ sudoku = sudoku(response) """
    print(response.status_code)
    """ 200 means --> successful """
    print(response.json())
    wjdata = json.loads(response)
    

if __name__ == "__main__":
    main()