import dataclasses
import shlex
import sys

import bs4
import requests

from ..login import interactive_login

MOSES_URL = 'https://moseskonto.tu-berlin.de'
MOSES_PERSONS_URL = '/moses/administration/personen'
MOSES_SEARCH_URL = MOSES_URL + MOSES_PERSONS_URL + '/suche.html'
MOSES_SHIB_URL = MOSES_URL + '/moses/shibboleth/login'


@dataclasses.dataclass
class Person:
    name: str
    surname: str
    username: str
    role: str
    id: int
    group: str
    email: str = ''
    link: str = ''
    degree_program = ''
    degree = ''

    def to_basic_str(self) -> str:
        l = [self.name, self.surname, self.username, self.id, self.role, self.group]
        return ','.join(map(lambda x: shlex.quote(x), l))

    def to_extended_str(self) -> str:
        l = [self.name, self.surname, self.username, self.id, self.role, self.group, self.email, self.degree_program,
             self.degree]
        return ','.join(map(lambda x: shlex.quote(x), l))

    def fetch_details(self, session):

        if self.link == '':
            raise ValueError('No link to details page provided!')

        rsp = session.get(self.link)
        soup = bs4.BeautifulSoup(rsp.content, 'html.parser')
        basic = soup.find('div', id=lambda i: i is not None and ':personendaten' in i)

        if basic:
            # Label is dependent on the language
            # But: Language is set in a stateful way, so
            # There is not much we can do

            EMAIL_LABEL_GER = 'E-Mail'
            EMAIL_LABEL_EN = 'Email'
            for label in basic.find_all('label'):
                if label.text == EMAIL_LABEL_GER or label.text == EMAIL_LABEL_EN:
                    iter = label.parent.stripped_strings
                    next(iter, None)
                    self.email = next(iter, None)

        study = soup.find('div', id=lambda i: i is not None and ':studium' in i)
        field = study.find(lambda t: t.name == 'div' and t.has_attr('class') and 'ui-datatable' in t['class'])

        DEGREE_PROGRAM_LABEL_GER = 'Studiengang'
        DEGREE_PROGRAM_LABEL_EN = 'Degree program'
        DEGREE_LABEL_GER = 'Abschluss'
        DEGREE_LABEL_EN = 'Degree'

        if field:
            row = field.findNext('tr')  # Skip header row
            col_headers = list(map(lambda th: th.text, row.findAll('th')))

            ix_program = None
            ix_degree = None

            try:
                ix_program = col_headers.index(DEGREE_PROGRAM_LABEL_GER)
            except ValueError:
                ix_program = col_headers.index(DEGREE_PROGRAM_LABEL_EN)

            try:
                ix_degree = col_headers.index(DEGREE_LABEL_GER)
            except ValueError:
                ix_degree = col_headers.index(DEGREE_LABEL_EN)

            row = row.findNext('tr')
            cols = list(map(lambda c: c.text, row.findAll('td')))

            if len(cols) != len(col_headers):
                return

            if ix_program is not None:
                self.degree_program = cols[ix_program]

            if ix_degree is not None:
                self.degree = cols[ix_degree]


def search_people(session: requests.Session,
                  lastname='',
                  surname='',
                  email='',
                  username='',
                  student_id='',
                  extended=False):
    r = session.get(MOSES_SEARCH_URL)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    view_state = soup.find('input', attrs={'name': 'javax.faces.ViewState'})['value']
    jfwid = soup.find('input', attrs={'name': 'javax.faces.ClientWindow'})['value']

    form = soup.find(lambda tag: tag.name == 'form' and tag['id'].startswith('j_idt'))

    lastname_id = form.find(lambda t: t.name == 'div' and
                                      t.find('label').text in ['Nachname']).input['name']  # it's not translated

    surname_id = form.find(lambda t: t.name == 'div' and
                                     t.find('label').text in ['Vorname', 'First name']).input['name']

    email_id = form.find(lambda t: t.name == 'div' and
                                   t.find('label').text in ['E-Mail-Adresse']).input['name']  # not translated, either

    username_id = form.find(lambda t: t.name == 'div' and
                                      t.find('label').text in ['Benutzername', 'User name']).input['name']

    student_id_id = \
        form.find(lambda t: t.name == 'div' and
                            t.find('label').text in ['Matrikelnummer', 'Matriculation number']).input['name']

    button_id = form.find(lambda t: t.name == 'a' and
                                    t.has_attr('id') and t['id'].startswith(f'{form["id"]}:j_idt'))['id']

    payload = {
        "javax.faces.source": button_id,
        'javax.faces.partial.ajax': 'true',
        'javax.faces.partial.execute': '@all',
        'javax.faces.partial.render': form['id'],
        button_id: button_id,
        form['id']: form['id'],
        lastname_id: lastname if lastname is not None else "",
        surname_id: surname if surname is not None else "",
        email_id: email if email is not None else "",
        username_id: username if username is not None else "",
        student_id_id: student_id if student_id is not None else "",

        'javax.faces.ViewState': view_state,
        'javax.faces.ClientWindow': jfwid
    }

    headers = {
        'Referer': 'https://moseskonto.tu-berlin.de/moses/administration/personen/suche.html',
        'Faces-Request': 'partial/ajax',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Language': 'de-DE,en-US;q=0.7,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    params = {
        'jfwid': jfwid
    }

    r: requests.Response = session.post(MOSES_SEARCH_URL, data=payload, headers=headers, params=params)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    soup = soup.find('tbody', attrs={'class': 'ui-datatable-data ui-widget-content'})

    if soup is None:
        return []

    results = []
    for record in soup.findAll('tr'):
        cols = map(lambda c: c.text, record.findAll('td'))
        cols = list(cols)[:-1]  # Drop unnecessary last column
        p = Person(*cols)

        if extended:
            link = record.find('a', attrs={'class': 'btn btn-default btn-sm'})

            if link:
                ext = MOSES_PERSONS_URL + '/' + link['href']
                p.link = MOSES_URL + ext
                p.fetch_details(session)

        results.append(p)

    return results


def main(args):
    _, _, s = interactive_login(MOSES_URL, MOSES_SHIB_URL, user=args.user, pw=args.password,
                                store_creds=args.store_credentials, clear_creds=args.clear_credentials)

    if args.batch is None:
        for r in search_people(s,
                               lastname=args.surname,
                               surname=args.firstname,
                               email=args.email,
                               username=args.account_name,
                               student_id=args.id,
                               extended=args.extended
                               ):

            if not args.extended:
                print(r.to_basic_str())
            else:
                print(r.to_extended_str())

    else:
        for line in sys.stdin.readlines():
            kwargs = {
                'username': line.strip() if args.batch == 'account' else '',
                'student_id': line.strip() if args.batch == 'id' else '',
                'email': line.strip() if args.batch == 'email' else '',
                'extended': args.extended
            }
            res = search_people(s, **kwargs)
            if res:

                if args.extended:
                    print(res[0].to_extended_str())
                else:
                    print(res[0].to_basic_str())
            else:
                print('N/A', line.strip())
