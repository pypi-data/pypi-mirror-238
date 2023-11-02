import json
import logging
import platform
import threading
import time
from ofdcomparer.dto_error_descriptions import get_dto_error_code_description
if platform.system == 'Windows':
    # toDo добавить для 32/64 или ставить через pip
    from ofdcomparer.libfptr10_win import IFptr
else:
    from ofdcomparer.libfptr10_lin import IFptr

class DTO10Helper:
    def __init__(self):

        while True:
            try:
                self.fptr = IFptr()
            except Exception:
                raise Exception("Error creating DTO 10")
            if self.fptr.interface.value is not None:
                break

        self.dto10_version = self.fptr.version().decode("cp866")

        self.ErrorCode = None
        self.ErrorDescription = None
        self.JsonAnswer = None

        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_MODEL, str(self.fptr.LIBFPTR_MODEL_ATOL_AUTO))
        self.RNM = self.get_rnm_number()
        self.FN = self.get_fn_number()

    def get_information_and_status(self):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_DATA_TYPE, self.fptr.LIBFPTR_DT_STATUS)
        self.fptr.queryData()
        self.request_error_code()
        serial_number = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_SERIAL_NUMBER)
        return serial_number

    def open(self):
        self.fptr.open()
        return self.request_error_code()

    def close(self):
        self.fptr.close()
        return self.request_error_code()

    def request_error_code(self, flag_all_kkt_settings=False):
        self.ErrorCode = self.fptr.errorCode()
        self.ErrorDescription = self.fptr.errorDescription()
        pytest_dto_error_description = get_dto_error_code_description(self.ErrorCode)
        if self.ErrorDescription != pytest_dto_error_description:
            logging.error(f"Код ошибки ДТО: {self.ErrorCode}")
            logging.error(f"ДТО [{self.ErrorDescription}] <-> "
                          f"[{pytest_dto_error_description}] const.dto_error_descriptions")
            logging.error("НЕОБХОДИМО АКТУАЛИЗИРОВАТЬ СЛОВАРЬ ALL_DTO10_ERROR_DESCRIPTIONS")
        if self.ErrorCode != self.fptr.LIBFPTR_OK:
            if flag_all_kkt_settings and self.ErrorCode == self.fptr.LIBFPTR_ERROR_NOT_SUPPORTED:
                pass
            else:
                logging.error("[ДТО]: Код ошибки: {} [{}]".format(self.ErrorCode, self.ErrorDescription))
        return self.ErrorCode

    def get_last_fiscal_document_number(self):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_FN_DATA_TYPE, self.fptr.LIBFPTR_FNDT_LAST_DOCUMENT)
        self.fptr.fnQueryData()
        self.request_error_code()
        return int(self.fptr.getParamInt(self.fptr.LIBFPTR_PARAM_DOCUMENT_NUMBER))

    def get_last_fd_number(self):
        logging.debug("get_last_fd_number()")
        try:
            json_task = {
                "type": "getFnStatus"
            }
            fn_status = self.execute_json(json_task)
            logging.debug("СТАТУС ФН: %s", fn_status)
            last_fd_number = fn_status['fnStatus']['fiscalDocumentNumber']
            logging.debug(f"get_last_fd_number() > {last_fd_number}")
            logging.info("ФД: %s", last_fd_number)
            return last_fd_number
        except Exception as e:
            logging.error("get_last_fd_number error: {}".format(e))
            logging.debug("get_last_fd_number() > None")
            return None

    def get_fd_from_fn(self, fd: int):
        """
        Извлечение ФД из ФН
        """
        logging.debug(f"get_fd_from_fn() < {fd}")
        if fd is None:
            logging.debug(f"get_fd_from_fn() > None")
            return None
        # JSON задание для чтения документа из ФН

        json_task = {
            "type": "getFnDocument",
            "fiscalDocumentNumber": int(fd),
            "withRawData": False
        }
        fd_fn = self.execute_json(json_task)
        if fd_fn is None:
            return None
        if isinstance(fd_fn, dict):
            fd_fn = fd_fn['documentTLV']
            return fd_fn
        return None

    def connect_to_kkt_by_usb(self, usb_device_path="auto"):
        logging.debug("Устанавливаем соединение с ККТ по USB...")
        self.set_connection_settings_to_usb(usb_device_path)
        if self.open() != self.fptr.LIBFPTR_OK:
            logging.error("Не удалось установить соединение с ККТ")
            return False
        if not self.is_connection_type_usb():
            return False
        logging.info("Соединение с ККТ установлено по USB")
        return True

    def connect_to_kkt_by_ethernet(self, ip="127.0.0.1", port="5555"):
        logging.debug(f"Устанавливаем соединение по ip {ip}:{port}")
        self.set_connection_settings_to_ethernet(ip, port)
        err = self.open()
        if err != self.fptr.LIBFPTR_OK:
            logging.info(f"Ошибка - не удалось установить соединение с ККТ ({err})")
            return False
        if not self.is_connection_type_ethernet():
            return False
        logging.info(f"Соединение с ККТ установлено по Ethernet. ip=[{ip}] port=[{port}]")
        return True

    def set_connection_settings_to_ethernet(self, ip, port):
        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_PORT, str(self.fptr.LIBFPTR_PORT_TCPIP))
        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_IPADDRESS, str(ip))
        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_IPPORT, str(port))
        self.fptr.applySingleSettings()
        return self.request_error_code()

    def is_connection_type_ethernet(self):
        if not self.fptr.isOpened():
            return False
        connection_type = self.fptr.getSingleSetting(self.fptr.LIBFPTR_SETTING_PORT)
        if not int(connection_type) == self.fptr.LIBFPTR_PORT_TCPIP:
            logging.error(f'Способ связи с ККТ [{connection_type}], а должен быть [Ethernet]')
            return False
        return True

    def set_connection_settings_to_usb(self, usb_device_path):
        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_PORT, str(self.fptr.LIBFPTR_PORT_USB))
        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_USB_DEVICE_PATH, str(usb_device_path))
        self.fptr.applySingleSettings()
        return self.request_error_code()

    def is_connection_type_usb(self):
        if not self.fptr.isOpened():
            return False
        connection_type = self.fptr.getSingleSetting(self.fptr.LIBFPTR_SETTING_PORT)
        self.request_error_code()
        if not int(connection_type) == self.fptr.LIBFPTR_PORT_USB:
            logging.error("Способ связи с ККТ [{}], а должен быть [USB]".format(connection_type))
            return False
        return True

    def connect_to_kkt_by_rs(self, com="COM1", baudrate=115200):
        print("Устанавливаем соединение по RS")
        if self.set_connection_settings_to_rs(com, baudrate) != self.fptr.LIBFPTR_OK:
            print("Не удалось установить настройки драйвера для подключения к ККТ")
            return False
        if self.open() != self.fptr.LIBFPTR_OK:
            print("Не удалось установить соединение с ККТ")
            return False
        if not self.is_connection_type_rs():
            return False
        print("Соединение с ККТ установлено по RS. com=[{}] baudrate=[{}]".format(com, baudrate))
        return True

    def set_connection_settings_to_rs(self, com, baudrate):
        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_MODEL, str(self.fptr.LIBFPTR_MODEL_ATOL_AUTO))
        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_PORT, str(self.fptr.LIBFPTR_PORT_COM))
        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_COM_FILE, com)
        self.fptr.setSingleSetting(self.fptr.LIBFPTR_SETTING_BAUDRATE, str(baudrate))
        self.fptr.applySingleSettings()
        return self.request_error_code()

    def is_connection_type_rs(self):
        if not self.fptr.isOpened():
            return False
        connection_type = self.fptr.getSingleSetting(self.fptr.LIBFPTR_SETTING_PORT)
        self.request_error_code()
        if not int(connection_type) == self.fptr.LIBFPTR_PORT_COM:
            logging.error("Способ связи с ККТ [{}], а должен быть [RS]".format(connection_type))
            return False
        return True

    def get_model_name(self):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_DATA_TYPE, self.fptr.LIBFPTR_DT_MODEL_INFO)
        self.fptr.queryData()
        model_name = str(self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_MODEL_NAME))
        return model_name

    def set_no_print_flag(self, no_print):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_REPORT_ELECTRONICALLY, no_print)
        return True

    def reset_settings(self):
        self.fptr.resetSettings()
        return self.request_error_code()

    def get_fatal_errors_status(self):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_DATA_TYPE, self.fptr.LIBFPTR_DT_FATAL_STATUS)
        self.fptr.queryData()

        self.request_error_code()

        no_serial_number = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_NO_SERIAL_NUMBER)
        rtc_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_RTC_FAULT)
        settings_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_SETTINGS_FAULT)
        counter_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_COUNTERS_FAULT)
        user_memory_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_USER_MEMORY_FAULT)
        service_counters_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_SERVICE_COUNTERS_FAULT)
        attributes_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_ATTRIBUTES_FAULT)
        fn_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_FN_FAULT)
        invalid_fn = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_INVALID_FN)
        hard_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_HARD_FAULT)
        memory_manager_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_MEMORY_MANAGER_FAULT)
        script_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_SCRIPTS_FAULT)
        wait_for_reboot = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_WAIT_FOR_REBOOT)
        universal_counters_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_UNIVERSAL_COUNTERS_FAULT)
        commodities_table_fault = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_COMMODITIES_TABLE_FAULT)

        return \
            no_serial_number, rtc_fault, settings_fault, counter_fault, user_memory_fault, service_counters_fault, \
                attributes_fault, fn_fault, invalid_fn, hard_fault, memory_manager_fault, script_fault, wait_for_reboot, \
                universal_counters_fault, commodities_table_fault

    def reboot_kkt(self):
        self.fptr.deviceReboot()
        return self.request_error_code()

    def set_setting_id(self, _id, _value):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_SETTING_ID, _id)
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_SETTING_VALUE, _value)
        self.fptr.writeDeviceSetting()
        self.request_error_code()
        if self.ErrorCode != self.fptr.LIBFPTR_OK:
            return self.ErrorCode
        self.fptr.commitSettings()
        return self.request_error_code()

    def get_setting_id(self, _id):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_SETTING_ID, _id)
        self.fptr.readDeviceSetting()
        self.request_error_code()
        return self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_SETTING_VALUE)

    def print_string(self, text=None, alignment=None, wrap=None, font=None, double_width=None, double_height=None,
                     linespacing=None, brightness=None, store_in_journal=None):
        self.fptr.beginNonfiscalDocument()
        if text is not None:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_TEXT, text)
        if alignment is not None:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_ALIGNMENT, alignment)
        if wrap is not None:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_TEXT_WRAP, wrap)
        if font is not None:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_FONT, font)
        if double_width is not None:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_FONT_DOUBLE_WIDTH, double_width)
        if double_height is not None:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_FONT_DOUBLE_HEIGHT, double_height)
        if linespacing is not None:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_LINESPACING, linespacing)
        if brightness is not None:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_BRIGHTNESS, brightness)
        if store_in_journal is not None:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_STORE_IN_JOURNAL, store_in_journal)
        self.fptr.printText()
        self.fptr.endNonfiscalDocument()
        return self.request_error_code()

    def print_custom_text(self, text_tuple: tuple):
        self.fptr.open()
        self.fptr.beginNonfiscalDocument()

        for text in text_tuple:
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_TEXT, text)
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_ALIGNMENT, self.fptr.LIBFPTR_ALIGNMENT_CENTER)
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_TEXT_WRAP, self.fptr.LIBFPTR_TW_WORDS)
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_FONT, 0)
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_FONT_DOUBLE_HEIGHT, False)
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_FONT_DOUBLE_WIDTH, False)
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_FORMAT_TEXT, False)
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_LINESPACING, 0)
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_BRIGHTNESS, 0)
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_STORE_IN_JOURNAL, True)
            self.fptr.printText()
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_PRINT_FOOTER, False)
        self.fptr.endNonfiscalDocument()

    def set_no_print_flag(self, no_print):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_REPORT_ELECTRONICALLY, no_print)

    def get_fn_info(self):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_FN_DATA_TYPE, self.fptr.LIBFPTR_FNDT_FN_INFO)
        self.fptr.fnQueryData()
        self.request_error_code()

        serial = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_SERIAL_NUMBER)
        version = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_FN_VERSION)
        type = self.fptr.getParamInt(self.fptr.LIBFPTR_PARAM_FN_TYPE)
        state = self.fptr.getParamInt(self.fptr.LIBFPTR_PARAM_FN_STATE)
        flags = self.fptr.getParamInt(self.fptr.LIBFPTR_PARAM_FN_FLAGS)

        need_replacement = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_FN_NEED_REPLACEMENT)
        exhausted = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_FN_RESOURCE_EXHAUSTED)
        memory_overflow = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_FN_MEMORY_OVERFLOW)
        ofd_timeout = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_FN_OFD_TIMEOUT)
        critical_error = self.fptr.getParamBool(self.fptr.LIBFPTR_PARAM_FN_CRITICAL_ERROR)

        return serial, version, type, state, flags, need_replacement, exhausted, memory_overflow, ofd_timeout, critical_error

    def init_mgm(self):
        self.fptr.initMgm()
        return self.request_error_code()

    def get_last_doc_with_template(self, tempalate, variable_settings=None):
        last_fn_doc_number = self.get_last_fiscal_document_number()
        last_fn_doc_str = None
        for _ in range(3):
            request_last_fn_doc = '{"type": "getFnDocument", "fiscalDocumentNumber": %i}' % last_fn_doc_number
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_JSON_DATA, request_last_fn_doc)
            self.fptr.processJson()
            last_fn_doc_str = (self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_JSON_DATA))
            if last_fn_doc_str != "":
                break
        last_fn_doc_dic = json.loads(str(last_fn_doc_str))
        last_fn_doc_dic = last_fn_doc_dic["documentTLV"]
        logging.info("\nФД %s, JSON из ФН: %s" %
                     (str(last_fn_doc_number),
                      json.dumps(last_fn_doc_dic, sort_keys=True, indent=4, ensure_ascii=False)))

        return last_fn_doc_dic

    def execute_json(self, json_task, timeout=30):
        logging.debug(f"execute_json() < json_task {json_task}, timeout {timeout}")
        try:

            self.fptr.open()
            self.fptr.setParam(self.fptr.LIBFPTR_PARAM_JSON_DATA, json.dumps(json_task))
            self.fptr.processJson()
            response_raw = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_JSON_DATA)
            if response_raw is not None:
                try:
                    response = json.loads(response_raw)
                    logging.debug(f"execute_json() > {response}")
                    return response
                except json.decoder.JSONDecodeError as e:
                    logging.error('[ERROR] error with json.loads from response: {}'.format(e))
        except ValueError as e:
            logging.error('Exception in execute_json(): {}'.format(e))
        finally:
            self.fptr.close()  # Закрытие ДТО
        logging.debug(f"execute_json() > None")
        return None

    def get_last_fd_number(self):

        logging.debug("get_last_fd_number()")
        try:
            json_task = {
                "type": "getFnStatus"
            }
            fn_status = self.execute_json(json_task)
            logging.debug("СТАТУС ФН: %s", fn_status)
            last_fd_number = fn_status['fnStatus']['fiscalDocumentNumber']
            logging.debug(f"get_last_fd_number() > {last_fd_number}")
            logging.info("ФД: %s", last_fd_number)
            return last_fd_number
        except Exception as e:
            logging.error("get_last_fd_number error: {}".format(e))
            logging.debug("get_last_fd_number() > None")
            return None

    def get_fd_from_fn(self, fd: int):
        """
        Извлечение ФД из ФН
        """
        logging.debug(f"get_fd_from_fn() < {fd}")
        if fd is None:
            logging.debug(f"get_fd_from_fn() > None")
            return None
        # JSON задание для чтения документа из ФН
        json_task = {
            "type": "getFnDocument",
            "fiscalDocumentNumber": int(fd),
            "withRawData": False
        }
        fd_fn = self.execute_json(json_task)
        if fd_fn is None:
            return None
        if isinstance(fd_fn, dict):
            fd_fn = fd_fn['documentTLV']
            # formatted_fd_fn = json.dumps(fd_fn, sort_keys=True, indent=4, ensure_ascii=False)
            return fd_fn
        return None

    def get_fn_number(self):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_DATA_TYPE, self.fptr.LIBFPTR_DT_CACHE_REQUISITES)
        self.fptr.queryData()

        serialNumber    = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_FN_SERIAL_NUMBER)
        ecrRegNumber    = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_ECR_REGISTRATION_NUMBER)
        ofdVatin        = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_OFD_VATIN)
        fnsUrl          = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_FNS_URL)
        ffdVersion      = self.fptr.getParamInt(self.fptr.LIBFPTR_PARAM_FFD_VERSION)
        return serialNumber

    def get_rnm_number(self):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_DATA_TYPE, self.fptr.LIBFPTR_DT_CACHE_REQUISITES)
        self.fptr.queryData()

        ecrRegNumber = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_ECR_REGISTRATION_NUMBER)

        return ecrRegNumber

    def get_not_sent_fd_qty(self, ):
        logging.debug(f"get_not_sent_fd_qty()")
        task = {
            "type": "ofdExchangeStatus"
        }
        ofdExchangeStatus = self.execute_json(task)
        if ofdExchangeStatus is not None:
            not_sent_fd_qty = ofdExchangeStatus['status']['notSentCount']
            logging.debug(f"get_not_sent_fd_qty() %s", not_sent_fd_qty)
            return not_sent_fd_qty
        logging.debug(f"get_not_sent_fd_qty() None")
        return None

    def wait_for_sent_all_fd(self, timeout: int = 600):
        logging.debug(f"wait_for_sent_all_fd() timeout %s", timeout)
        start_time = time.time()
        while self.get_not_sent_fd_qty() != 0:
            if time.time() - start_time > timeout:
                logging.debug(f"get_not_sent_fd_qty() False")
                return False
            time.sleep(3)
        logging.debug(f"get_not_sent_fd_qty() True")
        return True

    def process_json(self, json_task, answer_indent=4, flag_all_kkt_settings=False):
        self.fptr.setParam(self.fptr.LIBFPTR_PARAM_JSON_DATA, json_task)
        self.fptr.processJson()
        error = self.request_error_code(flag_all_kkt_settings=flag_all_kkt_settings)
        json_str_answer = self.fptr.getParamString(self.fptr.LIBFPTR_PARAM_JSON_DATA)
        if json_str_answer != "":
            self.JsonAnswer = None
            try:
                self.JsonAnswer = json.dumps(json.loads(json_str_answer), ensure_ascii=False, indent=answer_indent)
            except ValueError:
                logging.error("Не удалось считать структуру из json-ответа")
        return error

    def execute_mass_json(self, json_task, quantity, timeout=30):
        logging.debug(f"execute_json() < json_task {json_task}, timeout {timeout}")
        print(f"execute_json() < json_task {json_task}, timeout {timeout}")
        try:
            if not self.is_connected():
                if not self.wait_to_connect(timeout=timeout):
                    return False
            self.fptr.open()
            count = 0
            while count < quantity:
                self.fptr.setParam(self.fptr.LIBFPTR_PARAM_JSON_DATA, json.dumps(json_task))
                self.fptr.processJson()
                print(count)
                count += 1
        except:
            logging.error('Exception in execute_json():')
        finally:
            self.fptr.close()  # Закрытие ДТО
        logging.debug(f"execute_json() > None")
        return None

    def is_connected(self, timeout=5):
        logging.debug("ККТ is_connected() timeout %s", timeout)
        connected = False

        def check_connection():
            nonlocal connected
            self.fptr.open()
            if self.fptr.isOpened():
                self.fptr.close()
                logging.debug("ККТ is_connected() True")
                connected = True
            self.fptr.close()

        timer = threading.Timer(timeout, check_connection)
        timer.start()

        while not connected and timer.is_alive():
            time.sleep(0.1)

        timer.cancel()

        logging.debug("ККТ is_connected() %s", connected)
        return connected

    def wait_to_connect(self, timeout=300):
        logging.debug(f"wait_to_connect() timeout={timeout}")
        start_time = time.time()
        while not self.is_connected() and not time.time() - start_time > timeout:
            logging.debug(f"Не получен ответ от ККТ, time {time.time() - start_time} timeout {timeout}")
        if self.is_connected():
            logging.debug("ККТ доступна")
            return True
        logging.debug("ККТ не отвечает")
        return False


