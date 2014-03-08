redditcoin
==========
a cryptocurrency which supports reddit-style user generated content. Each post and comment is a ponzi scheme. You can make profit by upvoting unpopular content which later becomes popular.

### Types of transactions
*mint coins (only one allowed per block, the miner gives it to themselves.)
*send coins to another user.
*create post
*upvote post
*downvote post
*connect a unique user name to your public key
*add reputation to a user

### about posts
*a string of characters which is limited by a maximum length. This maximum length is voted on by shareholders.
*a post can optionally be a comment on another post.
*Each post has an amount of value
*there can only exist a limited number of posts at a time. If this limit is surpassed, then the least valuable post disappears. 
*If a post dies, then all of the comments on that post die as well.

### about shareholder raffle
There are a lot of numbers in the system which the miners use to verify transactions. The maximum blocksize for example. Each coin is also shares in the redditcoin system. When you create a user name, you also create a dictionary of the constants that you want to vote on, and the ideal value that you want each of those constants to be.
Every block, a single shareholder is selected at random. We look at what his ideal constants are, and adjust the constants by a certain portion in his preference. 
If you own 1/4th of all the redditcoin, then you have 1/4th chance of being selected to vote in the next block.
* max length of a post.
* max length of a block.
* min amount of coins that can be sent to another user.
* min amount of coins to upvote with.
* min amount of coins to downvote with.
* max number of posts before we start deleting the least valuable posts.
* cost to buy a user name or to switch user names.
* cost paid out every block in order to continue owning a user name.
* minimum amount of reputation to purchase.
* The miner fee associated to each type of transaction.

### numbers that have to be between 0 and 1
I need a formula to fairly have shareholders determine these numbers which have bounds of 0 and 1.
* portion change to numbers that shareholder raffle causes every block. 
* P1=portion of upvote that the post increases in value by
* P2=portion of upvote that gets paid back to owners of a post
* each block, all the posts lose the same percentage of value. (This is done so that old posts everntually die of age.) 

### upvoting
When upvoting, you spend X coins. X has to be greater than a minimum limit. The post you are upvoting increases in value by a percentage of X. Ownership of the post is re-calculated such that you own X/(all money spend on it) of it. A percentage of X coins are given out to the owners of the post. Each owner recieves coins according to what portion ownership they have.
P1=portion of upvote that the coin increases in value by
P2=portion of upvote that gets paid back to owners of a post
Example: There is a post worth 100 coins. You upvote it with 200 coins. (1-P2)*200 of your 200 get deleted, P2*200*(200/(200+100)) of your 200 go to yourself, and P2*200*(100/(200+100)) of the 200 go to the other owners.

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