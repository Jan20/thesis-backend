import os
import sys
import random
import string

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from models.level import Level
from models.user import User
from database.database import Database
from models.level import Level

#
#
#
class Evolution(object):

    ##################
    ## Constructors ##
    ##################

    ###############
    ## Functions ##
    ###############    
    def execute(self, user_key: str) -> str:

        #
        #
        #
        database: Database = Database()

        #
        #
        #
        random_level: Level = database.get_random_level('')

        #
        #
        #
        evolved_level: Level = self.evolve(random_level)

        #
        #
        #
        session_key: str = database.generate_session(user_key, evolved_level)
        
        #
        #
        #
        return session_key


    def evolve(self, level: Level) -> Level:

        print(level.representation)

        level.representation[1][2] = 'C'
        level.representation[1][3] = 'C'
        level.representation[1][4] = 'C'
        level.representation[1][5] = 'C'
        level.representation[1][6] = 'C'
        level.representation[1][7] = 'C'

        return level


#     #
#     #
#     #
#     #
#     #
#     def execute(self, in_string: str, in_string_length: int, population: int, generations: int):

#         agents = self.init_agents(population, in_string_length)

#         for generation in range(generations):

#             print("Generation:" + str(generation))

#             agents = self.fitness(agents, in_string)
#             agents = self.selection(agents)
#             agents = self.crossover(agents, population, in_string_length)
#             agents = self.mutation(agents, in_string, in_string_length)

#             if any(agent.fitness >= 90 for agent in agents):

#                 print('Threshold met!')
#                 exit(0)


#     #
#     #
#     #
#     #
#     def init_agents(self, population: int, in_string_length: int):

#         return [Agent(in_string_length) for _ in range(population)]


#     #
#     #
#     #
#     def fitness(self, agents: [Agent], in_string: str):

#         for agent in agents:

#             agent.fitness = fuzz.ratio(agent.string, in_string)

#         return agents

#     #
#     #
#     #
#     #

#     def selection(self, agents: [Agent]):

#         agents = sorted(agents, key=lambda agent: agent.fitness, reverse = True)
#         print('\n'.join(map(str, agents)))
        
#         return agents[:int(0.2 * len(agents))]


#     # 
#     #
#     #
#     #
#     def crossover(self, agents: [Agent], population: int, in_string_length: int):

#         offspring = []

#         for _ in range(int((population - len(agents)) / 2)):

#             parent1 = random.choice(agents)
#             parent2 = random.choice(agents)

#             child1 = Agent(in_string_length)
#             child2 = Agent(in_string_length)

#             split = random.randint(0, in_string_length)

#             child1.string = parent1.string[0:split] + parent2.string[split:in_string_length]
#             child2.string = parent2.string[0:split] + parent1.string[split:in_string_length]

#             offspring.append(child1)
#             offspring.append(child2)

#         agents.extend(offspring)

#         return agents


#     def mutation(self, agents: [Agent], in_string: str, in_string_length: int):

#         for agent in agents:

#             for index, param in enumerate(agent.string):

#                 if random.uniform(0.0, 1.0) <= 0.3:

#                     agent.sring = agent.string[0: index] + random.choice(string.ascii_letters) + agent.string[index + 1 : in_string_length]

#         return agents



# Genetic_Algorithm().execute('Deutschland', len('Deutschland'), 10, 100000)