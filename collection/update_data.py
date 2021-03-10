from collection.models import *
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from lxml.html import fromstring
import datetime


def data_save():
    links = ['https://www.chittorgarh.com/ipo/ipo_list.asp?a=mainline',
             'https://www.chittorgarh.com/ipo/ipo_list.asp?a=sme']
    categories = ['MAINBOARD', 'SME']
    print("updating....")
    for l in range(len(links)):
        url = urls(links[l])
        for i in range(3, len(url)):
            scraped_data = scraping(url[i])
            dfs = scraped_data[0]
            title = scraped_data[1]
            try:
                ipo_details = IpoDetails.objects.get(name=title)
            except:
                ipo_details = None

            if (ipo_details is not None):
                pk = ipo_details.pk
            else:
                pk = None
            if 'Particulars' in dfs[1].keys():
                ipo_details = details(dfs[2], title, categories[l], pk)
            else:
                ipo_details = details(dfs[1], title, categories[l], pk)

            for df in dfs:
                if 'Particulars' in df.keys():
                    asset(df, ipo_details)

                if 'IPO Subscription' in df.keys():
                    subscription(df, ipo_details)
                    scraping_share = scraping(url_change(url[i], 'ipo_subscription'))
                    share_data(scraping_share[0], ipo_details)

                field = fields(df)
                if field[0][1] == 'IPO Close Date' and list(df.keys()) == [0, 1]:
                    tentative(df, ipo_details)
            allotment_data(url[i], ipo_details)


def details(df, title, category, pk):
    field = fields(df)
    if (pk == None):
        ipo_details = IpoDetails.objects.create()
    else:
        ipo_details = IpoDetails.objects.get(pk=pk)

    ipo_details.name = title
    ipo_details.content = "There are many variations of passages of Lorem Ipsum available, but the majority have " \
                          "suffered alteration in some form, by injected humour, or randomised words which don't look " \
                          "even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be " \
                          "sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum " \
                          "generators on the Internet tend to repeat predefined chunks as necessary, making this the " \
                          "first true generator on the Internet. It uses a dictionary of over 200 Latin words, " \
                          "combined with a handful of model sentence structures, to generate Lorem Ipsum which looks " \
                          "reasonable. The generated Lorem Ipsum is therefore always free from repetition, " \
                          "injected humour, or non-characteristic words etc. "
    ipo_details.open = parsedate(field[1][0])
    ipo_details.close = parsedate(field[1][1])
    ipo_details.type = field[1][2]
    ipo_details.face_value = field[1][3]
    ipo_details.ipo_price = field[1][4]
    ipo_details.market_lot = field[1][5]
    ipo_details.listing_at = field[1][7]
    ipo_details.issue_size = field[1][8]
    ipo_details.category = category
    ipo_details.save()
    return ipo_details


def tentative(df, ipo_details):
    try:
        tentative_date = TentativeDate.objects.get(tentative_id=ipo_details)
    except:
        tentative_date = None
    if tentative_date is None:
        tentative_date = TentativeDate(tentative_id=ipo_details)
    field = fields(df)
    tentative_date.basic_of_allotment = parsedate(field[1][0])
    tentative_date.initiation_date = parsedate(field[1][1])
    tentative_date.credit_date = parsedate(field[1][2])
    tentative_date.listing_date = parsedate(field[1][3])
    tentative_date.save()


def asset(df, ipo_details):
    field = fields(df)
    for i in range(2, len(field) - 1):
        try:
            asset_data = Asset.objects.get(asset_id=ipo_details)
        except:
            asset_data = None

        if asset_data is None:
            asset_data = Asset(asset_id=ipo_details)
        asset_data.date = field[i][0]
        asset_data.total_asset = field[i][1]
        asset_data.total_revenue = field[i][2]
        asset_data.profit = field[i][3]
        asset_data.save()


def subscription(df, ipo_details):
    output = {}
    field = fields(df)
    for i in range(len(field[1])):
        output[field[0][i]] = field[1][i]

    # ipo_details = IpoDetails.objects.last()
    try:
        subscription_data = IpoSubscription.objects.get(sub_id=ipo_details)
    except:
        subscription_data = None
    if subscription_data is None:
        subscription_data = IpoSubscription(sub_id=ipo_details)

    if 'QIB' in output.keys():
        subscription_data.qib_sub = output['QIB']
    if 'NII' in output.keys():
        subscription_data.nii_sub = output['NII']
    subscription_data.total_sub = output['Total']
    if 'RII' in output.keys():
        subscription_data.retail_sub = output['RII']
    if 'Employee' in output.keys():
        subscription_data.employee = output['Employee']
    if 'Others' in output.keys():
        subscription_data.other = output['Others']
    subscription_data.save()


def share_data(df, ipo_details):
    output = {}
    try:
        field = fields(df[3])
    except:
        field = None
    if field is not None:
        for i in range(len(field[1])):
            output[field[0][i]] = field[1][i]

        # ipo_details = IpoDetails.objects.last()
        try:
            share_offer = ShareOffered.objects.get(share_id=ipo_details)
        except:
            share_offer = None

        if share_offer is None:
            share_offer = ShareOffered(share_id=ipo_details)
        if 'NII' in output.keys():
            share_offer.nii_share = output['NII']
        if 'QIB' in output.keys():
            share_offer.qib_share = output['QIB']
        if 'Retail' in output.keys():
            share_offer.retail_share = output['Retail']
        share_offer.total_share = output['Total']
        share_offer.save()


def allotment_data(url, ipo_details):
    link = allotment_link(url_change(url, 'ipo_allotment_status'))
    try:
        allotment = Allotment.objects.get(allotment_id=ipo_details)
    except:
        allotment = None

    if allotment is None:
        allotment = Allotment(allotment_id=ipo_details)
    if link is None:
        allotment.status = 'Not available'
    allotment.link = link
    allotment.save()


def parsedate(date):
    if str(date) == 'nan':
        return None
    return datetime.datetime.strptime(date, '%b %d, %Y')


def urls(url):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    req = Request(url, headers=header)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")
    table = soup.find('table', 'table table-bordered table-striped table-condensed')
    links = []
    for link in table.findAll('a'):
        links.append(link.get('href'))
    return links


def scraping(url):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    tree = fromstring(r.content)
    dfs = pd.read_html(r.text)
    title = tree.findtext('.//title')
    title1 = ""
    for i in range(len(title.split(',')[0].split(' ')) - 1):
        title1 = title1 + title.split(',')[0].split(' ')[i] + " "
    return [dfs, title1]


def fields(df):
    dict_tentative = df.to_dict()
    lst = []
    for i in dict_tentative.values():
        lst.append(list(i.values()))
    return lst


def url_change(url, change):
    lst = url.split("/")
    new_list = [change if x == 'ipo' else x for x in lst]
    separator = '/'
    new_url = separator.join(new_list)
    return new_url


def allotment_link(url):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    req = Request(url, headers=header)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")
    link = soup.find('a', {'class': 'btn btn-success btn-lg'})
    if link is not None:
        return link.get('href')
    return None
