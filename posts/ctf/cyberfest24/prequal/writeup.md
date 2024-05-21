### Troll
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/813b37d2-c052-41b1-9409-a985da23ed3d)

This challenge was pretty much created due to a rant about why there were no very trivial challs 😄

-- We asked for it...

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/556e5bef-06ac-475e-9f40-82560a35c2d3)

-- He delivered

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d9d5495d-0005-430c-ba29-660c3f0b4e75)

Now let's get to it

Going to the attached url doesn't show anything
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/06a284fe-3cf2-4578-b303-18ded56c4fdc)

Viewing page source reveals nothing also
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/656d4fa2-8066-4589-8928-8cf54c83afaf)

On checking `/robots.txt` reveals this path
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2553da28-c96a-4164-8013-64a04d587682)

Trying to access it downloads an attachment
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2e4d146f-b9cb-46b5-b7a4-42446281d5cf)

The file downloaded was a rust compiled executable
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fa517406-19be-4799-8b70-a95fd382d1cd)

I ran it and got this message
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ed67c45d-d9cb-41bd-bac8-1832c5429af3)

At this point when solving it I actually had to `CTRL+C` because during the prequal there was a rev chall which would logout the current session so I thought it was the same but luckily it wasn't

Searching for low hanging fruits revealed the flag

```
Flag: aCtF{robotTxt_and_strings_as_requested}
```
