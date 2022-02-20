
import random
import json

from datetime import datetime

def randG(n):
    G  = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                cost = random.randint(1, 20)
                G[i][j], G[j][i] = cost, cost
    return G

def print_graph(G):
    for row in G:
        print(row)

def create_random_pool(G, n, pop_size):
    genes = []
    for _ in range(pop_size):
        gene = [(i) for i in range(n)]
        random.shuffle(gene)
        gene.append(gene[0])
        genes.append(Gene(G, gene))
    return genes


def write_population_to_file(population):
    with open("population_history.json", "r+") as f:
        genes = [gene.getGene() for gene in population] 
        now = datetime.now()

        file_data = json.load(f)
        print(file_data)
        current_time = now.strftime("%H:%M:%S")
        entry = {current_time: genes}
        file_data.append(entry)
        json.dump(file_data, f)


def main():

    GENE_SIZE = 5
    POP_SIZE = 10
    DURATION = 4 

    G = randG(GENE_SIZE)

    population = create_random_pool(G, GENE_SIZE, POP_SIZE) # produce an even number

    write_population_to_file(population)
    print(write_population_to_file)

    # print("GET GENE: " + str(population[0].getGene()))
    population.sort(key = lambda gene : gene.getCost())

    history = []

    for _ in range(DURATION):

        history.append(population[0])

        new_population = []

        for j in range(len(population)-1):
            parent1, parent2 = population[j],population[j+1]
            child1, child2 = parent1.mate(parent2), parent2.mate(parent1)
            child1.mutate(); child2.mutate();
            new_population = new_population + [child1, child2]

        new_population.sort(key = lambda gene: gene.getCost())
        mid = POP_SIZE//2
        population = new_population[:mid+1]

    cream_of_the_crop = population[0]

    history.append(cream_of_the_crop)
    for i, gene in enumerate(history):
        print(f"{i}) {gene}")



class Gene:
    def __init__(self, G, gene=None):
        self.G = G
        self.n = len(G)
        self.gene = [(i % self.n) for i in range(self.n+1)] if not gene else gene
        self.cost = 0
        self.calcCost()

    def calcCost(self):
        for i in range(0, self.n-1):
            a, b = self.gene[i], self.gene[i+1]
            self.cost  += self.G[a][b]

    def mutate(self):
        allele1 = random.randint(0,self.n-1) 
        allele2 = allele1
        while allele1 == allele2:
            allele2 = random.randint(0,self.n-1) 

        # sawap two alleles
        self.gene[allele1], self.gene[allele2] = self.gene[allele2], self.gene[allele1]
        self.gene = self.gene[:-1] + [self.gene[0]]
        self.calcCost()

    def getGene(self):
        return self.gene

    def getCost(self):
        return self.cost

    def __str__(self):
        return "gene: " + str(self.gene) + " cost: " + str(self.cost)

    def mate(self, lover):
        #interleave genes 
        child = []
        i_turn = True
        i = 0; j = 0
        while i < self.n and j < self.n:
            if i_turn:
                if self.gene[i] not in child:
                    child.append(self.gene[i])
                i+=1
            else:
                if lover.getGene()[j] not in child:
                    child.append(self.gene[j])
                j+=1
        child.append(child[0])

        return Gene(self.G, child)

    
        
    



if __name__ == '__main__':
    main()