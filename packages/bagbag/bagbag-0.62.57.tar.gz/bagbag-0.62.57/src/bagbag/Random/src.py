
from typing import Any


#print("load random")

def Int(min:int, max:int) -> int:
    import random 
    return random.randint(min, max)

def Choice(obj:list|str) -> Any:
    import random 
    return random.choice(obj)

def String(length:int=8, charset:str="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") -> str:
    import random 
    res = []
    while len(res) < length:
        res.append(random.choice(charset))
    
    return "".join(res)

def Shuffle(li:list) -> list:
    import random 
    import copy
    l = copy.copy(li)
    random.shuffle(l)
    return l

if __name__ == "__main__":
    print(Choice("doijwoefwe"))
    print(String(5))
    print(Shuffle([1,2,3,4,5]))