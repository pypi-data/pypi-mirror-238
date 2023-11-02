import requests
import logging

# CARBON
def write(data:list[dict], batch:bool = True):
    """
    data: list[dict], example:
          [{'PLC_TAG1': 2.2}, {'PLC_TAG2': 1.2}]
    """
    api='http://jp-connector/api/write'
    try:
        if not batch:
            logging.info("reordered opc write")
            r = requests.post(api, json=data, timeout=5)
            if r.status_code != 200:
                logging.error(r.text)
                return r.text
        else:
            logging.info("batch opc write")
            errmsg = ""
            for x in data:
                r = requests.post(api, json=[x], timeout=5)
                if r.status_code != 200:
                    errmsg = r.text
            if errmsg:
                logging.error(errmsg)
                return errmsg
        logging.info(f"write opc success: {data}")
        
        return ""
    except Exception as e:
        logging.error(str(e))
        raise e