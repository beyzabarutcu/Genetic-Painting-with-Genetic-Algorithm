from random import *

class Individual:
    def __init__(self, imgWidth, imgHeight):
        self.width = imgWidth 
        self.height = imgHeight
        
        nums = range(self.width)  #nums are points(pixels) in image
        self.points = ((sample(nums, 2)), (sample(nums, 2)), (sample(nums, 2))) # choose 6 points (x,y) randomly
                                                                               # x,y must be tuple
        self.color = (randint(0, 256), randint(0, 256), randint(0, 256), randint(0, 256))#random color

    def mutate(self, sigma=1.0):
        mutations = ['point', 'color', 'reset'] #mutation types
        mutationType = choices(mutations, weights=[45,45,10], k=1) #choose a mutaion typee randomly
                                                                         #weights are our probability to mutating
        if mutationType == 'point':
           x = int(randint(0, self.width)*sigma)
           y = int(randint(0, self.width)*sigma)
           
           index = choice(list(range(len(self.points))))
           self.points = list(self.points)
           self.points[index] = (x, y)
           tuple(self.points)
         
        elif mutationType == 'color':
            self.color = tuple(
                c + int(random.randint(-0, 256) * sigma) for c in self.color
            )
            
        else:
            reset = Individual(self.width,self.height)
            
            self.points = reset.points
            self.color = reset.color



