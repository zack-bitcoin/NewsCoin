redditcoin
==========
a cryptocurrency which supports reddit-style user generated content. Each post and comment is a ponzi scheme. When you upvote content, you become a partial owner of it. Every time content its upvoted, all the owners make money.

### Types of transactions
* mint coins (only one allowed per block, the miner gives it to themselves.)
* send coins to another user.
* create post
* upvote post
* downvote post
* connect a unique user name to your public key
* add reputation to a user

### about posts
* a string of characters which is limited by a maximum length. 
* a post can optionally be a comment on another post. (comments can have comments recursively) 
* Each post has an amount of value
* there can only exist a limited number of posts at a time. If this limit is surpassed, then the least valuable post disappears. 
* If a post dies, then all of the comments on that post die as well.

### about shareholder raffle
There are a lot of numbers in the system which the miners use to verify transactions. The maximum blocksize for example. Each coin is also shares in the redditcoin system. When you create a user name, you also create a dictionary of the numbers that you want to raffle for, and the ideal value that you want each of those numbers to be. Every block, a single shareholder is selected at random. We look at what his ideal constants are, and adjust the constants by a certain portion in his preference. If you own 1/4th of all the redditcoin, then you have 1/4th chance of winning the raffle in the next block.

### unbounded numbers that shareholders vote on. (for practical purposes, these numbers are rounded up to the nearest integer.)
* max length of a post.
* max length of a block.
* min amount of coins that can be sent to another user.
* min amount of coins to upvote with.
* min amount of coins to downvote with.
* max number of posts before we start deleting the least valuable posts.
* cost to buy a user name or to switch user names.
* cost paid out every block in order to continue owning a user name.
* minimum amount of reputation to purchase.
* The miner fee associated to each type of transaction. (7 numbers that are each voted on independently)

### numbers shareholders vote on that are bounded between 0 and 1
Let the slipperiness of bounded numbers be a number = S. Say that the bounded number which the shareholder wants to change = x, and that the shareholder who won this block wants the number to be bigger, then the number x will become x+S*min(x,(1-x))/350. If instead the shareholder wanted the number to be smaller, then the number would become x-S*min(x,(1-x))/350. (See python example code #1 at the bottom) These constants are selected so that the number will always be bounded between 0 and 1. At maximum slipperiness, these bounded numbers can get closer to a bound by about 1/3rd in a single day, if everyone was to vote in the same direction.
* S=The slipperiness of the numbers that are bounded between 0 and 1. (If S is closer to 0, then the numbers are less slippery.) 
* S2=slipperiness of the unbounded numbers. If N is the unbounded number which gets bigger, it becomes N*(1+(S2/100)), if it gets smaller, it becomes N*(1-(S2/100)).
* P1=portion of upvote that the post increases in value by
* P2=portion of upvote that gets paid back to owners of a post
* P3=portion of comments value that the parent-post increases by. Valuable comments make posts more valuable in this way.
* P4. Say the value of a post is V. Every block, the new value of the post is V*(1-P4/10). This is done so that old posts everntually die of age. The closer P4 is to 1, the faster posts will age.

### value of a post
P3 = portion of a comments value that the parent recieved by being it's parent.
Value = value the post started out with + value it got from upvotes - value it lost from downvotes - value it lost from age + P3*(sum of it's comments values)

### upvoting
When upvoting, you spend X coins. X has to be greater than a minimum limit. The post you are upvoting increases in value by a percentage of X. Ownership of the post is re-calculated such that you own X/(all money spend on it) of it. A percentage of X coins are given out to the owners of the post. Each owner recieves coins according to what portion ownership they have.
Upvoting a comment causes it's parent post to increase in value as well.
```
P1=portion of upvote that the coin increases in value by
P2=portion of upvote that gets paid back to owners of a post
Example: There is a post worth 100 coins. You upvote it with 200 coins. (1-P2)*200 of your 200 get deleted, P2*200*(200/(200+100)) of your 200 go to yourself, and P2*200*(100/(200+100)) of the 200 go to the other owners.
````

### downvoting
When downvoting, you spend X coins where X is above a limit. The post you downvoted loses X value.

### creating a post
When creating a post, you spend X coins.
P1=portion of upvote that the coin increases in value by.
P2=portion of upvote that gets paid back to owners of a post.
The value of the post is like you kept upvoting with all the money you get back from the previous upvote.
The value of the post is: X*P1(1+P2+P2^2+P2^3+P2^4...)=X*P1/(1-P2)
Where the carrot symbol '^' means exponentiation.

### user names
* getting/changing users name costs a certain amount of coins. 
* each name can only be associated with one public key at a time.
* When getting/changing user name is when you optionally give your vote for the shareholder raffle. This vote is a dictionary containing the names of some or all of the constants in the system, and what you want those constants to be.
* Every block, the user name loses a small amount of value. If the user name runs out of money, then it gets completely deleted, and you permanently lose any reputation associated to that name.

### add reputation to a public key
* You give the user name associated with the public key.
* It costs X coins, where X is above some minimum.
* The user name increase in reputation by X.
* If that user changes names later, he takes the reputation with him.

### Python example 1 
```
At middle slipperiness, we can change by about 1/5th per day.
>>> def next(x):
...     return x+(1-x)/700
... 
>>> a=0.9
>>> for i in range(144):
...     a=next(a)
... 
>>> a
0.9186054089806828
>>> a=0.99
>>> for i in range(144):
...     a=next(a)
... 
>>> a
0.9918605408980671
>>> 
```