def is_palindrome(word): 
    if word == "": 
        return True
    elif word[0] != word[-1]:
        return False
    else: 
        return is_palindrome(word[1:-1])
    

print(is_palindrome("racecar"))