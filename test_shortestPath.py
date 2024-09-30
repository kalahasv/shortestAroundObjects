import pytest
import main as m


def test_program():
    adj,srt,end,n = m.digestInput("shortInput.txt")
    shortest,finalWeight = m.findShortestPath(adj,srt,end,n)
    #for row in adj:
    #    print(row)
    print(shortest,finalWeight)
    

def test_Pytest():
    assert 1 == 1