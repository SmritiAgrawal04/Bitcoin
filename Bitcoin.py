#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
from heapq import heapify, heappush, heappop


# In[2]:


class MempoolTransaction():
    """Save each transaction as an object"""
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight= int(weight)
        if len(parents)==0:
            self.parents =[]
        else:
            self.parents= parents.split('\n')[0].split(';')


# In[3]:


def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    data= open('mempool.csv', 'r').readlines()[1:]
    return([MempoolTransaction(*line.strip().split(',')) for line in data])


def write_blockTransactions(filename, blockTransactions):
    """Write the eligible bock transactions to an output file"""
    f = open(filename, "a")
    for transaction in blockTransactions:
        f.writelines(transaction)
        f.writelines('\n')
    f.close()


# In[4]:


class HeapSolution():
    
    def __init__(self):
        """Initialize the variables and read all transactions"""
        self.transactions= parse_mempool_csv()    
        self.heap= self.createHeap()
        self.blockWeight =0
        self.visited= set()
        self.blockTransactions= []
        self.suspendedTransactions= []      

    def createHeap(self,):
        """Create a max heap with all transactions sorted in descending order fee wise"""
        heap = [] 
        heapify(heap) 

        for entry in self.transactions:
            heappush(heap, (-1*entry.fee, entry.txid, entry.weight, entry.parents))

        return heap
    
    def pull_suspendedTransactions(self,):
        """Pull the suspended transctions back and push them into heap"""
        for entry in self.suspendedTransactions:
            heappush(self.heap, (entry.fee, entry.txid, entry.weight, entry.parents))    
    
    def get_appropriateTransactions(self, ):
        """Retreive the eligible transactions"""
        while self.heap and self.blockWeight <=400000:
            entry= heappop(self.heap)
            fee, txid, weight, parents= -1*entry[0], entry[1], entry[2], entry[3]
            if len(parents) ==0:
#                 print ("No Parents")
                self.blockTransactions.append(txid)
                self.visited.add(txid)
                self.blockWeight +=weight
                self.pull_suspendedTransactions()

            else:
                isSuspended= False
                for parent in parents:
                    if parent not in self.visited:
#                         print ("Parent unvisited")
                        self.suspendedTransactions.append(entry)
                        isSuspended= True
                        continue
                if not isSuspended:
#                     print ("All parent visited")
                    self.blockTransactions.append(txid)
                    self.visited.add(txid)
                    self.blockWeight +=weight
                    self.pull_suspendedTransactions()
        
        write_blockTransactions('block_MaxHeap.txt', self.blockTransactions)


# In[5]:


class DynamicSolution():
    def __init__(self):
        """Initialize the variables and read all transactions"""
        self.transactions= parse_mempool_csv()    
        self.capacity= 40000
        self.n= len(self.transactions)
        self.blockTransactions= []
        
    def get_appropriateTransactions(self, ):     
        """Retreive the eligible transactions"""
        K = [[0 for w in range(self.capacity + 1)]
            for i in range(self.n + 1)]
             
        for i in range(self.n + 1):
            for w in range(self.capacity + 1):
                if i == 0 or w == 0:
                    K[i][w] = 0
                elif self.transactions[i - 1].weight <= w:
                    K[i][w] = max(self.transactions[i - 1].fee + K[i - 1][w - self.transactions[i - 1].weight], K[i - 1][w])
                else:
                    K[i][w] = K[i - 1][w]
        
        
        profit = K[self.n][self.capacity]
        res =profit

        w = self.capacity
        for i in range(self.n, 0, -1):
            if res <= 0:
                break
            if res == K[i - 1][w]:
                continue
            else:
                self.blockTransactions.append(self.transactions[i-1].txid)
                res = res - self.transactions[i - 1].fee
                w = w - self.transactions[i - 1].weight
                
        write_blockTransactions('block_Dynamic.txt', self.blockTransactions)
        
        


# In[6]:


if __name__ == "__main__":
    hsObj= HeapSolution()
    hsObj.get_appropriateTransactions()
    dsObj= DynamicSolution()
    dsObj.get_appropriateTransactions()


# In[ ]:




