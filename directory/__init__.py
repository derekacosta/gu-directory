from bs4 import BeautifulSoup
import requests


class GUDirectory():
    def __init__(self):
        self.SIMPLE_URL = 'https://contact.georgetown.edu/simpleSearch/'
        self.SIMPLE_HEADERS = {
            'Referer': self.SIMPLE_URL
        }

        self.ADVANCED_URL = 'https://contact.georgetown.edu/advancedsearch/'
        self.ADVANCED_HEADERS = {
            'Referer': self.ADVANCED_URL
        }

        self.CATEGORIES = ['employees', 'students', 'both']
        self.FILTERS = ['exact', 'starts_with', 'contains']

        self.session = requests.Session()

    def simple_search(self, search, category='both'):
        '''
        execute a simple search of directory
        '''
        if self.invalid_search(search):
            raise Exception('A search term must be at least three letters long.')
        if category not in self.CATEGORIES:
            raise Exception('Invalid category type')

        # get csrf token
        response = self.session.get(self.SIMPLE_URL)
        csrf_token = response.cookies['csrftoken']

        data = {
            'csrfmiddlewaretoken': csrf_token,
            'Search': search
        }
        if category != 'students':
            data['SearchEmployee'] = 'Employee'
        if category != 'employees':
            data['SearchStudent'] = 'Student'

        response = self.session.post(self.SIMPLE_URL, data=data, headers=self.SIMPLE_HEADERS)
        return self.parse_results(response)

    def advanced_search(self, first='', last='', phone='', department='', first_match='exact', last_match='exact', phone_match='exact', department_match='exact', category='both'):
        '''
        execute an advanced search of directory
        '''
        if self.invalid_search(first, last, phone, department):
            raise Exception('A search term must be at least three letters long.')
        if self.invalid_filter(first_match, last_match, phone_match, department_match):
            raise Exception('Invalid match type')
        if category not in self.CATEGORIES:
            raise Exception('Invalid category type')

        # get csrf token
        response = self.session.get(self.ADVANCED_URL)
        csrf_token = response.cookies['csrftoken']

        data = {
            'csrfmiddlewaretoken': csrf_token,
            'lastNameMatch': self.FILTERS.index(last_match),
            'lastName': last,
            'firstNameMatch': self.FILTERS.index(first_match),
            'firstName': first,
            'phoneMatch': self.FILTERS.index(phone_match),
            'phoneNo': phone,
            'deptMatch': self.FILTERS.index(department_match),
            'department': department
        }
        if category != 'students':
            data['employeeSearch'] = 'on'
        if category != 'employees':
            data['studentSearch'] = 'on'

        response = self.session.post(self.ADVANCED_URL, data=data, headers=self.ADVANCED_HEADERS)
        return self.parse_results(response)

    def invalid_search(self, *terms):
        '''
        return whether search is invalid
        '''
        for term in terms:
            if len(term) > 0 and len(term) < 3:
                return True
        return False

    def invalid_filter(self, *filters):
        '''
        return whether filters are invalid
        '''
        for _filter in filters:
            if _filter not in self.FILTERS:
                return True
        return False

    def parse_results(self, response):
        '''
        parse and return directory results
        '''
        soup = BeautifulSoup(response.content, 'html.parser')
 
        # no results
        error = soup.find('font', {'color': 'red'})
        if error:
            return []
 
        # single result
        if 'view' in response.url:
            fields = {_input['name']: _input['value'] for _input in soup.find('form', {'id': 'go-to-VCard'}).find_all('input')}
            return ((
                fields['FullName'] if 'FullName' in fields else '',
                fields['NetID'] if 'NetID' in fields else '',
                fields['Title'] if 'Title' in fields else '',
                fields['DepartmentName'] if 'DepartmentName' in fields else '',
                fields['Phone'] if 'Phone' in fields else ''
            ),)
        
        # table of results
        else:
            rows = soup.find('table').find_all('tr', {'class': ['ListPrimary', 'ListAlternate']})
            results = []
            for row in rows:
                data = row.find_all('td')
                results.append((
                    data[0].find('a').text,                                         # name
                    data[0].find('a')['href'].rsplit('/', 1)[1],                    # netid
                    data[1].find(text=True, recursive=False).strip(),               # title
                    data[1].find('small').text if data[1].find('small') else '',    # department
                    data[2].text.strip()                                            # phone
                ))
            return results
