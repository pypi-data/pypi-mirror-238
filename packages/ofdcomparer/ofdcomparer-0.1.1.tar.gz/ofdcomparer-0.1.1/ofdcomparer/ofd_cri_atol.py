import logging
import requests
import time

from ofdcomparer.helpers import convert_receipt_format, convert_fn_format


def get_fd_from_cri_ofd(reg_number: str, fn: str, fd_number: int, timeout: int = 180):
    """
    Получение ФД от CRI-OFD-ATOL
    """
    logging.debug(f"get_fd_from_taxcom() < fn_number {fn}, fd {fd_number}")
    if fn is None:
        logging.debug(f"get_fd_from_ofd() > None")
        return None
    headers = {"Content-Type": "application/json"}
    data = {"reg_number": reg_number, "fn": fn, "fd_number": fd_number}

    # http://127.0.0.1:50010/get_fd
    # http://cri-ofd.atol.ru:50010/get_fd
    url = 'http://cri-ofd.atol.ru:50010/get_fd'

    response = requests.get(url, headers=headers, params=data, allow_redirects=True)
    fd_cri_ofd = None
    logging.debug(f"headers: {headers} \ndata: {data}")
    try:
        start_time = time.time()
        while not time.time() - start_time > timeout:
            response = requests.get(url, headers=headers, params=data, allow_redirects=True)
            logging.info(f"cri request {url},{headers} {data}")
            logging.info("response: %s", response)
            time.sleep(1)
            if response.status_code == 200:
                fd_cri_ofd = response.json()

                logging.info('fd_cri_ofd')
                logging.info(fd_cri_ofd)
                logging.info('convert_receipt_format(fd_cri_ofd)[0]')
                logging.info(convert_receipt_format(fd_cri_ofd)[0])

                fn_format_doc = convert_fn_format(convert_receipt_format(fd_cri_ofd)[0])
                logging.info('fn_format_doc')
                logging.info(fn_format_doc)
                #fn_sorted_doc = json.loads(json.dumps(fn_format_doc, ensure_ascii=False, sort_keys=True))
                #print(1122, type(fn_sorted_doc))
                print(112233, type(fn_format_doc))
                return fn_format_doc
    except requests.exceptions.RequestException as e:
        raise Exception(f'[ERROR] with get fd from ofd: {e}')
