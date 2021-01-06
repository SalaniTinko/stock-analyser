import requests, csv, tweepy, Util as u, Config as config
from urllib.parse import urlparse

api_key = config.api_key
api_secret = config.api_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

query = input("Query: ")
avoid = input("Exclude results without email? (Y/N): ")
save = True

account_count = 0
ids = []

filter_list = u.getFilterList()

keywords = query.split(",")

if avoid == "y" or avoid == "Y":
    avoid = True
    print(avoid)

for keyword in keywords:
    accounts = tweepy.Cursor(api.search_users, keyword).pages(51)
    keyword = keyword.lstrip()

    for page in accounts:
        for account in page:
            id = account.id_str
            emails = []
            new_emails = []

            if id not in ids:
                screen_name = account.screen_name

                try:
                    r = requests.get(account.url)
                    new_url = r.url
                    url = "https://" + urlparse(new_url).netloc

                    try:
                        emails = u.emailExtractor(url)
                        validity = True

                        for email in emails:
                            email = str(email).replace("thello", "hello").replace("tsupport", "support").replace(
                                "tinfo", "info")

                            for word in filter_list:
                                if word in email:
                                    validity = False

                            if validity:
                                email = email.lower()
                                new_emails.append(email)

                        new_emails = list(dict.fromkeys(new_emails))

                    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                        print("(" + keyword + " #" + str(
                            account_count) + "): " + id + " | " + screen_name + " | " + url)
                        continue

                    account_count += 1

                    with open("Contacts.csv", "a", newline='') as contacts:
                        writer = csv.writer(contacts, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                        if len(new_emails) > 0:
                            print("(" + keyword + " #" + str(
                                account_count) + "): " + id + " | " + screen_name + " | " + url + " | " + str(
                                new_emails))

                            for email in new_emails:
                                writer.writerow([id, screen_name, url, email])
                        else:
                            if not avoid:
                                print("(" + keyword + " #" + str(
                                    account_count) + "): " + id + " | " + screen_name + " | " + url + " | (/)")

                                writer.writerow([id, screen_name, url, "-"])

                        ids.append(id)

                except:
                    url = "(/)"
