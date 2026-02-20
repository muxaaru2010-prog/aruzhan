number = 87
guess = int(input("Угадай число  от 1 до 100: "))

while guess != number:
    print("Больше число!")
    guess = int(input("Угадай число  от 1 до 100: ")) 
print("Ты правильно угадал!")   