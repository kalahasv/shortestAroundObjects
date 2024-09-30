
'''

########### VISUALIZATION CODE ##################
import skvideo.io
import numpy as np
import cv2
import networkx as nx
import matplotlib.pyplot as plt
#################################################
'''

def digestInput(inputFileName,coordFileName,visualize = False): #formats input into adjacency List

    inputCFile = open(coordFileName)
    points = {}
    nodeNum = 1
    G = None
    for line in inputCFile:
        l = line.strip('\n').split(' ')
        point = (float(l[0]),float(l[1]))
        points[nodeNum] = point
        nodeNum +=1
    
    '''

    ########### VISUALIZATION CODE ##################
    if visualize:
        G = nx.DiGraph()
        G.add_nodes_from(points.keys())
    #################################################
    '''  

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
         
    for line in inputFile: #line = [[]]  #[[i,j,w]] placeholder
        line = line.strip("\n").split()
       
        src = int(line[0])
        dst = int(line[1])
        ''' 
        ########### VISUALIZATION CODE ##################
        if visualize:
            G.add_edge(src,dst)
        #################################################
        '''

        weight = float(line[2])

        adjMatrix[src-1][dst-1] = weight #this is where it gets adjusted to a 0 index
    inputFile.close()

    return adjMatrix,startNode,endNode,numNodes,G,points
      
def findShortestPath(adjMatrix,startNode,endNode,numNodes,G = None,points = None,visualize = False):

        
        ''' 
        ########### VISUALIZATION CODE ##################
        
        if visualize:
            fig, ax = plt.subplots()
            images = []
            limits=plt.axis('on') # turns on axis

            cMap = ['blue' for node in G]
            cMap[startNode] = 'red'
            cMap[endNode] = 'red'

            nx.draw(G,pos=points, with_labels=True,node_color = cMap,ax=ax,arrows=False)
            plt.savefig("Graph0.png", format="PNG")
            images.append(cv2.imread("Graph" + str(0) + ".png"))
        
        ###############################################################
        '''
        
        shortest = [] 
        unvisited = set([i for i in range(numNodes)]) #set of nodes to visit starts w/ everything
       

        cParents = [[]]*numNodes #starts off unknown
        cDist = [float('inf')]*numNodes #keeps the current distance to reach it, 0-indexed

        cDist[startNode] = 0 #set the startNode to a weight of 0 so there's a starting point

        iteration = 1
       

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
                ''' 
                ########### VISUALIZATION CODE ##################
                if visualize:
                    cMap[endNode] = 'green'

                    nx.draw(G,pos=points, with_labels=True,node_color = cMap,ax=ax,arrows=False)
                    plt.savefig("Graph" + str(iteration) + ".png", format="PNG")

                    images.append(cv2.imread("Graph" + str(iteration) + ".png"))
                ########### ################## ##################
                '''
                break
            
            unvisited.remove(pickedNode)

            #find its neighbors
            neighbors = adjMatrix[pickedNode]

            ''' 
            ########### VISUALIZATION CODE ##################
            if visualize:
                for c in range(len(cMap)):
                    if cMap[c] == 'yellow':
                        cMap[c] = 'grey'
            ########### VISUALIZATION CODE ##################
            '''

            for i in range(len(neighbors)):
                

                if neighbors[i] != float('inf') and i in unvisited:
                    ''' 
                    ########### VISUALIZATION CODE ##################
                    if visualize:
                        cMap[i] = 'yellow'
                    ##################################################
                    '''

                    temp = cDist[pickedNode] + neighbors[i]

                    if temp < cDist[i]:
                        cDist[i] = temp
                        cParents[i] = [pickedNode]
                    elif temp == cDist[i]:
                        cDist[i] = temp
                        cParents[i].append(pickedNode)
            
            ''' 
            ########### VISUALIZATION CODE ##################
            if visualize:
                nx.draw(G,pos=points, with_labels=True,node_color = cMap,ax=ax,arrows=False)
                plt.savefig("Graph" + str(iteration) + ".png", format="PNG")

                images.append(cv2.imread("Graph" + str(iteration) + ".png"))

            
                iteration +=1
            ###############################################
            '''

        #go backwards and find the shortest path
        current = endNode
        finalWeights = []
        finalEdges = []
        while current != None:
           # print("Current",current)
            temp = current
            shortest.append(current+1)
            finalWeights.append(cDist[current])
        
            if cParents[current]:
                current = min(cParents[current])
                finalEdges.append((int(current)+1,int(temp)+1))  
            else:
                current = None  
       
        
               
        shortest = shortest[::-1]
   
        finalWeights  = finalWeights[::-1]
        finalEdges = finalEdges[::-1]
        
        ''' 
        ########### VISUALIZATION CODE ##################
        if visualize:
            edge_colors = []
            alpha_list = []
            for c in range(len(cMap)):
                if cMap[c] == 'yellow':
                    cMap[c] = 'grey'
            for node in shortest:
                cMap[node-1] = 'red'

            a = 0.2
            found_edges = []
            #print("EDGES",G.edges())
            for e in G.edges():
                u = e[0]
                v = e[1]
                #print((u,v))
                #print((u,v) in finalEdges)


                if (u,v) in finalEdges:
                    found_edges.append((u,v))
                    G[u][v]['color'] = 'red'
                    a = 1
                else:
                    G[u][v]['color'] = 'white'
                    a = 0.2

                edge_colors.append(G[u][v]['color'])
                alpha_list.append(a)

           # print('Final Edges:',finalEdges)
           # print("Found Edges:",found_edges)

            nx.draw_networkx_nodes(G,pos=points,node_color = cMap,ax=ax)
            nx.draw_networkx_edges(G, pos=points, alpha=alpha_list, width=6,edge_color=edge_colors,arrows=False)
            
            for i in range(iteration+1,iteration+10):
                plt.savefig("Graph" + str(i) + ".png", format="PNG")
                images.append(cv2.imread("Graph" + str(i) + ".png"))
                

            #print('IMAGES LENGTH:',len(images))
            
            # reference -> https://stackoverflow.com/questions/67666587/how-can-i-create-a-slideshow-of-some-selected-frames-from-a-video-in-python

            height,width,etc =images[0].shape
            out_video =  np.empty([len(images), height, width, 3], dtype = np.uint8)
            out_video =  out_video.astype(np.uint8)
            for i in range(0,len(images)):
                img = cv2.imread('Graph' + str(i) + '.png')
                out_video[i] = img

            skvideo.io.vwrite("014305668.mp4", out_video)
        ##################################################
        '''

        return shortest,finalWeights

def writeOutFile(shortest,finalWeights):
    nodes = ' '.join([str(x) for x in shortest])
    weights = ' '.join([str(x) for x in finalWeights])
    with open('014305668.txt', 'w') as f:
        print(nodes, file=f)
        print(weights,file = f)





   
adj,srt,end,n,G,points = digestInput("input.txt","coords.txt",False)
shortest,finalWeights = findShortestPath(adj,srt,end,n,G,points,False)
writeOutFile(shortest,finalWeights)
 
