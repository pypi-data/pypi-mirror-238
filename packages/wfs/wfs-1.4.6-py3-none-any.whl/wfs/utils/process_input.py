from wfs.pages.app_page import *
from wfs.pages.base_page import *
from configparser import ConfigParser
from pathlib import Path

mypath = Path.cwd()
data_file_path = mypath / "conf.ini"
cObject = ConfigParser()
cObject.read(data_file_path)


def process_url():
    return 'Navigated to url ' + cObject.get('Url', 'base_url')


def process_xurl(lpage):
    return 'Navigated to url ' + lpage.get_current_url()


def process_type_uploadx(lpage, gAitem, gTestitem, gready):
    return get_type_key(lpage=lpage, item=gAitem, keyitem=gTestitem, gready=gready)


def process_upload_download(lpage, gAitem, gTestitem, gready):
    return get_updown(lpage=lpage, item=gAitem, keyitem=gTestitem, gready=gready)


def process_click(lpage, gAitem, gready):
    return get_click(lpage=lpage, item=gAitem, gready=gready)


def process_link_text(lpage, gAitem, gFelements, gready, gTestitem):
    return get_link_text(lpage=lpage, item=gAitem, testitem=gTestitem, felement=gFelements, gready=gready)


def process_text(lpage, gAitem, gFelements, aresults, case, testcase, exresults, linex, gItems, gready, gTestitem,
                 ptname, gcount):
    return get_text(lpage=lpage, item=gAitem, felement=gFelements, aresults=aresults, case=case,
                    testcase=testcase, exresults=exresults, stepline=linex, gitems=gItems, gready=gready,
                    testitem=gTestitem, ptname=ptname, gcount=gcount),


def process_misc(lpage, gAitem, aresults, case, testcase, exresults, linex, gtitems, gready):
    return get_page_title(lpage=lpage, item=gAitem, case=case, testcase=testcase, aresults=aresults,
                          exresults=exresults, stepline=linex, gready=gready, gtitems=gtitems)


def process_option(lpage, gAitem, gTestitem, gready):
    return get_select_item(lpage=lpage, item=gAitem, keyitem=gTestitem, gready=gready)


def process_attribure(lpage, gAitem, aresults, case, testcase, exresults, linex, gready, gTestitem, gtitems):
    return get_dom_attribute(lpage=lpage, item=gAitem, case=case, testcase=testcase, aresults=aresults,
                             exresults=exresults, stepline=linex, gready=gready, gtitems=gtitems,
                             testitem=gTestitem)


def process_label(lpage, gAitem, aresults, gTestitem, gcount):
    return get_label(lpage=lpage, item=gAitem, testitem=gTestitem, aresults=aresults, gcount=gcount)


def process_keys(lpage, gTestitem, gready):
    return get_keys_press(lpage=lpage, gready=gready, keyitem=gTestitem)


def process_hover_scroll(lpage, gAitem, gready):
    return mouse_actions(lpage=lpage, item=gAitem, gready=gready)


def process_idata(lpage, gAitem, gready):
    get_common(lpage=lpage, item=gAitem, gready=gready)


def process_check(lpage, gAitem, gready):
    get_check(lpage=lpage, item=gAitem, gready=gready)


def process_swipe_up_down(lpage, gAitem):
    return get_tap_swipe(lpage=lpage, item=gAitem, ax=None, ay=None)


def process_dall(lpage, gAitem, greadyx, gTestitem):
    # 'atype', 'kshown', 'hkboard', 'home', 'back', 'size'
    return get_key_text(lpage=lpage, item=gAitem, ktext=gTestitem)


def process_atext_aclick(lpage, gAitem, greadyx, gTestitem, ptname):
    if ptname == 'Android':
        return getAndroid(lpage=lpage, item=gAitem, greadyx=greadyx, desc=gTestitem)
    elif ptname == 'iOS':
        return getiOS(lpage=lpage, item=gAitem, greadyx=greadyx, desc=gTestitem)


def process_source(lpage, gAitem, gready, gTestitem, aresults):
    return get_html_source(lpage, gAitem, gready, gTestitem, aresults)
