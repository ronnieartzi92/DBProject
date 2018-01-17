import urllib2
import xml.etree.ElementTree as ET

api_key = 'r87bhSg3GG34XqX6'

API = 'http://api.eventful.com/rest/events/search?...&keywords={0}&date=Future&app_key=r87bhSg3GG34XqX6'


def get_events(artist):
        '''
        This script generate events objects list for every artists
        :param artist: artists name (string)
        :return: events list (or empty list if exception raised)
        '''
        try:
            # getting all events for artists - xml format
            result = []
            print 'event: {0}'.format(artist)
            url = API.format(artist).replace(' ', '%20')
            response = urllib2.urlopen(url).read()
            data = ET.fromstring(response)
            for item in data:
                try:
                    all = item.__dict__['_children']
                    for event in all:
                        # for every event, try to parse the relevant details from the event entity.
                        try:
                            for detail in event.__dict__['_children']:
                                if detail.tag == 'title':
                                    title = detail.text
                                if detail.tag == 'url':
                                    url = detail.text
                                if detail.tag == 'start_time':
                                    date = detail.text
                                if detail.tag == 'venue_name':
                                    venue = detail.text
                                if detail.tag == 'city_name':
                                    city = detail.text
                                if detail.tag == 'country_name':
                                    country = detail.text
                                # trying to bring image which is not must on owr DB
                                image = None
                                try:
                                    if detail.tag == 'image':
                                        raw_image = detail.__dict__['_children']
                                        image = raw_image[0].text
                                except Exception:
                                    print "no image for event {0}".format(title)

                            # generating event object and insert it to the data.
                            final_event = {'title': title, 'url': url, 'date': date,
                                          'venue': venue, 'city': city, 'country': country, 'img': image}
                            result.append(final_event)
                        except Exception:
                            continue  # continue for next event if Exception raised
                except Exception:
                    continue  # continue for next event if Exception raised
            return result
        except Exception, e:
            print "error get event"
            print e
            return result