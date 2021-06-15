# Bitcoin

## Launch
How to run the project?

**Dependencies**

Before plugging into the project make sure you have the following requirements updated: (run the command aside if not)

apt-get -y update : execute if running any of the below.
1) Python3: apt-get -y install python3 
2) Python3 pip: apt-get -y install python3-pip 
3) csv: pip3 install python-csv
4) heapq: pip3 install heapq

**Clone**

Clone this repo to your local machine using
```code
git clone https://github.com/SmritiAgrawal04/Bitcoin.git
```

**Activate/Plug**

In the cloned repo /Bitcoin/ directory open a new terminal and run the command-
```code
python3 Bitcoin.py
```

## Algorithms Used
* Solution using Max Heap:
	Under this solution, a max heap is maintained sorted on descending order based on the fee. Every time a transaction is pulled off the heap, a check is run to verify if there are no parents of the transaction or all its parents are already visited- if that is the case, that transaction is considered in the block. However, if any of the parent transaction is unvisited, this current transaction is suspended until an eligible transaction is picked. Also, these suspended transactions are pushed into heap again to check if they are eligibe transactions by now.
	
	The drawback of the solution is that it does not consider the comparision between two transactions in terms of weight i.e., even if two transactions that have a weight sum less than the considered transaction and better profit, it will greedily consider the one optimal at that point in time.
	
* Solution using Dynamic Approach:
	This solution is similar to 0/1 Knapsack problem of Dynamic Programming. 
	
	The drawback of the solution being that it does not consider the parents visit/unvisit before the currnet transaction.
