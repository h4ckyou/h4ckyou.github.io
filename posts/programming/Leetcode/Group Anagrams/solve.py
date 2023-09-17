def groupAnagrams(strs):
    anagram_dict = {}
    
    for word in strs:
        sorted_word = "".join(sorted(word))
        
        if sorted_word in anagram_dict:
            anagram_dict[sorted_word].append(word)
        else:
            anagram_dict[sorted_word] = [word]
    
    result = list(anagram_dict.values())
    
    return result

strs = ["eat","tea","tan","ate","nat","bat"]
anagram_groups = groupAnagrams(strs)
print(anagram_groups)
