import requests
import parsel
import re


def parse(html):
    '''
    Parse form data including the entry ID, page history, and some token
    thingies
    '''
    sel = parsel.Selector(html)
    inputs = sel.css('input[type=hidden]')

    entry_re = re.compile(r'entry\.(.*)_')
    entry = int(entry_re.search(inputs[0].get()).group(1))

    data = {'entry': entry}
    for inp in inputs:
        v = inp.attrib.get('value', '')
        data[inp.attrib['name']] = v

    return data


def find_path(goal_page, page_to_options):
    '''
    Greedy search from `goal_page` back to the first page. This should work
    because there should only be one path between these two pages.
    '''
    page = goal_page
    path = []

    def find_option(po):
        for option, p in enumerate(po):
            if p == page:
                return option
        return None

    while page != 0:
        for p, po in page_to_options.items():
            option = find_option(po)
            if option:
                path.append(option)
                page = p
                break

    return path[::-1]


url = \
    'https://docs.google.com/forms/d/e/' \
    '1FAIpQLSe7sOTLHmGjmUY3iE6E7QLqeYAZDfQXsiJrz8r-ZcA_4cXNFQ/formResponse'

# HTML class used by multiple-choice questions.
# Used to detect whether a page contains more options or if we're at a terminal
# page.
choices_class = 'freebirdFormviewerComponentsQuestionRadioChoicesContainer'

res = requests.get(url)
page_form = parse(res.text)

# What are the options on each page and where do they lead to?
# The explored graph is stored in here.
page_to_options = {}
pages_forms = {0: page_form}  # Form data need to send a request
pages_todo = {0}  # Unexplored pages

# From `FB_PUBLIC_LOAD_DATA_`, we kind of see the structure of the form.
# - There is a page that will ask for a password (which we found)
# - After that page is probably the 'congrats' page showing the flag format:
#   `pbctf{<digits you got along the way>_<password>}`
password = 's3cuR3_p1n_id_2_3v3ry0ne'

# Simple graph search (pick a element from unexplored set, add children to
# unexplored set, repeat)
while len(pages_todo) > 0:
    page = pages_todo.pop()

    data = pages_forms[page]
    entry_name = 'entry.' + str(data['entry'])
    # 'entry' is it for ourselves to remember what the ID is. It shouldn't
    # really be sent along with the form, so we'll just delete it now
    del data['entry']
    data['continue'] = '1'

    # What page does each option lead to?
    options = [0] * 10

    # `page_to_options` is used to keep track of which pages we've already
    # visited, so setting an empty value here will mark the page as visited for
    # now. This deals with pages with options leading back to itself.
    page_to_options[page] = {}

    print('Doing page {}: '.format(page))

    # Check all possible options
    for option in range(10):
        data[entry_name] = str(option)
        res = requests.post(url, data=data)

        if choices_class in res.text:
            # This page contains options, so let's parse it
            res_data = parse(res.text)

            # Figure out what the page number is (update `page_to_options`)
            page_history = res_data['pageHistory'].split(',')
            last_page = int(page_history[-1])
            options[option] = last_page
            print(str(last_page).rjust(2), end=' ', flush=True)

            # Save the form data so we can explore it later
            if last_page not in pages_forms:
                pages_forms[last_page] = res_data

            # Add it to unexplored set
            if last_page not in page_to_options:
                pages_todo.add(last_page)
        else:
            # This page doesn't have choices, so it must be the page that asks
            # for a password. We already know the password
            # `FB_PUBLIC_LOAD_DATA_` so we're done here
            path = find_path(page, page_to_options)
            path.append(option)
            print('Pin:', path)

            path = [str(x) for x in path]
            pin = ''.join(path)
            flag = 'pbctf{{{}_{}}}'.format(pin, password)
            print('Flag:', flag)

            exit(0)

    page_to_options[page] = options
    print()
