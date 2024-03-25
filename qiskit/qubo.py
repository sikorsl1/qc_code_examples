from dataclasses import dataclass

@dataclass
class Item:
    name: str
    value: int
    weight: int

def main():
    knapsack = [Item('ball', 8, 3), Item('computer', 47, 11), Item('camera', 10, 14),
                Item('books', 5, 19), Item('guitar', 16, 5)]
    max_weight = 26

if __name__ == "__main__":
    main()