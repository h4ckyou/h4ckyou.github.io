<h3> Candy </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c95a2cbc-e9bd-4e69-b9d8-f3ecfc0245f7)

There are `n` children standing in a line. Each child is assigned a rating value given in the integer array `ratings`.

You are giving candies to these children subjected to the following requirements:
- Each child must have at least one candy.
- Children with a higher rating get more candies than their neighbors.

Return the minimum number of candies you need to have to distribute the candies to the children.

From the problem description, we want to find the minimum number of candies needed to satisfy those requirements while also ensuring that children with higher ratings get more candies than their neighbors.

Let's take the first test case example:

Suppose you have the following ratings for children:

```
ratings = [1,0,2]
```

This means that:

```
Child 0 has a rating of 1.
Child 1 has a rating of 0.
Child 2 has a rating of 2
```

To satisfy the conditions:
- Each child must have at least one candy, so we start by giving each child one candy: `[1, 1, 1]`.
- Children with a higher rating should get more candies than their neighbors. In this case, `Child 2` has a higher rating than its neighbors `(1 and 0)`, so we give it more candies than its neighbors. The updated distribution becomes `[1, 1, 2]`.

Now, we've met both conditions. `Child 0` has one candy, `Child 1` has one candy, and `Child 2` has two candies. The minimum number of candies needed to satisfy these conditions is `1 + 1 + 2 = 4` candies.

The goal of the problem is to find the minimum total number of candies needed to satisfy these conditions for any given set of ratings.

In my solve script I basically iterate twice and one the first iteration I check for the children with higher ratings so as to give them more candies than their left neighbors, and the second iterate I check for the children with higher ratings so as to give them more candies than their right neighbors

From there the minimum total number of candies needed is then calculated based on this distribution.

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Candy/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/214f686a-8aee-46de-979d-756bc309528f)

