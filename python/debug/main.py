from neat_ref import *

gh = GenomeHistory(3,1)
pop = Population(gh, 10)


def eval(g:list[Genome]):
    for i in g:
        print(i.get_outputs([0.5, 0.5, 0.5]))


pop.run(eval, 5)



