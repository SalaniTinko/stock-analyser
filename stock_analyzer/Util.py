import requests, re
from bs4 import BeautifulSoup
from time import sleep

filter_list = ["quicklink@1.0.", "taplink@1.2.", "respond@1.4.", "selectivizr@1.0.", "nwmatcher@1.2.", "html5shiv@3.7.", "jquery.slick@1.6.", "jquery.ui@1.11.", "modernizr@3.3.", "snap.svg@0.5.", "gsap@1.19.", "scrollmagic@2.0.", "taplink@1.2.", "drupal-bootstrap-styles@0.0.", "optimizely-sdk@3.", "requirejs-bolt@2.3.", "vanilla-lazyload@8.17.", "bootstrap@4.4.", "blogs@baruch.", "13e49d785d8d4f828038b6136f3b48ba@sentry.io", "typed.js@2.0.", "lodash@4.17.", "focus-within-polyfill@5.0.", "email@address.com", "slick-carousel@1.8.", "focus-within-polyfill@5.0.", "example@domain.com", ".edges@filterempty.", "vmlkzw86bnl0oi8vdmlkzw8vnzvhyta0owutmgzhms01ntdhltk3mzytyzzmngmxmmvhn2yz.timestags@filterempty.", "u002f7e7af50d16da41fea6264c00f270dbdc@sentry.io", "u002fshimport@1.0.1.js", ".timestags@filterempty.", "shimport@1.0.1.js", "wixofday@wix.com", "lodash@4.17.", "@sentry.wixpress.com", "focus-within-polyfill@5.0.", "core-js-bundle@3.2.", "fontawesome-free@5.13.", ".png", ".jpg", "@apple.com", "@example.com", "@amazon.com", "@err.abtm.io", "your@email.com"]

def getFilterList():
    return filter_list

def emailExtractor(url_base):
    emails = []
    urls = [url_base, url_base + "/contact/", url_base + "/contact-us/"]
    for url in urls:
        try:
            with requests.get(url, stream=True) as response:

                regex = re.compile(r'[a-z0-9.+-]+(@|\s*\[\s*at\s*\]\s*)[a-za-z0-9._-]+(\.|\s*\[\s*dot\s*\]\s*)[a-z]*',
                                   flags=re.IGNORECASE)

                sleep(0.5)

                for m in regex.finditer(response.text):
                    emails.append(m.group(0))

                content = response.content
                soup = BeautifulSoup(content, 'html.parser')
                mailtos = soup.select('a[href^=mailto]')
                for i in mailtos:
                    href = i['href']
                    try:
                        str1, str2 = href.split(':')
                    except ValueError:
                        break

                    emails.append(str2)

            return emails
        except:
            return False