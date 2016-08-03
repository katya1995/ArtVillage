import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITI3.settings')

import django
django.setup()

from TheArtVillage.models import Art, Agent, Artist


def populate():
    agent_add1 = Agent(surname='Test', firstname='a', phone='0',postcode='AA1AA1', email='test@test.com')
    agent_add1.save()
    agent_add2 = Agent(surname='Test',firstname='b',phone='1',postcode='AA1AA2', email='test@test.com')
    agent_add2.save()
    agent_add3 = Agent(surname='Test',firstname='c',phone='2',postcode='AA1AA3', email='test@test.com')
    agent_add3.save()

    artist_add = Artist(firstname='Test', surname='t',description='This is a description')
    artist_add.save()

    count = 0
    artist = 0
    agents = [agent_add1,agent_add2,agent_add3]

    while count < 50:
        agent_add = Agent(surname=str(count), firstname='hello', phone=str(count),postcode=str(count), email='test@test.com')
        agent_add.save()
        count += 1

    while count < 10000:
        artist = int(artist)
        if artist % 5 == 0:
            artist += 1

        artist = str(artist)

        ag = agents[count%3]

        art = Art(name=str(count), sub_category=str(int(artist)%3), category=str(count%10), artist_id=artist_add, \
                  price=50, quantity=1, agent_id=ag, weight=50, size=50, postage_price=5)
        art.save()

        count += 1




# Start execution here!
if __name__ == '__main__':
    print "Starting Art Village population script..."
    populate()
    print "Done"