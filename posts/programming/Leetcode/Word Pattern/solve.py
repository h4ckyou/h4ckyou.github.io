def wordPattern(pattern, s):
    words = s.split()
    
    if len(pattern) != len(words):
        return False

    pattern_to_word = {} 
    word_to_pattern = {}  

    for char, word in zip(pattern, words):
        if char not in pattern_to_word and word not in word_to_pattern:
            pattern_to_word[char] = word
            word_to_pattern[word] = char
        elif pattern_to_word.get(char) != word or word_to_pattern.get(word) != char:
            return False

    return True

pattern = "abba"
s = "dog cat cat dog"
r = wordPattern(pattern, s)

print(r) 
