import json
import time
import traceback
from wfs.pages.base_page import get_common, get_html_source
from wfs.utils.common import extract_details
from wfs.utils.action_test_item import getextra
from wfs.utils.parseexcel import ParseExcel
from cdxg import Steps
from wfs.pages.action_step import get_test_steps
from wfs.pages.object_repo_page import object_repox
from wfs.utils.confapp import pax_session, drv_session
from wfs.utils.ui_conditions import process_input
from wfs.utils.response import apicall
from configparser import ConfigParser
from pages.uipage import UIPage_reference
from pages.appage import APPage_reference
from pathlib import Path

mypath = Path.cwd()
data_file_path = mypath / "conf.ini"
cObject = ConfigParser()
cObject.read(data_file_path)


def getdepend(test_case_data, reportpath, features, test_object_repo, test_data_json, dependdata, url, driver, ptname):
    testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case, depend = dependdata
    gtres = None

    def execute_steps(testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case, depend):
        gtresx = []
        linex = teststeps.split("\n")
        descp = adescribe.split("\n")
        tdatax = testdata.split("\n")
        # arets = aresults.split("\n")
        for steps_line in range(0, len(linex)):
            Steps(desc=ustory + ":" + linex[steps_line])
            getallx = get_test_steps(test_object_repo, test_data_json, tstepx=linex[steps_line], steps_line=steps_line,
                                     testdata=str(testdata),
                                     action=str(action), actiondesc=str(adescribe), ptname=ptname)

            def getExe(get_all):
                global lpage, ddriver, paxdriver, drvdriver
                gLocator, gElementor, gAction, gDescribe, gStepline, gAitem, gTestitem, gFelements, gItems, gRstring = get_all
                if ptname:

                    if '[Pax]' in gStepline or '[P]' in gStepline:
                        try:
                            if '[P]' in gStepline:
                                paxdriver.activate_app(app_id=cObject.get('MobileHost', str(ptname) + '_activity_pax'))
                                # paxdriver.activate_app(app_id='com.codigo.comfort')
                            else:
                                # drvdriver.background_app(-1)
                                paxdriver = pax_session(ptname, False)
                        except Exception as e:
                            paxdriver = pax_session(ptname, False)

                    if '[Drv]' in gStepline or '[D]' in gStepline:
                        try:
                            if '[D]' in gStepline:
                                drvdriver.activate_app(app_id=cObject.get('MobileHost', str(ptname) + '_activity_drv'))
                                # drvdriver.activate_app(app_id='com.codigo.cdgdriver.uat')
                            else:
                                paxdriver.background_app(-1)
                                drvdriver = drv_session(ptname, False)
                        except Exception as e:
                            drvdriver = drv_session(ptname, False)

                    if '[Pax]' in gStepline or '[P]' in gStepline:
                        lpage = object_repox(paxdriver)

                    if '[Drv]' in gStepline or '[D]' in gStepline:
                        lpage = object_repox(drvdriver)
                else:
                    if gAitem in ["url", "xurl"]:
                        if gTestitem == '***':
                            gTestitem = ''
                        driver.get(url + gTestitem)
                        driver.maximize_window()
                        lpage = object_repox(driver)
                gtitems = reportpath, features, ustory, teststeps, testdata, depend, tdatax[
                    steps_line]  # , arets[steps_line]
                if ',' in gAction:
                    gactionItems = str(gAction).split(',')
                    if gAitem in gactionItems: gAction = gAitem
                gtresults = getall_actions(testcase, lpage, gAitem, gTestitem, gFelements, linex[steps_line], gRstring,
                                           aresults, exresults, case, gItems, gLocator, gElementor, gAction, gtitems,
                                           ptname)
                return gtresults

            if getallx is not None and 'Error' not in getallx:
                for xx in range(len(getallx)):
                    get_all = getallx[xx].split("|")
                    astx = getExe(get_all)
                    gtresx.append(astx)
                    if 'Error' in gtresx and gtresx is not None:
                        break
            else:
                gtresx.append(getallx)
        return gtresx

    if depend is not None:
        gtdata = get_sheetnames_excel(test_case_data, pfix="FMS_", itemdata=depend, ustory=ustory)
        for xlen in range(0, len(gtdata)):
            testcase = gtdata[xlen][0]["Test_Case"]
            ustory = gtdata[xlen][0]["User_Story_Tcno"]
            teststeps = gtdata[xlen][0]["Test_Steps"]
            testdata = gtdata[xlen][0]["Test_data"]
            action = gtdata[xlen][0]["Seq|Object_Repo_Ref|Action"]
            adescribe = gtdata[xlen][0]["Action Description"]
            aresults = gtdata[xlen][0]["Results Validation[Automation]"]
            exresults = gtdata[xlen][0]["Expected_Results[Manual]"]
            case = gtdata[xlen][0]["Priority"]
            depend = gtdata[xlen][0]["Depend"]
            if depend is None:
                depend = 'Y'
            gtres = execute_steps(testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case,
                                  depend)
    else:
        gtres = execute_steps(testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case,
                              depend)
    try:
        api_url, getrespx = cObject.get('Xldata', 'api_target_list').split(',')
        if getrespx == 'response':
            getdatax = lpage.get_response_body_list(api_url)
        else:
            getdatax = []
            getlistdata, getheaderdata = lpage.get_endpoint_list(api_url)
            if getrespx == 'arequest':
                getheaderdata = json.loads(cObject.get('Xldata', 'xheaders'))
            for xapi in getlistdata:
                getresponse = apicall().apicall(url=xapi['currentURL'], method=xapi['method'], header=getheaderdata)
                getdatax.append(getresponse)
        fpath = mypath / 'test_data' / 'web' / 'response'
        with open(fpath / (str(ustory) + '.json'), 'w', encoding='utf-8') as jsonfile:
            getdatax = [item for item in getdatax if item is not None]
            jsonfile.write(json.dumps(getdatax, indent=4))
    except:
        pass
    print('Results : ' + str(gtres))
    return gtres


def getall_actions(testcase, lpage, gAitem, gTestitem, gFelements, linex, gRstring, aresults, exresults, case, gItems,
                   gLocator, gElementor, gAction, gtitems, ptname):
    gready = gLocator, gElementor, gAction, gFelements
    global gTx
    try:
        gTestitem, aresults, ptname, gcount = extract_details(lpage, gAitem, gready, aresults, gTestitem, ptname)
        if str(gElementor).startswith('SET') and str(gLocator) == 'id_':
            gelmsg, gElementor = get_common(lpage=lpage, item='iset', gready=gready)
            gready = (gready[0], gElementor, *gready[2:])
        gTestitem = getextra(keyitem=gTestitem, ustory=gtitems[2], kword=str(linex).split(':')[0], rstring=gRstring,
                             ptname=ptname)

        if str(gRstring) == 'XXXX':
            gready, tdataItem = get_html_source(lpage, gAitem, gready, gTestitem, aresults)
            if gTestitem is not '***':
                gTestitem = tdataItem

        if gItems == 'addon' or 'addon' in gItems:
            if ptname:
                pgClass = APPage_reference(lpage, gready, gTestitem, aresults)
            else:
                pgClass = UIPage_reference(lpage, gready, gTestitem, aresults)
            # methd_name = 'addon_type'
            methd_name = 'addon_' + str(gAction)
            if hasattr(pgClass, methd_name):
                gTx = getattr(pgClass, methd_name)
                gTx = gTx()  # Call the method using gTx
                time.sleep(1)
        else:
            gTx = process_input(testcase, lpage, gAitem, gTestitem, gFelements, linex, gRstring, aresults, exresults,
                                case,
                                gItems, gLocator, gElementor, gAction, gtitems, gready, ptname, gcount)

        gstp = str(linex).split(':')[0]
        gTx = gstp + ':' + gTx
        return gTx
    except Exception as e:
        traceback.print_exc()
        return 'Error : ' + str(e)


def get_sheetnames_excel(test_case_data, pfix='FMS_', itemdata='NSH_001_TC01', ustory=None):
    get_excel_data, gtdata = None, []
    getxcl = ParseExcel(test_case_data)
    getallxm = getxcl.get_sheetnames()
    getdata_item = itemdata.split(',')
    getdata_item.append(ustory)
    for gdata in range(0, len(getdata_item)):
        for xallm in getallxm:
            if pfix in xallm:
                get_excel_data = ParseExcel(test_case_data).get_row_all_col_data(sheetname=xallm,
                                                                                 columnname="User_Story_Tcno",
                                                                                 pagename=getdata_item[gdata])
                if get_excel_data:
                    gtdata.append(get_excel_data)
    return gtdata
