import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TheArtVillage.settings')

import django
django.setup()

from models import Art, Agent


def populate():
    agent_add1 = Agent(name='Test 1',phone='0',postcode='AA1AA1')
    agent_add1.save()
    agent_add2 = Agent(name='Test 2',phone='1',postcode='AA1AA2')
    agent_add2.save()
    agent_add3 = Agent(name='Test 3',phone='2',postcode='AA1AA3')
    agent_add3.save()

    count = 0
    artist = 0
    agents = [agent_add1,agent_add2,agent_add3]

    while count < 1000:
        artist = int(artist)
        if artist % 5 == 0:
            artist += 1

        artist = str(art)

        ag = agents[count%3]

        art = Art(name=str(count), sub_category=str(int(artist)%3), category=str(count%10), artist=artist, price=50, quantity=0, agent=ag)
        art.save()

        count += 1




# Start execution here!
if __name__ == '__main__':
    print "Starting Art Village population script..."
    populate()