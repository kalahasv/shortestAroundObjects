
'''
what does my input need to be formatted into?
-need to register the start point
-need to register the end point


leetcode question is given 1-n nodes, and a list of directed edges (u,v,w)
-creates adjacency map with weight attached
-result array
-queue
-store graph in an adjacency
list using a binary heap or priority queue. according to notes

-need to keep track of each node's current smallest distance, and its previous vertex
-visit its neighbors
-update the distances based on weight from the start vertex
-node goes into visited vertex
-visit the smallest weight

-should i make this a class or a collection of methods? I'm thinking class so I can keep the sets seperate, but really there is only two methods
-make seperate video generation f'ns for ease of use in testing 
    -con: reading a file twice instead of once 
    -could make a f'n that adds edge to the map and just call in in the main function -> might be better
-should produce results in a few seconds
-would it be easier to just 0 index everything? i feel like it would mess up the edges, though
-once it's been picked and is released from the visited set, then it goes to the solution set

'''
from collections import defaultdict



def digestInput(inputFileName): #formats input into adjacency List

    inputFile = open(inputFileName)
    numNodes = int(inputFile.readline())
    startNode = int(inputFile.readline())-1 #change to 0 index
    endNode = int(inputFile.readline()) -1 #change to 0 index
    adjMatrix = []

    for r in range(numNodes):
        row = []
        for c in range(numNodes):
            row.append(float('inf'))
        adjMatrix.append(row)
         
   # print("Adjacency",adjMatrix)

    #print(len(adjMatrix))

    for line in inputFile: #line = [[]]  #[[i,j,w]] placeholder

        #print()
        line = line.strip("\n").split()
       
        src = int(line[0])
        dst = int(line[1])
        weight = float(line[2])
        
        #print(src,dst)

        adjMatrix[src-1][dst-1] = weight #this is where it gets adjusted to a 0 index
        

    inputFile.close()

    return adjMatrix,startNode,endNode,numNodes
      
def findShortestPath(adjMatrix,startNode,endNode,numNodes):
        shortest = [] 
        unvisited = set([i for i in range(numNodes)]) #set of nodes to visit starts w/ everything
        print(unvisited)

        cParents = [[]]*numNodes #starts off unknown
        cDist = [float('inf')]*numNodes #keeps the current distance to reach it, 0-indexed

        cDist[startNode] = 0 #set the startNode to a weight of 0 so there's a starting point

        while unvisited:
            #choose list value with smallest weight that's IN unvisited
            pickedNode = None
            minDist = float('inf')
            for vertex in unvisited:
                if cDist[vertex] < minDist:
                    minDist = cDist[vertex]
                    pickedNode = vertex

                #originally, it would automatically go on the stack, but since there could be multiple 'good' paths, i left it
           
            if pickedNode == endNode: #don't need to keep exploring if you've visited the endNode, since you don't return to it
                break
           
            unvisited.remove(pickedNode)

            #find its neighbors
            neighbors = adjMatrix[pickedNode]

            for i in range(len(neighbors)):
                if neighbors[i] != float('inf') and i in unvisited:
                    temp = cDist[pickedNode] + neighbors[i]

                    if temp < cDist[i]:
                        cDist[i] = temp
                        cParents[i] = [pickedNode]
                    elif temp == cDist[i]:
                        cDist[i] = temp
                        cParents[i].append(pickedNode)

        #go backwards and find the shortest path
        current = endNode
        finalWeight = cDist[endNode]
        print("Parents",cParents)
        while current != None:
            print("Current",current)
            shortest.append(current+1)
        
            #print("Current",current+1)
            if cParents[current]:
                current = min(cParents[current])
            else:
                current = None
            print("Current After adjust",current)

            
        
        shortest = shortest[::-1]

        

        return shortest,finalWeight

                

        




if __name__ == '__main__':
   adj,srt,end,n = digestInput("input.txt")
   #digestInput("input.txt")
   
