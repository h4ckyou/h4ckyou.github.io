<h3> Generate a String With Characters That Have Odd Counts </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d06ccff-d859-463f-aeaa-7b27f90c4185)

We are given an integer `n` our goal is to return a string with `n` characters such that each character in the string occurs an `odd number` of times

Let's take an example:

```
n = 4
```

We need to make sure that each character formed with `n` number of times is an odd number

What that means is let's say I generate a string of `n` times:

```
string = aaaa
```

We can see that `a` appears 4 times which is even 

To make it odd we can remove one `a` and replace with `b`

```
string = aaab
```

So with that we meet the condition!

What of if `n` is already odd?

Well we can just return `n * string`

```
n = 3
```

Our return value 

```
string = aaa
```

Now one way we can easily approach solving this is to generate an equation that the return value should follow

And if you notice when `n` is even the value been returned follows this:

```
a + (b * (n - 1))
```

With that we can then solve this task!

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Generate%20a%20String%20With%20Characters%20That%20Have%20Odd%20Counts/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e7abffd6-5300-477d-89b1-fc1518dc2b00)


