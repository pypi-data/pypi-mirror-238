from stringsan.strings import occurrences, first_occurrence, last_occurrence, is_zalgo, random_occurrence

PATTERN = "hi"
STRING = "Hi, my name is hi man. He is hi hi man."
ZALGO = """
H̶̴̨̜̣͚̬͖̝̞̼͚̝̱̬̳̜̠͙̪͓͖̥̬͕̞̜̲͖̦̙̗̝̤̙̺̖̭̪̭̹̗̘̙̙͇̣͙̼͚̠͔̩̭͉͙̞̜̖̦̙̟̖͈͚͉̩̺̦͎̫̗̖̜̠̤̬̟̪͈̬͔̣̩̙̤̱͇̳̙̪̗̞͓͓͎̙̞̺͈͈̪͕̤̳̣̲̬̺̥͎̗̞̙̠̱̦̖͓̥̙̭̲̬̬̟̦̺̘̣̞̳͉̪̫̤̮͕̺̤̪̼̜̹͍̲̖͇̳̼̬̲͈̜̘͉̜̪̝̼͉̬͍̝̹̪̪͉̜̲̜̹̮̪͓̤̦̗͈̣̗̠̜̝̱̲̞̝̰̖̹̝̹̦̱͈̥͈͇̭̲͚̱̙̹̭̝͇͔̖̬̭̭͚͙͉̩̬̣̥̦͓̫̤̙̜̪̤͓̱̟͍̖͙̞̥͚̬̞͙̠͍̺̞͓̠̖͕̬͎̘̼̰̲̠͔͇̹̖͚̝͙͔̮̬̠̝͎̙̺̘͚͎̩̠̘̭͉͈͙͖͍̣̰̥͉̬͔͇̹̮̜̤͈͍̤̹̲͍͇͕̮͙̪̝͍̬̜̟̻̼͎̙͔͕̳̻͍̰̹̮͕͕͍͈͇̺̞͔̘̦̜̠̠̹̪͇͙͙͉̘̜̩͓͎̥̰̮͇͕̥̟̜̻̦͕̮̜͕̭͍̠̣̲͇̹̟̻̘͓̬͔̥̜̻̪̭̖͔̗͙͓̩̺̜̥͎̲̠͚̝͕̣̱̦͓͕̙͓̺̠̬̦͕͍̟̦̥̙̼̦̜̞̝͕̬̼̙̬̜͕̘̲͙̟͇̩͚̣̺̳̻͖̹͉͖͔̥͎̣̜̙̪̤͉̩̝̼̺͇̙̳̮̪̣͔̥̹̮̜̲̦̥̮̖͍̣̲͕̙͚̹̦͓̪͔̝͔̘̪̭̝̘͉̦̪̬̬̱̙̜̪̦̩͔̗͍̝̞̬̱͕͓̣̭̹̹͈̦͓͍̙͍̮͔̖̟̳͙̹͔̼̥͇̦̝̲͓̗̖̭̲̦̩̦̣͕̭̠̗͖̞̲̝̙̠͚̼͎͈̠͍̣̺͇̮̪̦̣͍̠̱̝̞͕̪͔͍̳͇͙̦̣̻̬͓̝͇̤̙̩̹͙̘̬̦̮̻͍̦͕̘͔̮̙͕̮͉̦͙͙̝͙̪̪̱͈̦̜̹̬͈͈͖̺̰̳͙̺̦̖͚͔͗̐͌͛̊ͨ̓̏ͥ̿͛̿͡
"""


def test_occurrences():
    assert occurrences(STRING, PATTERN) == 3
    
def test_first_occurrence():
    assert first_occurrence(STRING) == "Hi"

def test_last_occurrence():
    assert last_occurrence(STRING) == "man"

def test_random_occurrence():
    # Test case 1: Check if the result is one of the words in the string
    result = random_occurrence(STRING)
    assert result in STRING.split(" ")

    # Test case 2: Check if the result is a string type
    assert isinstance(result, str)

def test_is_zalgo():
    assert is_zalgo(STRING) == False 
    assert is_zalgo(ZALGO) == True