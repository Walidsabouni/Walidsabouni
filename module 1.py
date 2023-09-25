import random
from datetime import datetime
bericht = input('schrijf uw bericht:(max 140 karakters)')
if len(bericht) <= 140:
    naam = input('vul uw naam in')
    if naam == ' ':
        print('anoniem')
elif len(bericht) > 140:
    raise ValueError('Uw mag maximaal 140 karakters gebruiken!')

print(datetime.now())
stations = ['Arnhem', 'Almere', 'Amersfoort']
print(random.choice(stations))
