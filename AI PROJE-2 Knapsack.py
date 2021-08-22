import random
import math

class Knapsack:

    def __init__(self,capacity, weights, profits, pop_size, generation_num):
        self.capacity = capacity
        self.weights = weights
        self.profits = profits
        self.pop_size = pop_size
        self.generation_num = generation_num
        self.population = []
        

    # İlk popülasyon oluşturulur.
    def initial_pop(self):
        for i in range(self.pop_size):
            self.population.append([random.randint(0,1) for x in range(len(weights))]) #ağırlık listesinin uzunluğu kadar gene sahip 
                                                                                        #gene sahip bireyler oluşturulup populasyona eklendi
    def fitness(self, chromosome):
        # tüm popülasyonunun fitness degerleri hesaplanır
        sum_weight = 0
        sum_profit = 0
        # her bir bireyin ağırlık ve kazanç değerlerini gen sayısıyla çarparak hesaplar
        for i, gene in enumerate(chromosome):
            sum_weight += self.weights[i] * gene
            sum_profit += self.profits[i] * gene

        if sum_weight > self.capacity:
            return -1    # eğer toplam ağırlık belirtilen maksimum ağırlıktan fazla ise -1 döndürür
        else:
            return sum_profit

    def tournament_selection(self, pop, K):
        """
        populasyon listesi ile turnuva sayısını parametre olarak alır
        """
        best_contestant = 'None'
        for i in range(K):
            contestant = pop[random.randint(0, self.pop_size - 1)] # popülasyondan rastgele bireyler seçilir ve karsılastırılır.
            if (best_contestant == 'None') or self.fitness(contestant) > self.fitness(best_contestant):
                best_contestant = contestant[:] # en iyi fitness degerine sahip bireyi döndürür
        return best_contestant
    
    def roulette_selection(self, fitness_list):
        
        fitness_list.sort(key=lambda x: x[0], reverse=True)

        # find total fitness 
        total = 0
        pool = []
        fitness_rate_list = []
        for fit, chromosome in fitness_list:
            if fit == -1:
                continue
            total += fit
        #print("total:", total)
        if total == 0:
            return fitness_list[random.randint(0,len(fitness_list)-1)][1]

        # toplam fitness değerine bölünerek herbir populasyonun fitness değeri belirlenmektedir.
        for i in range(len(fitness_list)):
            fitness_rate_list.append((math.ceil(fitness_list[i][0]*100/total), self.population[i]))

        # havuza her elamanın bulunma yüzdesi kadar populasyondaki elemanlar eklendi.
        for fitness in fitness_rate_list:
            for j in range(fitness[0]):
                pool.append(fitness[1])
        return pool[random.randint(0, len(pool) - 1)]  # havuzdan rastgele bir parent seçiliyor

    def one_point_crossover(self, p1, p2): 
        ch1, ch2 = p1, p2

        # one point crossover
        point = random.randint(1, len(ch1) - 1)
        tmp1 = ch1[point:]
        tmp2 = ch2[point:]
        ch1 = ch1[:point]
        ch2 = ch2[:point]
        ch1 = ch1 + tmp2
        ch2 = ch2 + tmp1
        return ch1, ch2

    def multipoint_crossover(self, p1, p2):

        ch1, ch2 = p1, p2
        # multipoint crossover
        point1 = random.randint(1, (len(ch1) - 1) // 2)
        point2 = random.randint((len(ch1) - 1) // 2 + 1, len(ch1) - 1)

        temp1 = ch1[point1:point2]
        temp1_1 = ch1[point2:]
        temp2 = ch2[point1:point2]
        temp2_2 = ch2[point2:]
        ch1 = ch1[:point1]
        ch2 = ch2[:point1]
        ch1 = ch1 + temp2 + temp1_1
        ch2 = ch2 + temp1 + temp2_2


        return ch1 , ch2

    def mutation(self, chromosome): 
        for i in range(len(chromosome)):
            k = random.uniform(0, 100)
            if k < 8:
                # yüzde8 ihtimalle mutasyon gerçekleşir
                if chromosome[i] == 1:
                    chromosome[i] = 0
                else:
                    chromosome[i] = 1
        return chromosome

    def printResult(self, population): #işlemler sonucu çıkan en optimal sonucu yazdırır
        print("Last Generation: \n", population)
        last_gen_fitn = []
        for i in range(len(population)):
            last_gen_fitn.append(self.fitness(population[i]))
        sorted_pop = [x for _, x in sorted(zip(last_gen_fitn, population), key=lambda x: x[0], reverse=True)]
        print("Last generation fitness: ", last_gen_fitn)
        print("Optimum result: ", sorted_pop[0])

    def genetic(self):
        for i in range(self.generation_num):
            fitness_list = []
           #fitness_list1 = []
            new_pop = []
            for j in range(self.pop_size):
                fitness_list.append((self.fitness(self.population[j]), self.population[j]))  #fitness değerlerinin ve kromozomların olduğu liste
                #fitness_list1.append(self.fitness(self.population[j]))
            print("fitness_list: ", fitness_list)
            # if self.pop_size % 2 == 0:  ## geliştirilecek.....
            #     # en iyi ilk iki kromozom yeni populasyona ekleniyor
            #     fitness_list.sort(key=lambda x: x[0], reverse=True)
            #     new_pop.append(fitness_list[0][1])
            #     new_pop.append(fitness_list[1][1])
            # else:
            #     # en iyi kromamzan yeni populasyona ekleniyor
            #     fitness_list.sort(key=lambda x: x[0], reverse=True)
            #     new_pop.append(fitness_list[0][1]) ## geliştirilecek.....

            fitness_list.sort(key=lambda x: x[0], reverse=True)
            #new_pop.append(fitness_list[0][1])

            print("fitness_list sorted: ", fitness_list)

            for k in range(math.ceil((len(self.population)/2))):
                # iki birey seçilerek yeni iki birey oluşturulacak
                # x = self.roulette_selection(fitness_list) # roulette selection ile 2 parent seçimi
                # y = self.roulette_selection(fitness_list)
                x = self.tournament_selection(self.population, 5) #tournament yöntemi ile 2 tane paren seciliyor.
                y = self.tournament_selection(self.population, 5)
                ch1, ch2 = self.multipoint_crossover(x, y)  #crossover işlemleri 
                # ch1, ch2 = self.one_point_crossover(x, y)
                ch1, ch2 = self.mutation(ch1), self.mutation(ch2) # mutasyon işlemleri
                new_pop.append(ch1)
                #populasyon maksimum sayıya ulaştıysa break
                if len(new_pop) == pop_size:
                    break
                new_pop.append(ch2)
            print("old pop:", self.population)
            print("new pop: ", new_pop)
            self.population = new_pop
            print("population:", self.population)
        self.printResult(self.population)


# weights = [random.randint(1,10) for i in range(5)]
# profits = [random.randint(5,25) for i in range(5)]

weights = [12, 7, 11, 8, 9]
profits = [24, 13, 23, 15, 16]
#optimal= [ 0,1,1,1,0 ]  
capacity = 26
pop_size = 10
no_of_gen = 100

knapsack = Knapsack(capacity, weights, profits, pop_size, no_of_gen)
knapsack.initial_pop()
knapsack.genetic()