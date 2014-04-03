NEWScoin
==========


======INSTALL======
You need python 2.X
http://www.python.org/download/

=======INFO ON NEWSnet=======
NewsCoin is a cryptocurrency (NEWS) and a decentralized application which supports reddit-style aggregation of user generated content. Each post and comment has its own balance. When you upvote content, you become a partial owner of it through sending NEWS to it. Every time content is upvoted you buy a stake of the post and all the early stakeholders make profit according to their stake and internal order. The currency also supports minimal marketplace functionality, and is intended to be a distributed replacement for silkroad. 
There are 2 types of employees: miners and jury-members
NewsCoin is a type of slasher currency: http://blog.ethereum.org/2014/01/15/slasher-a-punitive-proof-of-stake-algorithm/


### Types of transactions
1)spend
*include a list of pubkeys you are giving the money to, and the number of pubkeys who have to agree, in order to spend the money. (the "n" and "m" of a NxM bitcoin address)
2)mint
*only 1 mint transaction per block
*this gives the miner a reward.
3) create named account
*Now people can spend to "ganjaQueen" instead of to nonsense pubkeys like: "1847f892h4f8928294f"
*Give a menu of what goods you are selling.
*Explain the process to purchase from you. Maybe give an XMPP address for OTR chat.
*You can update your info by making a new transaction of this type.
*if a named account runs out of money, then all the reputation associated with that account is deleted.
4) buy reputation for a named account
*proof of burn
5)jury signature
*jury members sign the chain which they think is the valid chain.
*jury members have an incentive to only sign 1 chain.
*this gives the jury member a reward.
*There are about 20 constants built into the currency, examples: transaction fees, difficulty. The jury members vote to slightly adjust each of these constants upward or downward.
6)catch a cheating jury member
*if a jury member signs 2 forks, then anyone else can take those 2 signatures and make this type of transaction.
*the jury member loses their reward
*the person who created this transaction receives a reward
7)create post
*When creating a top-level post, you spend X NEWS. The value of the post is X. You own X of the post, which is all of the post.
*If your post is a comment on a different post, then it acts like an upvote and a post at the same time.
8)upvote post
*spend X NEWS
*a portion of this upvote pays the owners of the post you are upvoting, call this portion P. It includes you as one of the owners of the post, so there is an incentive to do all your investing in 1 go, instead of investing in the same post more than once.
*the post increases in value by X*(1-P)*(1-P3)
*you own the amount of the post that you increased it's value by.
*The parent posts increase in value by X*(1-P)**2*P3 according to the same rules.
*you own the portion of the parent post that you increased it's value by.
*The parent post's owners get paid P*X*(1-P)*p3
The goal here is for value to never be created or destroyed. (The total value of all the posts) + (the amount that owners get paid) = (amount that was invested).
*for an upvote to be valid, you need to own non-negative amount of coins at the end.
9)downvote post
*When downvoting, you spend X NEWS. 
*The post you downvoted loses X value.

### about posts
* a string of characters which is limited by a maximum length. 
* a post can optionally be a comment on another post. (comments can have comments recursively) 
* Each post has an amount of value
* Each post loses a percentage of its value every block.
* there can only exist a limited number of posts at a time. If this limit is surpassed, then the least valuable post disappears. 
* If a post dies, then all of the comments on that post die as well.
* When posts increase in value, they pay out to the shareholders.

### positive numbers that shareholders vote on which change exponentially. (many of these numbers are rounded up to the nearest integer when they are used.)

Let f be one of these types of numbers. Lets assume that the jury member votes for f to get bigger, the new f is calculated this way:
f=f*(1+unbounded_slipperiness) where unbounded_slipperiness is a constant bounded between 0 and 1.

* max length of a post.
* max length of a block.
* max number of posts before we start deleting the least valuable posts.
* fee every block in order to continue owning a user name or address.
* The miner fee associated to each type of transaction. (7 numbers that are each voted on independently)
*difficulty to mine next block
*The bounded_slipperiness which is used to limit by how much the bounded numbers can be changed by each jury signator

### numbers shareholders vote on that are bounded between 0 and 1

Let f be one of the numbers which must stay between 0 and 1.
Then x is the number we vote on. x's bounds are [-infinity, infinity]. Every jury signator has the ability to change x up or down by bounded_slipperiness. f is computed from x by this formula: f(x)=(atan(x)/pi)+0.5

* P1=portion of upvote that gets paid back to owners of a post
* P3=portion of comments value that the parent-post increases by. Valuable comments make posts more valuable in this way.
* P4. Every block, all the posts become less valuable. the value of the post on block n+1 is computed this way: V(n+1)=V(n)*P4
* unbounded_slipperiness which is the constant that determines how quickly we can change the unbounded numbers


### value of a post
Value = value the post started out with + value it got from upvotes - value it lost from downvotes - value it lost from age + P3*(sum of it's comment's values)

===databases=== 6
blockchain
potential transactions suggested to us by peers
potential blocks suggested to us by peers
valid transactions to include in next block
current ledger
backups of the ledger, in case we get on a fork and need to rebuild from an earlier ledger.

===handshakes between nodes to maintain consensus=== 5
getinfo
  *blocklength
  *hash of most recent block
  *number of jury signatures in chain
pushtx
pushblock
request blocks in range
request transactions to be included in next block

===threads===
1) trying to mine next block
2) listen for peers
3) gui
