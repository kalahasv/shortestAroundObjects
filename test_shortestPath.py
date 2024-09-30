import pytest
import 014305668 as m


def test_program():
    adj,srt,end,n,G,points = m.digestInput("input.txt","coords.txt",False)
    shortest,finalWeights = m.findShortestPath(adj,srt,end,n,G,points,False)
    m.writeOutFile(shortest,finalWeights)
    #for row in adj:
    #    print(row)
    #print(shortest)
    #print(finalWeights)
    
    

