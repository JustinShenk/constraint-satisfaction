import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)
white = (180, 180, 180)
colorList = [red, blue, green]


class ConstraintModel():

    def __init__(self):
        # Initialize plot.
        self.fig, self.ax = plt.subplots(1, 1)
        self.fig.suptitle('Contraint Satisfaction', fontsize=14)

        # Initialize variables.
        self.unresolved = 0

        # Initialize animation parameters.
        self.colors = np.empty((4,4,3))
        self.domains = np.empty((4, 4), dtype=np.object)
        self.conflicts = np.empty((4, 4), dtype=np.object)
        self.conflicts[:, :] = {'above': False,
                                'below': False, 'right': False, 'left': False}
        self.conflictLabels = self.ax.annotate('', (0, 0))
        self.ims = []
        self.signal = self.ax.annotate('', (0, 0))
        self.drawGrid()
        self.checkConstraints()

        # Animate the algorithm.
        self.ani = self.animate()
        plt.show()

    def drawDomain(self, position):
        # self.domainText = self.ax.annotate(
        #     self.getDomain(position), position, ha='center')
        self.domainText = self.ax.annotate(self.getNeighbors(position),position, ha='center')

    def sendText(self, position, text, direction):
        rowInd, colInd = position
        if direction == 'right':
            self.signal = self.ax.annotate(
                self.domains[position] + '>', (colInd + 0.35, rowInd - 0.25), color='white')
        elif direction == 'down':
            self.signal = self.ax.annotate(
                self.domains[position], (colInd, rowInd + 0.35), color='white', ha='center')
        return self.signal

    def drawGrid(self):
        colors = np.zeros((4, 4, 3), dtype='uint8')
        # Domain text is empty.
        self.domainText = self.ax.annotate('', (0, 0))
        self.domains[:] = '{r,g,b}'
        # Fill squares with colors.
        for rowInd, row in enumerate(colors):
            for colInd, pixel in enumerate(row):
                colors[rowInd, colInd] = random.choice(colorList)
#                 self.domainText = self.ax.text(colInd-0.2,rowInd,self.domains[rowInd,colInd],horizontalalignment='center')
        self.colors = colors

    def checkConstraints(self):
        for rowInd, row in enumerate(self.colors):
            for colInd, pixel in enumerate(row):
                try:
                    if np.array_equal(pixel, self.colors[rowInd + 1, colInd]):
                        self.drawConflict(
                            'below', (rowInd + 1, colInd), rowInd, colInd)
                        self.conflicts[rowInd, colInd]['below'] = True
                    else:
                        self.conflicts[rowInd, colInd]['below'] = False
                except:
                    pass
                try:
                    if np.array_equal(pixel, self.colors[rowInd - 1, colInd]):
                        self.drawConflict(
                            'above', (rowInd - 1, colInd), rowInd, colInd)
                        self.conflicts[rowInd, colInd]['above'] = True
                    else:
                        self.conflicts[rowInd, colInd]['above'] = False
                except:
                    pass
                try:
                    if np.array_equal(pixel, self.colors[rowInd, colInd - 1]):
                        self.drawConflict(
                            'left', (rowInd, colInd - 1), rowInd, colInd)
                        self.conflicts[rowInd, colInd]['left'] = True
                    else:
                        self.conflicts[rowInd, colInd]['left'] = False
                except:
                    pass
                try:
                    if np.array_equal(pixel, self.colors[rowInd, colInd + 1]):
                        self.drawConflict(
                            'right', (rowInd, colInd + 1), rowInd, colInd)
                        self.conflicts[rowInd, colInd]['right'] = True
                    else:
                        self.conflicts[rowInd, colInd]['right'] = False
                except:
                    pass

    def drawConflict(self, direction, neighbor, rowInd, colInd):
        if direction == 'right':
            print("drawconflict", rowInd, colInd, direction)
            self.ax.annotate(
                '==', (colInd + 0.35, rowInd), color='white')
    #     ax.annotate('conflict', xy=neighbor, xytext=(rowInd,colInd),
    #             arrowprops=dict(facecolor='black', shrink=0.05))
    #     elif direction == 'above':
    #         ax.text(colInd,rowInd-0.35,'||\n||',color='white')
    #     elif direction == 'left':
    #         ax.text(colInd-0.35,rowInd,'==',color='white')
        elif direction == 'below':
            self.ax.annotate(
                '||\n||', (colInd, rowInd + 0.60), color='white')
        self.unresolved += 1

    def getDomain(self, position):
        return self.domains[position]

    def drawAllDomains(self):
        for rowInd, row in enumerate(self.colors):
            for colInd, pixel in enumerate(row):
                self.drawDomain((rowInd, colInd))

    def getNeighbors(self, position):
        # neighbors = [0,1,2,3] # 0 is right, 1 down, 2 left, 3 above
        matrix = self.countNeighbours(np.zeros((4,4)))
        return matrix[position]

    def countNeighbours(self,theInputMatrix, countRadius=1, borderValue=0.):        
        """(Function found at https://davescience.wordpress.com/2011/12/12/counting-neighbours-in-a-python-numpy-matrix/)
        CountNeighbours(theInputMatrix,countRadius,borderValue) spirals around theInputMatrix to produce resultMatrix: 
        a matrix with the same dimensions as the input with with elements containing the sum of neighbour elements.
        The radius of the neighbours to include is set with counterRadius (default = 1), the value for elements beyond
        the borders is set with borderValue (default = 0.)."""
        heightFP, widthFP = theInputMatrix.shape  # define height and width of input matrix
        # make a matrix same size as input matrix plus borders the same size as the neighbour radius and
        # set the border to borderValue
        withBorders = np.ones(
            (heightFP + (2 * countRadius), widthFP + (2 * countRadius))) * borderValue
        # set the interior region to the input matrix
        withBorders[countRadius:heightFP + countRadius,
                    countRadius:widthFP + countRadius] = theInputMatrix
        # set up an empty matrix for the results
        resultMatrix = np.zeros((heightFP, widthFP))
        minRow, minCol = 0, 0
        maxRow, maxCol = 2. * countRadius, 2. * countRadius
        rowVal, colVal = 0, 0
        # spiral round...
        for i in range(4 * countRadius):
            while colVal < maxCol:  # move right along top of spiral
                resultMatrix = resultMatrix + \
                    withBorders[rowVal:heightFP +
                                rowVal, colVal:widthFP + colVal]
                colVal += 1

            while rowVal < maxRow:  # move down right hand side of spiral
                resultMatrix = resultMatrix + \
                    withBorders[rowVal:heightFP +
                                rowVal, colVal:widthFP + colVal]
                rowVal += 1

            while colVal > minCol:  # move left along base of spiral
                resultMatrix = resultMatrix + \
                    withBorders[rowVal:heightFP +
                                rowVal, colVal:widthFP + colVal]
                colVal -= 1
            minRow += 1
            maxCol -= 1
            while rowVal > minRow:  # move up left hand side of spiral
                resultMatrix = resultMatrix + \
                    withBorders[rowVal:heightFP +
                                rowVal, colVal:widthFP + colVal]
                rowVal -= 1
            minCol += 1
            maxRow -= 1
        return resultMatrix

    def clearDomains(self):
        self.domainText.remove()

    def animate(self):
        # Move through color squares and add image to animation.
        for rowInd, row in enumerate(self.colors):
            for colInd, col in enumerate(row):
                position = (rowInd, colInd)
                # Redraw domains.
                self.clearDomains()
                self.drawAllDomains()
                im = plt.imshow(self.colors, interpolation='none')
                if colInd != 3:
                    signalRight = self.sendText((position), self.domains[
                                                position] + '>', 'right')
                if rowInd != 3:
                    signalBottom = self.sendText(
                        (position), self.domains[position], 'down')
                # TODO: Check for self.conflicts for each direction.
                # If conflict, resolve conflict with `revise` method.
                title = self.ax.set_title(
                    'Unresolved constraints = ' + str(self.unresolved))
                self.ims.append(
                    [im, title, signalRight, self.ax, signalBottom])

        return animation.ArtistAnimation(self.fig, self.ims, interval=600, blit=True, repeat_delay=500)

model = ConstraintModel()
