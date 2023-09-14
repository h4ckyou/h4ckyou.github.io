<h3> Binary Tree Inorder Traversal </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6efa44dd-4e85-4c8a-a914-c537f5ce77a2)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e6d31e7a-29f8-4bca-b79e-58b66dc501b5)

We are going to be given a binary tree and our goal is to return the inorder traversal of its nodes' values

First let's know what `Traversing` means:

Traversing refers to the process of visiting each node of a tree exactly once. Visiting a node generally refers to adding the node's key to a list. There are three ways to traverse a binary tree and return the list of visited keys

In this case I'll deal with the `Inorder Traversal` method:

- Traverse the left subtree recursively inorder
- Traverse the current node
- Traverse the right subtree recursively inorder

That does not sound too good so let's take a sample

Consider this `binary tree` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/840f2369-e11a-4fb1-8af9-93b55189566c)

The key node is `3` which has two children `2 and 4` and the left and right subarray has other children

Let's take an example on what Inorder Traversal means:

First we'll start from the left subarray
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6d5ca74c-4848-4877-b47a-d651d2364220)

Now we check if the left node has another left key value, in this case it does i.e the node `2` has another left node `1`

We check again but in this case the node `1` does not have another node connected to it so we add that to our list 

Now we move up the from the left subtree to the current node


