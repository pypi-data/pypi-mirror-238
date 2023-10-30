import re
from KorDigits.utils.num_unit import NUM_UNIT

import pkg_resources
import json
class Num2Word:
    def __init__(self):
        dict_path = pkg_resources.resource_filename("KorDigits", "utils/word_dict.json")
        dict_file = json.load(open(dict_path, 'r', encoding='utf-8'))
        self.kor1 = dict_file['kor1_dict']  # label 7
        self.kor2 = dict_file['kor2_dict']  # label 8
        self.native_unit_dict1 = dict_file['native_unit_dict1']  # label 7 십의 자리
        self.native_unit_dict2 = dict_file['native_unit_dict2']  # label 8 십의 자리
        self.hanzi = dict_file['hanzi']  # 한자어
        self.unit_dict = dict_file['unit_dict']  # 십이상의 자리
        self.eng = dict_file['eng']  # 영어
        self.cats = ['빌리언', '밀리언', '싸우전드']
        self.month_dict = dict_file['month_dict']  # 월 단위
        self.wave_dict = dict_file['wave_dict']
    def number_to_han(self, num):
        if num == '0':
            return self.hanzi[num]
        elif num == '00':
            return '공공'

        digits = []
        i = len(list(num)) - 1
        is_zero = True
        for digit in str(num):
            if digit != '0':
                is_zero = False
                unit = self.unit_dict[str(i)]
                if i in [1, 5, 9, 13, 17] and digit == '1':
                    digits.append(self.unit_dict[str(i)])
                else:
                    digits.append(self.hanzi[digit] + unit)
            else:
                if not is_zero and i in [4, 5, 6]:
                    digits.append(self.unit_dict[str(4)])
                elif not is_zero and i in [8, 9, 10, 11]:
                    digits.append(self.unit_dict[str(8)])
                elif not is_zero and i in [12, 13, 14, 15]:
                    digits.append(self.unit_dict[str(12)])
                elif not is_zero and i in [16, 17, 18, 19]:
                    digits.append(self.unit_dict[str(16)])

                is_zero = True
            i = i - 1

        result = ''.join(digits)
        start = result[0:2]
        start = start.replace('일만', '만')
        result = start + result[2:]
        result = result.replace('일십', '십').replace('일백', '백').replace('일천', '천')
        return result


    def number_to_kor(self, num):
        if num == 0:
            return self.hanzi[str(num)]

        digits = []
        one = ""
        is_zero = True
        for i, digit in enumerate(num[::-1]):
            if i == 0:
                digits.append(self.kor1[digit])
                one = digit
            elif i == 1:
                if digit == '2' and one == '0':
                    digits.append(self.native_unit_dict1[digit])
                elif digit != "0":
                    digits.append(self.native_unit_dict2[digit])
            else:
                if digit != '0':
                    is_zero = False
                    unit = self.unit_dict[str(i)]
                    if i in [1, 5, 9] and digit == '1':
                        digits.append(self.unit_dict[str(i)])
                    else:
                        digits.append(self.hanzi[digit] + unit)
                else:
                    if not is_zero and i in [4, 5, 6]:
                        digits.append(self.unit_dict[str(4)])
                    elif not is_zero and i in [8, 9, 10]:
                        digits.append(self.unit_dict[str(8)])
                    is_zero = True

        result = ''.join(digits[::-1])
        start = result[0:2]
        start = start.replace('일만', '만')
        result = start + result[2:]
        result = result.replace('일십', '십').replace('일백', '백').replace('일천', '천')
        return result


    def number_to_kor2(self, num):
        if num == 0:
            return self.hanzi[str(num)]

        digits = []
        is_zero = True
        for i, digit in enumerate(num[::-1]):
            if i == 0:
                digits.append(self.kor2[digit])
            elif i == 1:
                digits.append(self.native_unit_dict2[digit])
            else:
                if digit != '0':
                    is_zero = False
                    unit = self.unit_dict[str(i)]
                    if i in [1, 5, 9] and digit == '1':
                        digits.append(self.unit_dict[str(i)])
                    else:
                        if digit != "0":
                            digits.append(self.hanzi[digit] + unit)
                else:
                    if not is_zero and i in [4, 5, 6]:
                        digits.append(self.unit_dict[str(4)])
                    elif not is_zero and i in [8, 9, 10]:
                        digits.append(self.unit_dict[str(8)])
                    is_zero = True

        result = ''.join(digits[::-1])
        start = result[0:2]
        start = start.replace('일만', '만')
        result = start + result[2:]
        result = result.replace('일십', '십').replace('일백', '백').replace('일천', '천')
        return result


    # !/usr/bin/env python3
    # -*- coding: utf-8 -*-
    # File: num2words/en.py
    #
    # Author: Saeed Rasooli <saeed.gnu@gmail.com>    (ilius)
    #
    # This library is free software; you can redistribute it and/or
    # modify it under the terms of the GNU Lesser General Public
    # License as published by the Free Software Foundation; either
    # version 2.1 of the License, or (at your option) any later version.
    #
    # This library is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    # Lesser General Public License for more details.

    ######################### ENG #######################

    def convert_hundred(self, n):
        n = str(n)
        if len(n) < 2:
            n = '0' + n
        if n[0] == '1' or n[1] == '0':
            return self.eng[n]
        else:
            if int(n) < 10:
                return self.eng['0' + n[1]]
            else:
                return self.eng[n[0] + '0'] + self.eng['0' + n[1]]


    def convert_thousand(self, n):
        assert n < 1000
        if n < 10:
            return self.eng['0' + str(n)]
        if n < 100:
            return self.convert_hundred(n)
        n = str(n)
        if n[1:] == '00':
            return f"{self.eng['0' + n[0]]}헌드레드"
        return f"{self.eng['0' + n[0]]}헌드레드{self.convert_hundred(int(n[1:]))}"

    def convert_eng(self, n):
        n = str(n)
        n = n.zfill(12)
        s = []
        for (i, cat) in enumerate(self.cats):
            start, end = i * 3, (i + 1) * 3
            if int(n[start:end]) > 0:
                s.append(self.convert_thousand(int(n[start:end])) + cat)
        if int(n[-3:]) >= 0:
            s.append(self.convert_thousand(int(n[-3:])))
        if s:
            return "".join(s)
class Convert_Unit:
    def __init__(self):
        self.num_unit = NUM_UNIT
        self.num2word = Num2Word()
    def change_kor(self, sentence: str) -> (str, str):
        ''' 한국어 단위명사 리스트에 있을 경우 한국어로 숫자 바꾸기'''
        r_num_group = r"([0-9]+.?\s?~?)+|[0-9]+"
        tagging = re.findall(r_num_group, sentence)
        return tagging

    def change_num_unit(self, sentence: str) -> str:
        ''' 숫자 단위 명사 한글로 바꾸기 '''
        r_unit_pattern = r"\d+\s*여*\s*(?![\uAC00-\uD7A3]+)([a-zA-Z]+|[\S]+)"
        if re.search(r_unit_pattern, sentence):
            unit_sent = re.findall(r_unit_pattern, sentence)
            for sent in unit_sent:
                r_eng_pattern = r"[a-zA-Z]+|[\S]+"
                for x in re.findall(r_eng_pattern, sent):
                    if x.strip() in self.num_unit:
                        sentence = sentence.replace(x.strip(), self.num_unit[x.strip()], 1)
        return sentence