import requests
import pandas as pd
import io
import os
from dotenv import load_dotenv
load_dotenv()


login_data = {
  'username': os.getenv('INTEGRAL_USER_NAME'),
  'password': os.getenv('INTEGRAL_PASSWORD')
}

# standard headers for grades request
default_headers = {
'authority': 'my.integralmaths.org',
'cache-control': 'max-age=0',
'upgrade-insecure-requests': '1',
'content-type': 'application/x-www-form-urlencoded',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

# standard headers for grades request
default_data = [
  ('mform_isexpanded_id_gradeitems', '1'),
  ('checkbox_controller1', '1'),
  ('mform_isexpanded_id_options', '1'),
  ('export_onlyactive', '1'),
  ('sesskey', 'O7eeaaleKC'),
  ('_qf__grade_export_form', '1'),
  ('itemids[1915]', '0'),
  ('itemids[1918]', '0'),
  ('itemids[1919]', '0'),
  ('itemids[1921]', '0'),
  ('itemids[1922]', '0'),
  ('itemids[1923]', '0'),
  ('itemids[1924]', '0'),
  ('itemids[1925]', '0'),
  ('itemids[1926]', '0'),
  ('itemids[1927]', '0'),
  ('itemids[1928]', '0'),
  ('itemids[1920]', '0'),
  ('itemids[1917]', '0'),
  ('itemids[6300]', '0'),
  ('itemids[197]', '0'),
  ('itemids[5077]', '0'),
  ('itemids[5083]', '0'),
  ('itemids[5089]', '0'),
  ('itemids[5096]', '0'),
  ('itemids[5102]', '0'),
  ('itemids[5106]', '0'),
  ('itemids[5112]', '0'),
  ('itemids[5124]', '0'),
  ('itemids[5130]', '0'),
  ('itemids[5136]', '0'),
  ('itemids[5142]', '0'),
  ('itemids[5118]', '0'),
  ('itemids[1]', '0'),
  ('display[real]', '1'),
  ('decimals', '2'),
  ('separator', 'comma'),
  ('submitbutton', 'Download'),
]


courses={'course_AL_PURE':
            {'id':'15','groups':{
                'ma2022':'75238',
                'ma2123':'99166'
            }},
        'course_AS_PURE':
            {'id':'2','groups':{
                'ma2022':'75237',
                'ma2123':'98733'
            }}
        }

# gets the course info from the relevant csv and converts into dataframe
def get_course_info(course_name):
    topics =pd.read_csv('{}.csv'.format(course_name), index_col='Name')
    topics.index = topics.index.map(lambda s : s[5:])
    return topics

# returns the pair needed to add to the request to include test with this code
def get_test_pair(test_code, course_table, in_test):
    return ('itemids[{}]'.format(course_table.loc[test_code]['Button_id']), in_test)

# returns the pairs needed to add to the request to include test with this code as a list
def get_all_test_pairs(test_codes, course_table):
    test_pairs = []
    courses = dict(course_table['Button_id'])
    for course_name in courses.keys():
        if course_name in test_codes:
            test_pairs.append(get_test_pair(course_name, course_table,'1'))
        else:
            test_pairs.append(get_test_pair(course_name, course_table,'0'))
    return test_pairs

# gets the session key from the login screen. Must be a better way to do this
def get_sess_key(l):
    start = l.index("\"sesskey\":\"")
    end = l.index("\"", start+11)
    return l[start+11:end]

# returns the grades needed
def download_grades(course_name, group_name, tests_needed):

    headers = default_headers

    course_table = get_course_info(course_name)
    course_data = courses[course_name]

    data = default_data
    for test_pair in get_all_test_pairs(tests_needed, course_table):
        data.append(test_pair)

    data.append(('id',course_data['id']))
    data.append(('group',course_data['groups'][group_name]))
    grades_download = None
    with requests.Session() as s:
        l = s.post('https://my.integralmaths.org/login/index.php', data=login_data)
        data.append(('sesskey',get_sess_key(l.text)))
        grades_download = s.post('https://my.integralmaths.org/grade/export/txt/export.php', headers=headers, data=data)

    return grades_download.content
