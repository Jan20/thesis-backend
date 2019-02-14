import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database

class TextFileReader:

  def read_text_file(self, file_name: str) -> [[str]]:

    lines: [str] = []

    string_representation: [str] = []
    
    f = open(file_name, "r")

    for line in f:

      lines.append(line)
      break

    for line in f:

      lines.append(line)

    lines = [lines[0]] + lines

    for line in lines:
      
      line = line.replace('-', '.') # Empty Space to Empty Space
      line = line.replace('\n', '')
      line = line.replace('S', 'B') # Stone to brick
      line = line.replace('Q', 'S') # Coin to Coin
      line = line.replace('[', 'D') # Pipe to Brick
      line = line.replace(']', 'D') # Pipe to Brick
      line = line.replace('<', 'D') # Pipe to Brick
      line = line.replace('>', 'D') # Pipe to Brick
      line = line.replace('?', 'P') # Todo: Find better match
      line = line.replace('E', 'C') # Todo: Find better match Gumba to Bumba
      line = line.replace('o', 'B') # Todo: Find better match Gumba to Bumba
      line = line.replace('b', 'B') # Should result in opponnent type 3
      
      string_representation.append(line)
      
    level_representation: [[str]] = []

    for line in string_representation:

      level_representation.append(list(line))

    last_column: int = len(level_representation[0]) - 1

    level_representation[14][last_column] = 'Z'

    return level_representation

if __name__ == "__main__":
    
    TextFileReader().read_text_file('level_01.txt')
