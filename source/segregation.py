from Map import Map
from Particles import Particles


myMap = Map()
myMap.initMap(100,100)

particles = Particles()
'''

    initParticles will receive the percenteige of each types:
    eg: 2 types each 45% of the map that is passed as Input
    args = [45, 45]

    The implementation also support multiple types eg. 3 or 4
'''
percentages = [45, 45]

particles.init(percentages, myMap, 4, 0, 1000)

print("Unhappy particles", len(particles.unHappyParticles))
particles.printParticles(False)
iterations, unhappy = particles.improveHappyParticles()
print("iterations", iterations)
print("UnHappy Particles", unhappy)
particles.printParticles(True)
