#!/usr/bin/python
# coding=utf-8
# email:heyuhao87@gmail.com

__author__ = 'Lings'


import urllib2
import re
import alfred
import time


class DomainSearchResult(object):

    AVAILABLE = 0
    NOT_AVAILABLE = 1
    PARAMETER_ERROR = 2
    SEARCH_ERROR = -1


def domainsearch(domain):

    ''' Search domain availability. '''

    url = "http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=" + domain

    headers = {
        'Accept': 'text/html',
        'Accept-Encoding': 'utf-8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    }

    try:
        request = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(url=request, data=None, timeout=30)
        content = response.read()

        # returncode=200  表示接口返回成功
        # key=***.com     表示当前check的域名
        # original=210    Domain name is available     表示域名可以注册
        # original=211    Domain name is not available 表示域名已经注册
        # original=212    Domain name is invalid   表示域名参数传输错误

        # xmldoc = minidom.parseString(content)
        #
        # properties = xmldoc.getElementsByTagName("property")
        # if len(properties) > 0:
        #     property = properties[0]
        #     originals = property.getElementsByTagName("original")
        #
        #     if len(originals) > 0:
        #         original = originals[0]
        #         codestr = original.firstChild.nodeValue
        #         if len(codestr) > 3:
        #             code = int(codestr[:3])
        #
        #             if code == 210:
        #                 return DomainSearchResult.AVAILABLE
        #             elif code == 211:
        #                 return DomainSearchResult.NOT_AVAILABLE
        #             elif code == 212:
        #                 return DomainSearchResult.PARAMETER_ERROR


        strRe = re.compile(r"<original>\s*([0-9]{3})")
        codes = strRe.findall(content)
        if len(codes) > 0:
            code = int(codes[0])

            if code == 210:
                return DomainSearchResult.AVAILABLE
            elif code == 211:
                return DomainSearchResult.NOT_AVAILABLE
            elif code == 212:
                return DomainSearchResult.PARAMETER_ERROR


    except Exception, e:
        print e

    return DomainSearchResult.SEARCH_ERROR


def show_result(infos, domain, result):

    subtitle = ""
    icon = ""
    if result == DomainSearchResult.AVAILABLE:
        subtitle = "Available"
        icon = "available.png"
    elif result == DomainSearchResult.NOT_AVAILABLE:
        subtitle = "Not avaialbe"
        icon = "not_available.png"
    else:
        subtitle = "Error"
        icon = "error.png"

    info = alfred.Item(
        attributes={"domain": domain},
        title=domain,
        subtitle=subtitle,
        icon=(icon, {'type': 'png'})
    )

    infos.append(info)
    # alfred.write(alfred.xml(infos, maxresults=10))



def alfred_search(keyword, query):

    infos = []

    strings = keyword.split(".")

    # Include extension
    if len(strings) > 1:
        result = domainsearch(keyword)
        show_result(infos, keyword, result)

        alfred.write(alfred.xml(infos, maxresults=10))

        return

    # No extension
    base_exts = [".com", ".cn", ".net", ".me"]
    advanced_exts = [".org", ".tv", ".cc"]

    final_exts = base_exts
    if query == "all":
        final_exts = base_exts+advanced_exts

    for ext in final_exts:
        domain = keyword+ext
        result = domainsearch(domain)
        show_result(infos, domain, result)

    alfred.write(alfred.xml(infos, maxresults=10))




(parameter, query) = alfred.args()
keyword = parameter.strip().encode('utf-8')
query = query.strip().encode('utf-8')

alfred_search(keyword, query)

# alfred_search("heyuhao.com", None)

