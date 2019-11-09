import requests
import json
import matplotlib.pyplot as plt

year = '2019'
month = '11'
day = '01'
after_m_time = year + '-' + month + '-' + day
before_m_time = year + '-' + month + '-' + '30'
start_url = 'http://172.16.1.12:8080/changes/?q=status:merged+after:' + after_m_time + '+' + 'before:' + before_m_time
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    'Cookie': 'GerritAccount=aGCupgBN4-0khFZPSVgEvWO.-xBEezi',
    'Connection': 'keep-alive'
}

info_dict = {}


def get_page(start_url):
    response = requests.get(start_url, headers=headers)
    # print(response.text)
    try:
        global info_dict
        dic = response.text.replace(')]}\'', '')
        res = json.loads(dic)
        for li in res:
            # print('owner:###', li['owner'], 'change_id:###', li['change_id'], 'branch:###', li['branch'], 'project:###',
            #      li['project'])
            if li['owner']['name'] not in info_dict:
                info_dict[li['owner']['name']] = 1
            else:
                info_dict[li['owner']['name']] = info_dict[li['owner']['name']] + 1
        print(info_dict)
    except TypeError:
        print("Type Error!!!")


def show_chart():
    labels = []
    sizes = []
    for dic in info_dict:
        labels.append(dic)
        sizes.append(info_dict[dic])
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False)
    plt.show()


if __name__ == '__main__':
    print(start_url)
    get_page(start_url)
    show_chart()
