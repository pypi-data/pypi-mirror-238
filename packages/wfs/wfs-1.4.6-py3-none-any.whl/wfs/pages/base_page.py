from cdxg.logging import log
from selenium.common import StaleElementReferenceException
from wfs.utils.common import getcheckorder, get_check_list, check_word_order, get_action_dict
from wfs.utils.assertions import Assertion
from selenium.webdriver.common.keys import Keys
import traceback, time, re


def get_type_key(lpage, item, keyitem, gready):
    try:
        if item in ['type', 'upload']:
            if item == 'type':
                lpage.locators_ready(greadyx=gready).clear()
            lpage.locators_ready(greadyx=gready).send_keys(keyitem)
            log.info('Enter data as : ' + str(keyitem))
            return 'Enter data as : ' + str(keyitem)
    except Exception as e:
        traceback.print_exc()
        return 'Error ' + str(e)


def get_updown(lpage, item, keyitem, gready):
    try:
        if item == 'upload':
            if ',' in keyitem:
                keyitem = str(keyitem).split(',')
            else:
                keyitem = [keyitem]
            lpage.upload_file_data()
            time.sleep(2)
            # gready = gready[0], gready[1], 'click', gready[3]
            for xfile in keyitem:
                get_type_key(lpage, item, xfile, gready)
                log.info('File uploaded from the path ' + str(xfile))
            return 'Given or list of files uploaded from the path ' + str(keyitem)
    except Exception as e:
        traceback.print_exc()
        return 'Error ' + str(e)


def get_dom_attribute(lpage, item, case, testcase, aresults, exresults, stepline, gready, gtitems, testitem):
    try:
        if item == 'attrib':
            if testitem == '***':
                atx1, atx2 = aresults.split('@')
            else:
                atx1, atx2 = testitem.split('@')
            getattribx = atx1.lower()
            get_attrib = lpage.locators_ready(greadyx=gready).get_attribute(getattribx)
            if get_attrib == atx2:
                if testitem == '***':
                    Assertion().assert_equals_results(case, testcase, get_attrib, atx2, exresults, stepline, gtitems)
                    return 'YES'
                else:
                    return 'Attribute ' + str(getattribx) + ' named with ' + str(atx2) + ' is displayed'
            else:
                return 'Error : No attribute or text available'
    except Exception as e:
        return 'Error ' + str(e)


def get_click(lpage, item, gready):
    if item == 'click':
        try:
            # print(lpage.locators_ready())
            lpage.locators_ready(greadyx=gready).click()
            log.info('1. Button or Clickable item get Clicked')
            return 'Button1 clicked'
        except Exception as e:
            getclicked = lpage.clickable_element(gready)
            if getclicked == 'YY':
                log.info('2. Button or Clickable item get Clicked')
                return 'Button2 clicked'
            else:
                return 'Error ' + str(e)


def get_text(lpage, item, felement, aresults, case, testcase, exresults, stepline, gitems, gready,
             testitem, ptname, gcount=None):
    global gttext
    try:
        gtt = None
        lref = 'N'
        gettxt = []
        if item == 'text':
            timeout_start = time.time()
            timeout = 2 * 5
            progress_net = None
            while not progress_net:
                delta = time.time() - timeout_start
                if 'Frame_' in gitems:
                    getnavg = lpage.element_in_frames()
                    # print(getnavg)
                else:
                    getnavg = lpage.locators_ready(greadyx=gready)
                if testitem == '***':
                    gttext = aresults
                else:
                    if str(testitem).startswith('>>'):
                        testitem = get_ordering_table(lpage, item, gready, aresults, testitem)
                    gttext = testitem
                if felement == 'S':
                    if getnavg.is_displayed():
                        gtt = lpage.locators_ready(greadyx=gready, textn=gttext)
                        progress_net = 'Done'
                        # gtt = getnavg.text
                    lref = 'Y'
                else:
                    for xnavigation in range(0, len(getnavg)):
                        try:
                            if getnavg[xnavigation].is_displayed():
                                if getnavg[xnavigation].text == gttext:
                                    gtt = getnavg[xnavigation].text
                                    if 'Loading...' not in gtt:
                                        lref = 'Y'
                                        progress_net = 'Done'
                                        break
                                else:
                                    gettxt.append(getnavg[xnavigation].text)
                                    gtt = gettxt
                                    if 'Loading...' not in gtt:
                                        lref = 'YY'
                                        xnavigation = xnavigation + 1
                                        # print(xnavigation)
                                        if ptname is None:
                                            if xnavigation >= len(getnavg):
                                                progress_net = 'Done'
                                                break
                        except StaleElementReferenceException:
                            progress_net = None
                if progress_net == 'Done':
                    progress_net = 'Success'
                if delta >= timeout:
                    break

            if 'Frame_' in gitems:
                lpage.back_to_default()

            if lref == 'Y':
                # print(testitem, lref)
                if testitem == '***':
                    log.info('Given Text : ' + str(gtt) + ' displayed on Page')
                    Assertion().assert_equals_results(case=case, testcase=testcase, gtext=gtt,
                                                      aresults=aresults,
                                                      exresults=exresults, stepline=stepline, gtitems=testitem)
                    return 'YES'
                else:
                    if ptname:
                        gtt = set(gtt)
                    if testitem in gtt or gtt == testitem:
                        log.info('Given Text : ' + str(gtt) + ' displayed on Page')
                        return 'Given Text data (' + str(gtt) + ') is available in Page'
                    else:
                        return 'Error : Given Text : ' + str(gtt) + ' not available in Page'
            else:
                log.info('List of Texts : ' + str(gtt) + ' displayed')
                aresultsitem = gttext if testitem == '***' else testitem
                print(aresultsitem, gcount)
                if gcount is None:
                    is_valid, aresults, vxdata = getcheckorder(order_list=gtt, expected_order=aresultsitem)
                else:
                    is_valid = lpage.all_texts_page(getcount=gcount, gxcount=gtt)
                    gtt = is_valid

                if 'N' in is_valid:
                    if ptname:
                        gtt = set(gtt)
                    return 'Error : In order Sequence -->' + str(is_valid) + ' / Items missing --> ' + str(vxdata)
                else:
                    if testitem == '***':
                        if gtt == aresults:
                            log.info('Test data list is Equal....')
                            Assertion().assert_equals_results(case=case, testcase=testcase, gtext=gtt,
                                                              aresults=aresults,
                                                              exresults=exresults, stepline=stepline, gtitems=testitem)
                        else:
                            log.info('List is not Equal, but given test data are in list..')
                            Assertion().assert_in_results(case=case, testcase=testcase, gtext=gtt, aresults=aresults,
                                                          exresults=exresults, stepline=stepline, gtitems=testitem)
                        return 'YES'
                    else:
                        return 'List/Order of Texts data are displayed : ' + str(testitem)
    except Exception as e:
        print(traceback.print_exc())
        return 'Error :' + str(e)


def get_label(lpage, item, testitem, aresults, gcount):
    try:
        if item == 'label':
            xt = []
            timeout_start = time.time()
            timeout = 2 * 5
            progress_net = None
            while not progress_net:
                delta = time.time() - timeout_start
                getall_labels = lpage.all_texts_page(gcount)
                gettext = aresults if testitem == '***' else testitem
                if ',' in gettext:
                    gettext = str(gettext).split(',')
                    for xtext in gettext:
                        if xtext in getall_labels:
                            xt.append(xtext)
                            progress_net = 'Done'
                        else:
                            xt = 'Error : label -->' + str(gettext) + ' is missing'
                            progress_net = None
                else:
                    if gettext in getall_labels:
                        xt = gettext
                        progress_net = 'Done'
                    else:
                        xt = 'Error : label -->' + str(gettext) + ' is missing'
                        progress_net = None
                if progress_net == 'Done':
                    progress_net = 'Success'
                if delta >= timeout:
                    break
            log.info(xt)
            if 'Error' not in xt:
                if testitem == '***':
                    return 'YES'
                else:
                    return f"Given label(s) {xt} Available"
            else:
                return xt
    except Exception as e:
        traceback.print_exc()
        return 'Error :' + str(e)


def get_link_text(lpage, item, testitem, felement, gready):
    try:
        if item == 'link_text':
            timeout_start = time.time()
            timeout = 2 * 5
            progress_net = None
            while not progress_net:
                delta = time.time() - timeout_start
                getnavigation = lpage.locators_ready(greadyx=gready)
                if felement == 'S':
                    if getnavigation.is_displayed():
                        if getnavigation.text == testitem:
                            getnavigation.click()
                            progress_net = 'Done'
                            log.info('1.Link_text or Clickable item get Clicked')
                            time.sleep(1)
                else:
                    for xnavigation in getnavigation:
                        if xnavigation.is_displayed():
                            log.info(xnavigation.text)
                            if xnavigation.text == testitem:
                                xnavigation.click()
                                log.info('2.Link_text or Clickable item get Clicked')
                                time.sleep(1)
                                progress_net = 'Done'
                                break
                if progress_net == 'Done':
                    progress_net = 'Success'
                if delta >= timeout:
                    break
            return 'Link Item get Clicked'
    except Exception as e:
        return 'Error ' + str(e)


def get_page_title(lpage, item, case, testcase, aresults, exresults, stepline, gready, gtitems):
    global rTitle
    yx = 'NO'
    try:
        if item == 'title':
            rTitle = lpage.get_title
            yx = 'YES'
        if item == 'row':
            gdx = get_ordering_table(lpage, item, gready)
            rTitle = int(gdx) - 1
            if type(aresults) == list:
                aresults = [int(num) for num in aresults]
            yx = 'YES'

        if item in ['asc', 'desc']:
            aresults, rTitle = get_ordering_table(lpage, item, gready)
            yx = 'YES'

        if yx == 'YES':
            Assertion().assert_equals_results(case, testcase, rTitle, aresults, exresults, stepline, gtitems)
            return yx
    except Exception as e:
        print(traceback.print_exc())
        return 'Error ' + str(e)


def get_select_item(lpage, item, keyitem, gready):
    try:
        if item == 'option':
            opts = lpage.locators_ready(greadyx=gready)
            matched = False
            for opt in opts:
                if keyitem == opt.text:
                    opt.click()
                    matched = True
                    break
            if not matched:
                # raise NoSuchElementException("Could not locate element with visible text: %s" % keyitem)
                return 'Error : ' + str(keyitem) + ' Not Match'
            else:
                return str(keyitem) + ' is Matched'
    except Exception as e:
        return 'Error ' + str(e)


def _get_longest_token(value: str) -> str:
    items = value.split(" ")
    longest = ""
    for item in items:
        if len(item) > len(longest):
            longest = item
    return longest


def get_clickable_selectable(lpage, item, gready):
    try:
        getElement = lpage.gethidden(gready)
        if item == 'click':
            getElement.click()
            return 'Item Clicked'
    except Exception as e:
        return 'Error ' + str(e)


def get_keys_press(lpage, gready, keyitem='ENTER'):
    try:
        element = lpage.locators_ready(greadyx=gready)
        actions = lpage.get_action_chains()
        if keyitem == 'ENTER':
            actions.send_keys_to_element(element, Keys.ENTER)
        actions.perform()
        return 'Key Action Performed ->' + str(keyitem)
    except Exception as e:
        return 'Error  ' + str(e)


def get_check(lpage, item, gready):
    if item == 'check':
        return lpage.get_elements(greadyx=gready)


def long_press(lpage, gready):
    element = lpage.locators_ready(greadyx=gready)
    actions = lpage.get_touch_actions()
    actions.long_press(element).perform()


def mouse_actions(lpage, item, gready):
    if item == 'hover':
        element = lpage.locators_ready(greadyx=gready)
        actions = lpage.get_action_chains()
        actions.move_to_element(element).click().perform()
        return 'Mouse over to element -> clicked'
    else:
        return scrollpage(lpage, item, gready)


def scrollpage(lpage, item, gready):
    if item == 'scroll':
        element = lpage.locators_ready(greadyx=gready)
        try:
            actions = lpage.get_action_chains()
            # actions.scroll_to_element(element)
            lpage.getscrolled(elementx=element)
            return 'Scrolled the element'
        except Exception as e:
            return 'Error ' + str(e)


def get_common(lpage, item, gready):
    try:
        if item == 'idata' or item == 'iset':
            if str(gready[1]).startswith('SET'):
                getsetx = str(gready[1]).split('**')
                log.info(len(getsetx))
                if len(getsetx) <= 3:
                    n, gelement, btn = str(gready[1]).split('**')
                    gready = (gready[0], gelement, *gready[2:])
                    gtx = 'N'
                elif len(getsetx) == 5:
                    n, gelement, btn, idsx, indvname = str(gready[1]).split('**')
                    gready = (gready[0], gelement, *gready[2:])
                    if ',' in idsx and ',' in indvname:
                        idsx = str(idsx).split(',')
                        indvname = str(indvname).split(',')
                    gtx = 'Y'
                else:
                    n, locate, gelement, btn, idsx, indvname = str(gready[1]).split('**')
                    gready = (locate, gelement, gready[1], 'M')
                    gtx = 'Y'
            # gready = (gready[0], gelement, *gready[2:])
            element = lpage.locators_ready(greadyx=gready)
            log.info(element)
            log.info(len(element))
            if gtx == 'Y':
                elex, btnx = [], []
                for i in range(0, len(element)):
                    if btn + str(i + 1) == idsx:
                        elex.append(element[i])
                        btnx.append(indvname)
                        break
                    else:
                        for j in range(0, len(idsx)):
                            if btn + str(i + 1) == idsx[j]:
                                elex.append(element[i])
                                btnx.append(indvname[j])
                                break
                set_elements = lpage.set_attributes_values(elements=elex, attribValues=btnx, btnname=gtx)
            else:
                set_elements = lpage.set_attributes_values(elements=element, attribValues=btn)
            if set_elements:
                if len(set_elements[0]) == 1:
                    set_elements = f'Elements available -->[{set_elements[0]}]', set_elements[1]
                else:
                    set_elements = ', '.join(set_elements[0])
                    set_elements = f'Elements available -->[{set_elements}]'
            log.info(set_elements)
            return set_elements
    except Exception as e:
        traceback.print_exc()
        return 'Error  ' + str(e)


def get_ordering_table(lpage, item, gready, arst=None, titem=None):
    # Get all the rows of the table
    global expected_order
    if item == 'row':
        locator_identity, element_identity, action_item, fetchlements = 'tag', 'tr', 'page', 'M'
        gready = locator_identity, element_identity, action_item, fetchlements
        rows = lpage.locators_ready(greadyx=gready)
        return len(rows)

    if item in ['asc', 'desc']:
        extracted_order = []
        cells = lpage.locators_ready(gready)
        extracted_order = [cell.text for cell in cells]
        if item == 'asc':
            expected_order = sorted(extracted_order, key=lambda x: x.lower())
        if item == 'desc':
            expected_order = sorted(extracted_order, key=lambda x: x.lower(), reverse=True)
        log.info(expected_order)
        log.info(extracted_order)
        return expected_order, extracted_order

    if item == 'text':
        # extracted_order = []
        cells = lpage.locators_ready(gready)  # row.find_elements(By.TAG_NAME, "td")
        extracted_order = [cell.text for cell in cells]
        abc = extracted_order
        g_arst = arst if titem == '***' else titem
        getrxt = str(g_arst).split('>>')[1]
        def_value = getrxt.split(',')  # Example list with additional strings
        is_valid = all(any(element == def_val for def_val in def_value) for element in abc)
        if is_valid:
            return extracted_order
        else:
            return 'No Extracted Data Not Matched'


def get_html_source(lpage, item, gready, gtestitem, aresults, refkey=0):
    #if ('{' in gready[1] or '}' in gready[1]) and ('*' not in gready[1]):
    pattern = r'[{*](.*?)[}*]'
    match = re.findall(pattern, gready[1])

    matches=[]
    for matchx in match:
        matches.append(matchx)
    get_order = check_word_order(gready[1])
    action, daction, felem = get_action_dict(get_order)
    actionlist = {'find': 1, 'click': 1, 'enter': 2, 'Find': 1, 'Click': 1, 'Enter': 2, 'findandenter': 3,
                  'clickandenter': 3, 'findandclick': 4, 'select': 5, 'findandselect': 6, 'selectoption': 1,
                  'selecttext': 1}
    getsource = lpage.get_source_xpath(greadyx=gready, textmatch=matches, refkey=actionlist[daction], action=action,
                                       felem=felem)
    return getsource, gtestitem