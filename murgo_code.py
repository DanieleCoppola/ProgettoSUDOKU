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
    response_json = response.json()
    print(response_json['board'][0][0])
    for i in range (len(response_json['board'][0])):
        for j in range (len(response_json['board'][0])):
            print(response_json['board'][j][i], end = " ")
        print("\n")

if __name__ == "__main__":
    main()


""" La memoria è una funzione psichica e neurale di assimilazione """