import pgmlink
import numpy as np
import matplotlib.pyplot as plt
import colorsys


class HypothesesGraphDiagnostics(object):
    def __init__(self, hg, width=600, height=600, radius=15, withDetProbLabels=True, withActiveLabels=False, fileName='HypothesesGraph.png'):        
        plt.clf()
        plt.axis([0,width,0,height])
        fig=plt.figure(1)
        ax=fig.add_subplot(1,1,1)
        
        self.hg = hg
        
        nodeIt = pgmlink.NodeIt(hg)
        arcIt = pgmlink.ArcIt(hg)
        
        traxelMap = hg.getNodeTraxelMap()
        
        # Get unique timesteps
        tsteps = []
        for traxel in traxelMap.values():
            tsteps.append(traxel.Timestep)
        
        uniqueTsteps = np.unique(tsteps)
        
        columnWidth = width/float(len(uniqueTsteps)+1)
        rowHeight = 3*radius
        
        rowPos = {}
        
        for tstep in uniqueTsteps:
            rowPos[tstep] = radius*4
            
            ax.annotate('t+'+str(tstep),
            xy=(0, 0),  # theta, radius
            xytext=((tstep+1)*columnWidth,radius),    # fraction, fraction
            horizontalalignment='center',
            verticalalignment='center',
            zorder=3
            )              

        # Get colors
        colors = self._get_colors(20)

        # Get active arcs map
        activeNodesMap = None
        if withActiveLabels:
            activeNodesMap = hg.getNodeActiveMap()
        
        # Draw nodes
        nodeCoordsMap = {}
        
        for node in nodeIt:
            tstep = traxelMap[node].Timestep
            traxelId = traxelMap[node].Id
            
            nodeCoordsMap[node] = ( (tstep+1)*columnWidth, rowPos[tstep])
            rowPos[tstep] += rowHeight

            # Set the color of active nodes
            color = 'k'
            if activeNodesMap and activeNodesMap[node]:
                color='r'

            circle=plt.Circle(nodeCoordsMap[node], radius=radius, edgecolor=color, facecolor=colors[traxelId], fill=True, zorder=2)
            ax.add_patch(circle)
            
            if withDetProbLabels:
                nodeId = np.argmax(traxelMap[node].get_feature_array('detProb'))
                   
                ax.annotate(str(nodeId),
                xy=(0, 0),  # theta, radius
                xytext=nodeCoordsMap[node],    # fraction, fraction
                horizontalalignment='center',
                verticalalignment='center',
                zorder=3
                )           
         
        # Get active arcs map
        activeArcsMap = None
        if withActiveLabels:
            activeArcsMap = hg.getArcActiveMap()
        
        # Draw arcs
        arcCoordsMap = {}
                 
        for arc in arcIt:
            sourceNode = hg.source(arc)
            targetNode = hg.target(arc)
            
            sourceCoords = None
            targetCoords = None
            
            for node in nodeCoordsMap.keys():
                if hg.id(node) == hg.id(sourceNode):
                    sourceCoords = nodeCoordsMap[node]

                if hg.id(node) == hg.id(targetNode):
                    targetCoords = nodeCoordsMap[node]                    
            
            # Set the color of active arcs
            color = 'k'
            linestyle = 'solid'
            #linestyle = 'dashed'
            if activeArcsMap and activeArcsMap[arc]:
                color='r'
                #linestyle = 'solid'
            
            if sourceCoords and targetCoords:
                arcCoordsMap[arc] = [ [sourceCoords[0],targetCoords[0]], [sourceCoords[1],targetCoords[1]] ]
                line=plt.Line2D( arcCoordsMap[arc][0], arcCoordsMap[arc][1], color=color, linestyle=linestyle, zorder=1)
                ax.add_line(line)  
            else:
                print "Source {} or target {} not found".format(hg.id(sourceNode), hg.id(targetNode))
            

        plt.axis('off')
        plt.savefig(fileName)


    def _get_colors(self, num_colors):
        colors=[]
        for i in np.arange(0., 360., 360. / num_colors):
            hue = i/360.
            lightness = (50 + np.random.rand() * 10)/100.
            saturation = (90 + np.random.rand() * 10)/100.
            colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
        return colors

    
    