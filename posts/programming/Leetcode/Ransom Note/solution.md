<h3> Ransom Note </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8af505b1-43a6-46fc-933b-aa03b89f57ba)

Given two strings `ransomNote` and `magazine`, return `True` if `ransomNote` can be constructed by using the letters from `magazine` and `False` otherwise.

Note: Each letter in magazine can only be used once in ransomNote.

We will be given two strings and our goal is to return True is the first string can be formed from the second one

Here's my solution approach:

First I'll gather each character occurrence of the two string and store in a hashtable (one for each)

The reason for doing that is because I'll need it in the future also we need to make sure that each character in string a has the same occurrence in string b

So assuming we're trying a brute force approach that particular test case will make the program return the wrong answer let's say:

```
ransomNote = "aa"
magazine = "ab"
```

Because we'll be likely checking `if ransomNote[i] in magazine` and that would presumely return True that `ransomNote` can be formed by using letters from `magazine`

That's because the occurrence of `a` in `ransomNote` is twice while in `magazine` it's just once and since we're using the `in` command in python it would return that yes there are two a's 

So inorder to not meet that I'm saving each occurrence of letters of both strings in a hashtable

Then I will iterate through the key and value pairs of the `ransomNote` hashtable and check if the key exists in the `magazine` hashtable `AND` the value of `magazine[key]` is equal to or greater than the current iterate `value`

If that returns True I'll append it to a list `tt` else I'll append False to the `tt` list

At the end of the iteration I'll check if `False` exists in `tt` and if it does then I return False or True

Here's my solve script: [link]()
