# coding: utf-8
from typing import Union, List, Optional
from ofdcomparer.tags_fn import tags
from ofdcomparer import ofd_cri_atol
import logging
import traceback


class ComparerOfd:

    def __init__(self, dto10):
        # Конечный результат обработки
        self.result = {}
        self.DTO10 = dto10

        # Белый лист, проверка отключена
        self.__white_list = ["1162", "1077", "fiscalDocumentType", "qr", "short"]

        self.__cast_methods = {
            'BYTE': self.__cast_byte,
            'INT16': self.__cast_int16,
            'INT32': self.__cast_int32,
            'VLN': self.__cast_vln,
            'FPD': self.__cast_fpd,
            'STRING': self.__cast_string,
            'COINS': self.__cast_coins,
            'UNIXTIME': self.__cast_unixtime,
            'FVLN': self.__cast_fvln,
            'STLV': self.__cast_stlv,
            'ENUM': self.__cast_enum,
            'SET': self.__cast_set,
            'BITS': self.__cast_bits,
            'BYTES': self.__cast_bytes,
        }

        self.etalon_value = None
        self.comparable_value = None

    def compare(self, comparable: dict, etalon: dict) -> bool:
        """
        Сравнение по тегам ФД из ФН и ОФД
        """
        for key in etalon:
            if key in comparable:
                if key in self.__white_list:
                    continue
                try:
                    self.etalon_value = etalon[key]
                    self.comparable_value = comparable[key]
                    if tags[key]['Type'] == 'STLV':
                        self.__cast_stlv(key=str(key), comparable=self.comparable_value, etalon=self.etalon_value)

                    self.__cast_to_one_type(key=str(key), comparable=self.comparable_value,
                                            etalon=self.etalon_value)
                except TypeError as e:
                    logging.error("Exception: {}".format(e))
                    logging.error("params: tag = {}".format(key))
                    traceback.print_exc()
                except Exception as e:
                    logging.error("Exception: {}".format(e))
                    logging.error("params: tag = %s, etalon = %s, comparable = %s", key, etalon[key],
                                  comparable[key])
                    traceback.print_exc()
                if self.comparable_value == self.etalon_value:
                    self.__message_pass(key, self.comparable_value, self.etalon_value)
                else:
                    self.__message_fail(key, self.comparable_value, self.etalon_value)
            else:
                self.__message_not_found(key, self.etalon_value)
        return True

    def compare_etalon_fn_ofd(self, etalon: dict, changes: dict = None) -> bool:
        """
        Метод сравнивает эталон с последним ФД в ФН, затем последний ФД в ФН с ФД в ОФД.
        """
        logging.debug("compare_etalon_fn_ofd()")
        logging.info("Сравнение ФД, ЭТАЛОН : ФН")
        # if bool(changes):
        #     utils.change_values_in_dict(dict_needs_to_change=etalon, changes=changes)
        comparable = self.DTO10.get_fd_from_fn(self.DTO10.get_last_fd_number())
        self.compare(etalon=etalon,
                     comparable=comparable,
                     cast=False)

        logging.debug("etalon: %s", etalon)
        logging.debug("comparable: %s", comparable)
        logging.debug("compare_result: %s", self.result)
        self.output_result_to_log()
        assert not self.is_have_failed()
        self.DTO10.wait_for_sent_all_fd()
        logging.info("Сравнение ФД, ФН : ОФД")
        self.compare_last_fd_in_fn_and_ofd()
        logging.debug("etalon: %s", etalon)
        logging.debug("comparable: %s", comparable)
        logging.debug("compare_result: %s", self.result)
        self.output_result_to_log()
        assert not self.is_have_failed()
        return True

    def compare_last_fd_in_fn_and_ofd(self, changes: dict = None, rnm=None, fn=None, fd=None) -> bool:
        """
        Сравнивает последние документы в ФН и ОФД.
        modif_fd_number - опционально, добавляет смещение в номер сравниваемого документа.
        """

        logging.info("Сравнение ФД, ЭТАЛОН : ФН")
        # if bool(changes):
        #     utils.change_values_in_dict(dict_needs_to_change=etalon, changes=changes)

        # logging.debug("compare_result: %s", self.result)
        # self.output_result_to_log()
        # assert not self.is_have_failed()

        logging.info(f"Считанный документ из теста 4 - {fd}")
        self.DTO10.wait_for_sent_all_fd()
        # logging.info(f"Сравнение ФД, ФН : ОФД {self.DTO10.get_fn_number()} {self.DTO10.get_fn_number()}")
        self.compare_tags(rnm=rnm, fn=fn, fd=fd)
        logging.debug("compare_result: %s", self.result)
        self.output_result_to_log()
        assert not self.is_have_failed()
        return True

    def compare_tags(self, modif_fd_number: Optional[int] = 0, rnm=None, fn=None, fd=None) -> bool:

        logging.debug("compare_tags()")
        try:
            fd_number = self.DTO10.get_last_fd_number()
            # fd = self.Receipt.read_document_from_fn()
            if not rnm or not fn or not fd_number:
                return False
            fd_ofd = ofd_cri_atol.get_fd_from_cri_ofd(reg_number=rnm, fn=fn, fd_number=fd_number)
            logging.info(f"fd_number {fd_number} {fn} {rnm} {fd}")
            logging.info(f"Считанный документ из cri ofd - {fd_ofd}")
            self.compare(etalon=fd, comparable=fd_ofd)
            return True
        except Exception as e:
            logging.error("compare() error: {}".format(e))
            traceback.print_exc()

            return False

    def output_result_to_log(self) -> None:
        """
        Выводит результат сравнения в лог
        """
        if not self.result:
            logging.error("Результат сравнения пуст")
        else:
            for tag in self.result:
                if not self.result[tag][1] == '___WHITE_LIST___':
                    logging.info(
                        f"{self.result[tag][1]} | {self.result[tag][2]} | etalon {self.result[tag][4]} | "
                        f"compared {self.result[tag][3]} | {self.result[tag][5]}")

    def print_result(self) -> None:
        """
        Печатает результат сравнения
        """
        if not self.result:
            logging.error("Результат сравнения пуст")
        else:
            for tag in self.result:
                if not self.result[tag][1] == '___WHITE_LIST___':
                    print(
                        f"{self.result[tag][1]} | {self.result[tag][2]} | etalon {self.result[tag][4]} | "
                        f"compared {self.result[tag][3]} | {self.result[tag][5]}")

    def calc_result(self):
        """
        Считает результаты сравнения тегов и формирует отчет по количествам.
        """
        logging.debug("calc_result()")
        test_result = {tag: 0 for tag in ['passed', 'skipped', 'not_founded', 'failed']}
        if not self.result:
            logging.error("Результат сравнения пуст")
            return None
        for tag in self.result:
            if self.result[tag][1] == "+++PASS+++":
                test_result['passed'] += 1
            if self.result[tag][1] == "__SKIP__":
                test_result['skipped'] += 1
            if self.result[tag][1] == "===NOT_FOUND===":
                test_result['not_founded'] += 1
            if self.result[tag][1] == "---FAIL---":
                test_result['failed'] += 1
        logging.debug("calc_result(): %s", test_result)
        return test_result

    def is_have_failed(self):
        """
        Проверяет, есть ли в результатах сравнения проваленные сравнения тегов или если тег у сравниваемого не обнаружен.
        Если результат хоть одного из этих параметров не равен 0, то вернет True.
        """
        logging.debug("is_have_failed()")
        if not self.result:
            logging.error("Результат сравнения пуст")
            return True
        test_result = self.calc_result()
        if test_result['failed'] != 0 or test_result['not_founded'] != 0:
            logging.debug("is_have_failed(): True")
            self.clear()
            return True
        logging.debug("is_have_failed(): False")
        logging.info("ФД совпали")
        self.clear()
        return False

    def clear(self):
        """
        Очистка результата сравнения
        """
        self.result = {}
        return True

    def __cast_to_one_type(self, key, etalon, comparable):
        """
        Приводит значения одинаковых типов тегов к единой форме представления.
        Например, если один тег в копейках, а другой в рублях.
        """
        if tags[key]['Type'] in self.__cast_methods:
            key_method = tags[key]['Type']
            if not self.__cast_methods[key_method](key, etalon, comparable):
                return False

    def __cast_byte(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов BYTE
        """
        if comparable == 0 or "0":
            self.comparable_value = False
        if comparable == 1 or "1":
            self.comparable_value = True
        if etalon == 0 or "0":
            self.etalon_value = False
        if etalon == 1 or "1":
            self.etalon_value = True
        return True

    def __cast_int16(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов INT16
        """
        return True

    def __cast_int32(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов INT32
        """
        return True

    def __cast_vln(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов VLN
        """
        return True

    def __cast_fpd(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов FPD
        """
        return True

    def __cast_string(self, key: str, etalon: Union[str, List[str]], comparable: Union[str, List[str]]) -> bool:
        """
        Приводит к одному виду тип тегов STRING

        Аргументы:
        - key: Ключ тега (не используется в методе)
        - etalon: Значение эталона, может быть строкой или списком строк
        - comparable: Значение для сравнения, может быть строкой или списком строк

        Возвращает:
        - bool: True, если приведение типа выполнено успешно
        """
        print("__cast_string() < key", key, ", etalon ", etalon, ", comparable ", comparable)
        if isinstance(etalon, list):
            # Если etalon - список, применяем strip() к каждому элементу списка
            self.etalon_value = [value.strip() for value in etalon]

        if isinstance(comparable, list):
            # Если comparable - список, применяем strip() к каждому элементу списка
            self.comparable_value = [value.strip() for value in comparable]

        if isinstance(etalon, str):
            # Если etalon - строка, применяем strip() к ней
            self.etalon_value = etalon.strip()

        if isinstance(comparable, str):
            # Если comparable - строка, применяем strip() к ней
            self.comparable_value = comparable.strip()

        if isinstance(etalon, list) and isinstance(comparable, str):
            # Если etalon - список, а comparable - строка,
            # применяем strip() к первому элементу etalon
            self.etalon_value = etalon[0].strip()

        if isinstance(comparable, list) and isinstance(etalon, str):
            # Если comparable - список, а etalon - строка,
            # применяем strip() к первому элементу comparable
            self.comparable_value = comparable[0].strip()

        return True

    def __cast_coins(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов COINS
        """
        etalon = float(etalon)
        comparable = float(comparable)
        if etalon > comparable:
            self.etalon_value = etalon / 100
            self.comparable_value = float(comparable)
        if comparable > etalon:
            self.comparable_value = comparable / 100
            self.etalon_value = float(etalon)
        return True

    def __cast_unixtime(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов UNIXTIME
        """
        self.etalon_value = self.__remove_timezone(data=etalon)
        self.comparable_value = self.__remove_timezone(data=comparable)
        return True

    def __cast_fvln(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов FVLN
        """
        etalon = str(etalon).strip()
        comparable = str(comparable).strip()
        try:
            self.etalon_value = float(etalon)
            self.comparable_value = float(comparable)
        except ValueError:
            try:
                self.etalon_value = int(etalon)
                self.comparable_value = int(comparable)
                return True
            except ValueError:
                traceback.print_exc()
                return False
        return True

    def __cast_stlv(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов STLV
        """
        if not self.__expand_stlv(etalon=etalon, comparable=comparable, key=key):
            return False
        return True

    def __cast_enum(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов ENUM
        """
        return True

    def __cast_set(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов SET
        """
        return True

    def __cast_bits(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов BITS
        """
        return True

    def __cast_bytes(self, key, etalon, comparable):
        """
        Приводит к одному виду тип тегов BYTES
        """
        return True

    def __expand_stlv(self, key, comparable, etalon):
        """
        Итерируется по составному тегу, и к каждому внутреннему тегу применяет метод compare()
        """
        print("expand_stlv() < comparable", comparable, ", etalon ", etalon, "key ", key)
        if self.__is_list(comparable, etalon):
            if not isinstance(comparable, list) and isinstance(etalon, list):
                # self.compare(comparable=comparable, etalon=etalon[0])
                comparable = [comparable]
                # return True
            elif isinstance(comparable, list) and not isinstance(etalon, list):
                # self.compare(comparable=comparable[0], etalon=etalon)
                etalon = [etalon]
                # return True
            # elif isinstance(comparable, list) and isinstance(etalon, list):
            # print("isinstance(comparable, list) and isinstance(etalon, list)")
            count = 0
            for i in range(len(etalon)):
                print("iteration ", count)
                count += 1
                # print("comparable = ", comparable[etalon.index(i)])
                # print("etalon ", i)
                print("comparable[i] ", comparable[i])
                print("etalon[i] ", etalon[i])
                self.compare(comparable=comparable[i], etalon=etalon[i])
            return True
        if isinstance(comparable, dict) and isinstance(etalon, dict):
            print("isinstance(comparable, dict) and isinstance(etalon, dict)")
            count = 0
            for key, value in etalon.items():
                print("iteration ", count)
                count += 1
                print("comparable ", comparable[key])
                print("etalon ", etalon[key])
                self.compare(comparable=comparable[key], etalon=etalon[key])
            return True
        return False

    def __is_list(self, comparable, etalon):
        """
        Проверяет, является ли хоть одно из значений списком.
        """
        if isinstance(comparable, list) or isinstance(etalon, list):
            return True
        else:
            return False

    def __remove_timezone(self, data):
        """
        Удаляет таймзону из UNIXTIME значения
        """
        if "+" in data:
            return data.split("+")[0]
        return data

    def __append_to_result(self, status, message, key, comparable, etalon):
        """
        Добавление в итоговый результат
        """
        try:
            if not key in self.__white_list:
                self.result[len(self.result) + 1] = status, message, key, comparable, etalon, tags[str(key)]['Name']
                return True
            self.result[len(self.result) + 1] = True, "___WHITE_LIST___", key, comparable, etalon
            return True
        except Exception as e:
            logging.error("[ERROR] ", status, message, key, comparable, etalon)
            logging.error("Exception: {}".format(e))
            traceback.print_exc()
            return False

    def __message_pass(self, key, comparable, etalon):
        """
        Добавление в итоговый лист положительный результат сравнения
        """
        if not self.__append_to_result(True, "+++PASS+++", key, comparable, etalon):
            return False
        return True

    def __message_fail(self, key, comparable, etalon):
        """
        Добавление в итоговый лист отрицательный результат сравнения
        """
        if not self.__append_to_result(False, "---FAIL---", key, comparable, etalon):
            return False
        return True

    def __message_not_found(self, key, etalon):
        """
        Добавление в итоговый лист неудавшееся сравнение
        """
        if not self.__append_to_result(False, "===NOT_FOUND===", key, "None", etalon):
            return False
        return True

    def __message_error(self, key, comparable, etalon):
        """
        Добавление в итоговый лист сообщение об ошибке в обработке тега
        """
        if not self.__append_to_result(False, "[ERROR]", key, comparable, etalon):
            return False
        return True

    def __message_skip(self, key, comparable, etalon):
        """
        Добавление в итоговый лист сообщения о пропуске обработки тега
        """
        if not self.__append_to_result(True, "__SKIP__", key, comparable, etalon):
            return False
        return True
