import inspect
import traceback
from wfs.utils.process_input import process_url, process_xurl, process_type_uploadx, process_upload_download, process_click, \
    process_text, process_link_text, process_misc, process_attribure, process_keys, process_label, process_hover_scroll, \
    process_idata, process_check, process_swipe_up_down, process_dall, process_atext_aclick, process_source, process_option

web_conditions = {
    'url': process_url,
    'xurl': process_xurl,
    'type': process_type_uploadx,
    'uploadx': process_type_uploadx,
    'upload': process_upload_download,
    'download': process_upload_download,
    'click': process_click,
    'text': process_text,
    'link_text': process_link_text,
    'title': process_misc,
    'row': process_misc,
    'asc': process_misc,
    'desc': process_misc,
    'attrib': process_attribure,
    'keys': process_keys,
    'label': process_label,
    'hover': process_hover_scroll,
    'scroll': process_hover_scroll,
    'idata': process_idata,
    'check': process_check,
    'option': process_option,
    'source': process_source,
}

mobile_conditions = {
    'SwipeUp': process_swipe_up_down,
    'SwipeDn': process_swipe_up_down,
    'atype': process_dall,
    'kshown': process_dall,
    'hkboard': process_dall,
    'home': process_dall,
    'back': process_dall,
    'size': process_dall,
    'atext': process_atext_aclick,
    'aclick': process_atext_aclick,
}


def process_input(testcase, lpage, gAitem, gTestitem, gFelements, linex, gRstring, aresults, exresults, case,
                  gItems, gLocator, gElementor, gAction, gtitems, gready, ptname, gcount):
    try:
        handler = web_conditions.get(gAitem)
        argspec = inspect.getfullargspec(handler)
        argument_names = argspec.args
        defaults = argspec.defaults
        # print("Argument names:", argument_names)
        # print("Defaults:", defaults)
        # print("Documentation:", handler.__doc__)
        arguments = {
            "testcase": testcase, "lpage": lpage, "gAitem": gAitem, "gTestitem": gTestitem, "gFelements": gFelements,
            "linex": linex, "gRstring": gRstring, "aresults": aresults, "exresults": exresults, "case": case,
            "gItems": gItems, "gLocator": gLocator, "gElementor": gElementor, "gAction": gAction, "gtitems": gtitems,
            "gready": gready, "ptname": ptname, "gcount": gcount
        }
        getvarib = []
        if argument_names is not []:
            for argname in argument_names:
                getvarib.append(arguments[argname])
        args = tuple(getvarib)
        if handler:
            handler = handler(*args)
            return handler[0] if type(handler) == tuple else handler
    except Exception as e:
        traceback.print_exc()
        return str(e)
