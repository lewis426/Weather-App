import requests
import bs4
import collections

WeatherReport = collections.namedtuple('WeatherReport', 'cond, temp, scale, location')


def main():
    while True:
        try:
            print_the_header()
            zipcode = input('What zipcode would you like the weather for?(e.g. 90210): ')
            html = get_html_from_web(zipcode)
            # parse the html
            report = get_weather_from_html(html)
            # display weather for forecast
            print('The temperature in {0} is {1}\N{DEGREE SIGN}{2} and the condition is {3}.'.format(report.location,
                                                                                                 report.temp,
                                                                                                 report.scale,
                                                                                                 report.cond))
            break
        except AttributeError:
            print('Please enter a valid zip code (UK post codes not yet available)')
            print()
            continue
def print_the_header():
    print('-------------------------')
    print('      WEATHER APP')
    print('-------------------------')
    print()


def get_html_from_web(code):
    url= 'http://www.wunderground.com/weather-forecast/{}'.format(code)
    response = requests.get(url)
    # print(response.status_code)
    # print(response.text[0:250])
    return response.text


def get_weather_from_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    loc = clean_up_text(soup.find(class_='region-content-header').find('h1').get_text())
    condition = clean_up_text(soup.find(class_='condition-icon').get_text())
    temp = clean_up_text(soup.find(class_='wu-unit-temperature').find(class_='wu-value wu-value-to').get_text())
    scale = clean_up_text(soup.find(class_='wu-unit-temperature').find(class_='wu-label').get_text())
    #print(loc)
    #print('{0}, {1}\N{DEGREE SIGN}{2}'.format(condition, temp, scale))
    report = WeatherReport(condition, temp, scale, loc)
    return report


def clean_up_text(text):
    if not text:
        return text
    else:
        text = text.strip()
        return text


if __name__ == '__main__':

    main()
