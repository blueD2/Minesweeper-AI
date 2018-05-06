import random
from minesweeper import Minesweeper
from ann import ANN
import config
import numpy

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

creator.create("FitnessMax", base.Fitness, weights = (1.0,))
creator.create("Individual",list,fitness=creator.FitnessMax)

toolbox = base.Toolbox()

#we dont have a method to create a minesweeper object?
sweepGame = Minesweeper()#is this correct?

def rand(lower, upper):
    diff = upper - lower
    return random.random() * diff + lower

toolbox.register("attr_real", rand, -1.337, 1.337)

#how many weights? 25 inputs, so (25 + bias)*hidden nodes + (hiddenlayer-1) * (hiddenNodes + 1)* (hidden nodes) + (hidden nodes + bias) * outputs

num_inputs = config.nnet['n_inputs']
num_h_layers = config.nnet['n_h_layers']
num_h_neurons0 = config.nnet['n_h_neurons0']
num_h_neurons1 = config.nnet['n_h_neurons1']
num_outputs = config.nnet['n_outputs']

#weights of inputs to hidden + all hidden to hidden + hidden to outputs
weight_count = (num_inputs+1)*num_h_neurons0 + (num_h_neurons0+1)*num_h_neurons1 + (num_h_neurons1 + 1)*num_outputs

#(num_h_layers-1)*(num_h_neurons0 + 1)*(num_h_neurons0) +

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_real, n = weight_count) 
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalFit(individual):
    ann = ANN(num_inputs, num_h_neurons0, num_h_neurons1, num_outputs, individual)
    fitNum = sweepGame.playgame(ann, False)
    return fitNum,

toolbox.register("evaluate",evalFit)

toolbox.register("select",tools.selTournament, tournsize = 3)
toolbox.register("mate", tools.cxBlend, alpha = .75)
toolbox.register("mutate", tools.mutGaussian, mu = 0, sigma = .1337, indpb = .3) 
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("max", numpy.max)
stats.register("std", numpy.std)
fBest = open("best.txt", "w+")
fMean = open("mean.txt", "w+")
fStd = open("std.txt", "w+")

prob_xover = config.ga['cxpb']
prob_mut = config.ga['mutpb']
pop = toolbox.population(n = config.ga['pop_size'])

print("Generation 0")
fitnesses = toolbox.map(toolbox.evaluate,pop)
for ind, fit in zip(pop,fitnesses):
    ind.fitness.values = fit
    #print(str(fit))
    
record = stats.compile(pop)
print(record)
fBest.write(str(record['max']) + "\n")
fMean.write(str(record['avg']) + "\n")
fStd.write(str(record['std']) + "\n")

#output = open("output.txt","a+")

for g in range(1,config.ga['n_gens']):
    offspring = toolbox.select(pop,len(pop))
    offspring = algorithms.varAnd(offspring, toolbox, prob_xover, prob_mut)
    pop[:] = offspring

    #some code putting individuals back into game or something, if needed

    if(g % 1 == 0):
        print("Generation " + str(g))
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop,fitnesses):
        ind.fitness.values = fit
        #print(str(fit))
     
    record = stats.compile(pop)
    print(record)
    fBest.write(str(record['max']) + "\n")
    fMean.write(str(record['avg']) + "\n")
    fStd.write(str(record['std']) + "\n")


fBest.close()
fMean.close()
fStd.close()
best = tools.selBest(pop, k=1)[0]
ann = ANN(num_inputs, num_h_neurons0, num_h_neurons1, num_outputs, best)
print("Training done, results for best individual playing 20 times:")
for i in range(0,20):
    sweepGame.playgame(ann, True)
#print final generation
#for ind in pop:
    #output.write(str(ind[0])+": "+str(ind.fitness.values)+"\n")

#output.close()


