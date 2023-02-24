class NodeIR:

    def __init__(self, nodeID: int, nodeName: str, inputIDs, outputIDs, scriptRep: str):
        self.nodeID = nodeID
        self.nodeName = nodeName
        self.inputIDs = inputIDs
        self.outputIDs = outputIDs
        self.scriptRep = scriptRep
