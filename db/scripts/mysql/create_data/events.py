import urllib2
import xml.etree.ElementTree as ET

api_key = 'r87bhSg3GG34XqX6'

API = 'http://api.eventful.com/rest/events/search?...&keywords={0}&date=Future&app_key=r87bhSg3GG34XqX6'

def get_events(artist):
        try:
            result = []
            url = API.format(artist).replace(' ', '%20')
            response = urllib2.urlopen(url).read()
            data = ET.fromstring(response)
            for item in data:
                all = item.__dict__['_children']
                for event in all:
                    address = []
                    for detail in event.__dict__['_children']:
                        if detail.tag == 'title':
                            title = detail.text
                        if detail.tag == 'url':
                            url = detail.text
                        if detail.tag == 'description':
                            description = detail.text
                        if detail.tag == 'start_time':
                            date = detail.text
                        if detail.tag == 'venue_name':
                            venue = detail.text
                        if detail.tag == 'city_name':
                            city = detail.text
                        if detail.tag == 'country_name':
                            country = detail.text
                    final_evet = {'title': title, 'url': url, 'description': description, 'date': date,
                                  'venue': venue, 'city': city, 'country': country}
                    result.append(final_evet)
            return result
        except Exception, e:
            print "error get event"
            print e
