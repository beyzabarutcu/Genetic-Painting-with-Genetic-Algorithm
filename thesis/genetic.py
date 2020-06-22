import os
from copy import deepcopy
from random import *

from PIL import Image
from evol import Evolution, Population

from painting import DrawImage


def score(x:DrawImage) -> float: # Calculate the distance to the target image
                                #fitness
    score = x.image_diff(x.targetImage)
    print(".", end='', flush=True)
    return score

def selection(pop, maximize=False): #selection part

    evaluated_individuals = tuple(filter(lambda x: x.fitness is not None, pop))
    if len(evaluated_individuals) > 0:
        mom = max(evaluated_individuals, key=lambda x: x.fitness if maximize else -x.fitness)
    else:
        mom = choice(pop)
    dad = choice(pop)
    return mom, dad

def mutation(x:DrawImage, rate=0.04, sigma=1.0) -> DrawImage: #mutation part

    x.mutatePolygons(rate=rate, sigma=sigma)
    return deepcopy(x)

def crossover(mom:DrawImage, dad:DrawImage): #crossover part

    child_a, child_b = DrawImage.mate(mom, dad)
    return deepcopy(child_a)

def final(pop, img_template="output%d.png", checkpoint_path="output") -> Population:
    avg_fitness = sum([i.fitness for i in pop.individuals])/len(pop.individuals)

    print("\nCurrent generation %d, best score %f, population. avg. %f " % (pop.generation, pop.current_best.fitness, avg_fitness))
    img = pop.current_best.chromosome.draw()
    img.save(img_template % pop.generation, 'PNG')
    img.show()
    
    if pop.generation % 50 == 0:
        pop.checkpoint(target=checkpoint_path, method='pickle')

    return pop


if __name__ == "__main__":
    
    checkpoint_path = "./geneticArt/"
    image_template = os.path.join(checkpoint_path, "drawing_%05d.png")
    targetImage = Image.open("./img/unicorn.png").convert('RGBA')
    #targetImage.show()

    #size = targetImage.size

    numPolygons = 150
    popSize: int = 200
    
    pop = Population(chromosomes=[DrawImage(numPolygons, targetImage, background_color=(255, 255, 255)) for _ in range(popSize)],
                         eval_function=score, maximize=False, concurrent_workers=6)

    evolution = (Evolution()
                     .survive(fraction=0.05)
                     .breed(parent_picker=selection, combiner=crossover, population_size=popSize)
                     .mutate(mutate_function=mutation, rate=0.05)
                     .evaluate(lazy=False)
                     .apply(final, img_template=image_template, checkpoint_path=checkpoint_path))
    
    pop = pop.evolve(evolution, n=2000)

    
