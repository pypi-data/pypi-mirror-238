import random
import warnings
import pkg_resources

import os
import pandas as pd
import re
import json

from KorDigits.utils.KoCharELECTRA.tokenization_kocharelectra import KoCharElectraTokenizer
from KorDigits.model.LSTM_CLS_Model import LSTM_Model
import torch
import platform
if "Windows" == platform.system():
    from eunjeon import Mecab # Windows
else:
    from konlpy.tag import Mecab # Linux
from KorDigits.utils.convert_num_unit import (
    Convert_Unit, Num2Word
)

warnings.filterwarnings("ignore")
from datetime import datetime
class Label2Num:
    def __init__(self, mecab):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        hidden_size = 512  # 512
        embed_size = 512  #
        dropout = 0.3
        num_layers = 2
        num_classes = 10
        self.tokenizer = KoCharElectraTokenizer.from_pretrained("monologg/kocharelectra-base-discriminator")
        special_tokens_dict = {'additional_special_tokens': ['<N>', '</N>']}
        self.tokenizer.add_special_tokens(special_tokens_dict)
        src_vocab_size = len(self.tokenizer.get_vocab())
        self.model = LSTM_Model(num_classes, src_vocab_size, embed_size, hidden_size, num_layers, dropout, num_filters=32,
                           kernel_size=5)

        model_path = pkg_resources.resource_filename("KorDigits", "results/save_model/lstm_kt_model.pt")
        self.model.load_state_dict(torch.load(model_path))


        self.mecab = mecab
        self.convert_unit = Convert_Unit()
        self.num2word = Num2Word()

    def _preprocess(self, sentence):
        # 정규표현식을 이용해 숫자를 추출하는 패턴
        if sentence.endswith("."):
            sentence = sentence[:-1]


        number_pattern = r"\d+"
        is_num = False
        self.start, self.end = [], []

        # 숫자가 이어질 때 단위명사가 끝에 있는 경우 하나로 묶기
        num_words, num_word = [], ""
        split_sentence = sentence.split()
        is_continue = False
        for s in split_sentence:
            # 1 2개 처럼 단위 명사가 뒤에만 붙은 경우 처리
            is_SN, is_NNBC = False, False
            for w, p in self.mecab.pos(s):
                if p == 'SN':
                    is_SN = True
                if is_SN and (p == 'NNBC' or p == 'NNG' or p == 'NR' or p == 'NNP'):
                    is_NNBC = True
            if is_SN == True and is_NNBC == False:
                num_word += s + " "
                is_continue = True
            elif is_SN == True and is_NNBC == True and is_continue == True:
                num_word += s + " "
                is_continue = False
                num_words.append(num_word.strip())
                if len(num_word.strip().split()) > 1:
                    sentence = sentence.replace(num_word.strip(), "NUMERAL", 1)
                else:
                    num_words.pop()
                num_word = ""
            else:
                is_continue = False
                if len(num_word) > 0:
                    num_words.append(num_word.strip())
                    if len(num_word.strip().split()) > 1:
                        sentence = sentence.replace(num_word.strip(), "NUMERAL", 1)
                    else:
                        num_words.pop()
                    num_word = ""
        # end 하나로 묶기

        # 나머지 처리
        if len(num_word) > 0:
            num_words.append(num_word.strip())
            if len(num_word.strip().split()) > 1:
                sentence = sentence.replace(num_word.strip(), "NUMERAL", 1)
            else:
                num_words.pop()

        if re.search(number_pattern, sentence) or len(num_words) > 0:
            is_num = True
            result = []
            num_pattern = r'\b\S*\d+\S*\b'

            words = re.findall(num_pattern, sentence)
            sentence = re.sub(r"\d+", "NUM", sentence)
            split_sentence = sentence.split()

            # 이어지는 단위명사 숫자 처리
            for i, word in enumerate(num_words):
                for j in range(len(split_sentence)):
                    tmp = split_sentence[:]
                    if 'NUMERAL' in split_sentence[j]:
                        tmp[j] = tmp[j].replace('NUMERAL', word.strip(), 1)
                        start = max(0, j - 2)
                        end = min(len(split_sentence)+len(word.split()), j+3+len(word.split()))
                        self.start.append(start)
                        self.end.append(end)
                        result.append(" ".join(tmp[start:end]))
                        split_sentence[j] = "NuM" + str(i)
                        break
            for i, word in enumerate(words):
                for j in range(len(split_sentence)):
                    tmp = split_sentence[:]
                    if 'NUM' in split_sentence[j]:
                        tmp[j] = word.strip()
                        start = max(0, j - 2)
                        end = min(len(split_sentence), j+3)
                        self.start.append(start)
                        self.end.append(end)
                        result.append(" ".join(tmp[start:end]))
                        split_sentence[j] = "NuM" + str(i)
                        break

            for i in range(len(num_words)):
                words.insert(i, num_words[i])
            # 결과 반환
            return result, is_num

        # 문장에 숫자가 없으면 문장 반환
        else:
            return sentence, is_num

    def generate(self, sentence):
        # 전처리
        ''' 숫자 뒤 영어 단위 한글로 바꾸기 '''
        sentence = self.convert_unit.change_num_unit(sentence)
        sentence_list, is_num = self._preprocess(sentence)
        self.sentence_list = sentence_list
        self.model.eval()
        self.labels = []
        pattern = r"NuM(\d+)"
        previous_pred = []

        # 한국어로 읽히는 단위명사 저장 리스트 읽기
        kor_pronun_unit = pkg_resources.resource_filename("KorDigits", "utils/kor_pronun_unit.TXT")
        with open(kor_pronun_unit, 'r', encoding='utf-8') as f:
            kor_unit_list = f.readlines()
        kor_unit_list = [x.replace('"', "").strip() for x in kor_unit_list]

        # 문장에 숫자가 포함되어 있을 경우
        if is_num:
            nnbc_count = {}  # 단위 명사 갯수
            past_max_label = ""  # 이전 동일 단위 명사 최대 빈도 label
            max_nnbc_label = ""
            for i in range(len(self.sentence_list)):
                # 이전 NuM 채우기
                nums = re.findall(pattern, self.sentence_list[i])
                for j in nums:
                    j = int(j)
                    self.sentence_list[i] = self.sentence_list[i].replace(f"NuM{j}", previous_pred[j])

                is_korean = False # 한국어 단위 명사 부합하는지 확인

                # 단위 명사 같은거 통일하기 위해 형태소 분석
                is_SN, nnbc = False, ""
                for w, p in self.mecab.pos(self.sentence_list[i]):
                    if p == 'SN' and re.search('\d+', w):
                        is_SN = True
                    elif is_SN and (p == 'NNBC' or p == 'NR'):
                        ''' 한국어로 읽히는 리스트에 있는지 확인 '''
                        if w in kor_unit_list:
                            tagging = self.convert_unit.change_kor(self.sentence_list[i])
                            for tag in tagging:
                                label = 7
                                self.labels.append(label)
                                pred = self._generate_pred(label, tag)
                                sentence = sentence.replace(tag.strip(), pred.strip(), 1)
                                previous_pred.append(pred)
                                is_korean = True
                            break
                        if w not in nnbc_count:
                            nnbc_count[w] = {x: 0 for x in range(10)}
                        nnbc = w
                        break
                    else:
                        is_SN = False

                if not is_korean:
                    with torch.no_grad():
                        tokenized_sentence = self.tokenizer.encode(self.sentence_list[i], add_special_tokens=True,
                                                                   max_length=128,
                                                                   padding='max_length', truncation=True)

                        if '=' in self.sentence_list[i]:
                            label = 3
                        else:
                            input_tensor = torch.LongTensor(tokenized_sentence).to(self.device)
                            model = self.model.to(self.device)
                            output = model(input_tensor.unsqueeze(0), self.device)
                            label = torch.argmax(output, dim=1).detach().cpu().numpy()[0]

                        # 단위 명사 count
                        if is_SN and nnbc:
                            nnbc_count[nnbc][label] = nnbc_count[nnbc][label] + 1

                    tagging = ""
                    for s in self.sentence_list[i].split():
                        if re.search("\d+", s):
                            tagging += s + " "
                    tagging = tagging.strip()

                    # 동일한 단위 명사 label 제일 많이 나온거  찾기
                    if nnbc:
                        max_value = max(nnbc_count[nnbc].values())
                        max_labels = [label for label, count in nnbc_count[nnbc].items() if count == max_value]
                        # 동일 단위명사 최대 빈도가 하나인 경우
                        if len(max_labels) < 2:
                            max_nnbc_label = max_labels[0]
                        else:
                            max_nnbc_label = past_max_label
                        past_max_label = max_nnbc_label

                    # 숫자 뒤에 단위 명사가 있고 현재 label이 제일 많이 나온 label가 다를 때 바꾸기
                    if nnbc and label != max_nnbc_label:
                        # 단위 명사 중복 상관 없는 레이블 제외
                        if not ((label == 3 and max_nnbc_label == 5) or (label == 5 and max_nnbc_label == 3) or
                                (label == 7 and max_nnbc_label == 8) or (label == 8 and max_nnbc_label == 7)):
                            nnbc_count[nnbc][label] = nnbc_count[nnbc][label] - 1
                            label = max_nnbc_label
                            nnbc_count[nnbc][label] = nnbc_count[nnbc][label] + 1
                    self.labels.append(label)

                    pred = self._generate_pred(label, tagging)

                    previous_pred.append(pred)
                    pred = pred.strip()
                    sentence = sentence.replace(tagging.strip(), pred.strip(), 1)
                sentence = re.sub(r" +", " ", sentence).strip()

        return sentence

    def _generate_pred(self, label, tagging):
        if label == 0:
            pred = self._label_0(tagging)
        elif label == 1:
            pred = self._label_1(tagging)
        elif label == 2:
            pred = self._label_2(tagging)
        elif label == 3:
            pattern = r"0\d+"
            try:
                if re.search(pattern, tagging):
                    pred = self._label_5(tagging)
                else:
                    pred = self._label_3(tagging)
            except:
                pred = self._label_5(tagging)

        elif label == 4:
            pred = self._label_4(tagging)
        elif label == 5:
            pred = self._label_5(tagging)
        elif label == 6:
            pred = self._label_6(tagging)
        elif label == 7:
            pred = self._label_7(tagging)
        elif label == 8:
            pred = self._label_8(tagging)
        elif label == 9:
            pred = self._label_9(tagging)
        else:
            return tagging

        return pred

    def _label_0(self, tagging):
        # 몇시 몇분 -> '시' 12이하는 고유어, 13이상은 한자어, '분' 한자어
        # 몇시간 몇분 -> '시간' 고유어, '분' 한자어
        # 9:00 처리
        output = tagging[:]
        minute_regex = r"(\d+)분|(\d+)여분"
        second_regex = r"\d+초"
        if ":" in tagging:
            # 시 분
            if len(output.split(":")) == 2:
                output = output.replace(":", '시')
                output = output.strip() + "분"
            # 시 분 초
            elif len(output.split(":")) == 3:
                output = output.replace(":", '시', 1)
                output = output.replace(":", '분', 1)
                output = output.strip() + "초"

        if '시간' in output:
            hour_regex = r"(\d+)시간"
            if re.search(hour_regex, output):
                hours = re.search(hour_regex, output).group()
                hours = re.findall(r"\d+", hours)
                for hour in hours:
                    if hour == '0':
                        hour_string = '영'
                    else:
                        hour_string = self.num2word.number_to_kor(hour)
                    output = output.replace(hour, hour_string, 1)


        elif '시' in output or "씨" in output:
            hour_regex = r"(\d+)시|(\d+)씨"
            if re.search(hour_regex, output):
                hours = re.search(hour_regex, output).group()
                hours = re.findall(r"\d+", hours)
                for hour in hours:
                    # 12시 이하
                    if int(hour) <= 12:
                        if hour == '0':
                            hour_string = '영'
                        else:
                            hour_string = self.num2word.number_to_kor(hour)
                    # 12시 이상
                    else:
                        hour_string = self.num2word.number_to_han(hour)
                    output = output.replace(hour, hour_string, 1)

        # 분 처리
        if re.search(minute_regex, output):
            minutes = re.search(minute_regex, output).group()
            minutes = re.findall(r"\d+", minutes)
            for minute in minutes:
                # '분' 십의 자리 숫자
                if minute == '0':
                    minute_string = "영"
                else:
                    minute_string = self.num2word.number_to_han(minute)
                output = output.replace(minute, minute_string, 1)

        # 초 처리
        if re.search(second_regex, output):
            seconds = re.findall(r"\d+", output)
            for second in seconds:
                if second == '00':
                    second_string = "영"
                else:
                    second_string = self.num2word.number_to_han(second)
                output = output.replace(second, second_string, 1)
        # 점 처리
        if "." in output:
            point_regex = r"\d+\.\d+"
            point_match = re.search(point_regex, output)
            if point_match:
                decimal_part = point_match.group()
                decimal = decimal_part.split(".")[-1]
                under_point = decimal[:]
                for d in decimal:
                    if d == "0":
                        num_words = "영"
                    else:
                        num_words = self.num2word.number_to_han(d)
                    under_point = under_point.replace(d, num_words, 1)
                output = output.replace("." + decimal, "." + under_point, 1)

        # 처리 안된 부분
        if re.search(r"\d+", output):
            nums = re.findall(r"\d+", output)
            for n in nums:
                num_words = self.num2word.number_to_han(n)
                output = output.replace(n, num_words)

        output = output.replace("~", " 에서 ").replace(".", "쩜").replace("공공분", "")

        return output

    def _label_1(self, tagging):
        regex = "\d+"
        num = re.findall(regex, tagging)
        output = tagging[:]
        for n in num:
            num_words = self.num2word.convert_eng(n)
            output = output.replace(n, num_words, 1)

        output = output.replace("+", '플러스')

        return output

    def _label_2(self, tagging):
        year_regex = "\d+년"
        month_regex = "\d+월"
        day_regex = "\d+일"
        output = tagging[:].replace(",", "")

        output = output.replace("~", " 에서 ")
        year = re.search(year_regex, output).group()[:-1] if re.search(year_regex, output) else None
        month = re.findall(month_regex, output) if re.search(month_regex, output) else None
        day = re.search(day_regex, output).group()[:-1] if re.search(day_regex, output) else None

        if year:
            num_words = self.num2word.number_to_han(year)
            output = output.replace(year, num_words, 1)
        if month:
            for m in month:
                _m = str(int(m[:-1]))
                try:
                    num_words = self.month_dict[_m]
                    output = output.replace(m[:-1], num_words, 1)
                except:
                    num_words = self.num2word.number_to_han(_m)
                    output = output.replace(m[:-1], num_words, 1)
        if day:
            num_words = self.num2word.number_to_han(day)
            output = output.replace(day, num_words, 1)

        # 나머지
        comma_regex = r"\d+"
        comma_match = re.search(comma_regex, output)
        if comma_match:
            comma_list = re.findall(comma_regex, output)
            for c in comma_list:
                num_words = self.num2word.number_to_han(c)
                output = output.replace(c, num_words, 1)
        output = output.replace(",", "")

        if year is None and month is None and day is None:
            output = self._label_3(output)

        return output

    def _label_3(self, tagging):
        tagging = tagging.replace(",", "").replace("∼", "~")
        regex = r"\d+"
        division_regex = r"^\d+/\d+[ㄱ-ㅣ가-힣]*$"
        vs_regex = r"\d+대\d+"
        is_vs = False
        output = tagging[:]

        # / -> 몇분의몇
        if re.search(division_regex, output):
            num_regex = r"(\d+)/(\d+)"
            output = re.sub(num_regex, r"\2/\1", output)
            output = output.replace("/", " 분의 ")


        # 소수점
        if "." in output:
            point_regex = r"\d+\.\d+"
            point_match = re.search(point_regex, output)
            if point_match:
                decimal_part = re.findall(point_regex, output)
                for decimals in decimal_part:
                    decimal = decimals.split(".")[-1]
                    under_point = decimal[:]
                    if decimals.split(".")[0] == '0':
                        output = output.replace('0', "영", 1)
                    for d in decimal:
                        if d == "0":
                            num_words = "영"
                        else:
                            num_words = self.num2word.number_to_han(d)
                        under_point = under_point.replace(d, num_words, 1)
                    output = output.replace("." + decimal, "." + under_point, 1)
        if re.search(vs_regex, output):
            is_vs = True

        num = re.findall(regex, output)
        for n in num:
            if is_vs and n == '0':
                num_words = '영'
            else:
                num_words = self.num2word.number_to_han(n)
            output = output.replace(n, num_words, 1)

        output = output.replace(".", "쩜").replace("~", " 에서 ").replace(":", " 대 ")
        return output

    def _label_4(self, tagging):
        regex = "\d+"
        num = re.findall(regex, tagging)
        output = tagging[:]
        for n in num:
            for i in list(n):
                num_words = self.num2word.convert_eng(i)
                output = output.replace(i, num_words, 1)

        output = output.replace("+", '플러스')

        return output

    def _label_5(self, tagging):
        regex = r"\d"
        division_regex = r"^\d+/\d+[ㄱ-ㅣ가-힣]*$"
        output = tagging[:]
        vs_regex = r"\d+대\d+"
        is_vs = False
        # 소수점 처리
        if '.' in tagging:
            output = output.replace("0", "영")

        # / -> 몇분의몇
        if re.search(division_regex, output):
            if '분기' in output:
                output = output.replace("/", "")
            else:
                num_regex = r"(\d+)/(\d+)"
                output = re.sub(num_regex, r"\2/\1", output)
                output = output.replace("/", " 분의 ")


        # 몇대몇 처리
        if re.search(vs_regex, output):
            is_vs = True

        num = re.findall(regex, output)
        for n in num:
            if is_vs or len(num) == 1 and n == '0':
                num_words = '영'
            else:
                num_words = self.num2word.hanzi[n]
            # output = output.replace(n, " "+num_words + " ", 1)
            output = output.replace(n, num_words, 1)
        output = output.replace(".", '쩜').replace("~", " 에서 ").replace("+", "플러스").replace(":", " 대 ")
        return output

    def _label_6(self, tagging):
        regex = r"\d+[~|∼]\d+"

        if not re.search(regex, tagging):
            return self._label_8(tagging)
        num = re.search(regex, tagging).group()
        output = tagging[:].replace("∼", "~")

        # 십의 자리 이상의 숫자가 들어오면
        start, end = num.split("~")
        if len(list(start)) > 1:
            start_ones = int(start[-1])
            start_tens = int(start) - start_ones
            end_ones = int(end[-1])

            tens = self.num2word.number_to_kor(str(start_tens))

            ones = str(start_ones) + "~" + str(end_ones)
            ones = self.wave_dict[ones]

            result = tens + ones
            output = output.replace(num, result)
            return output
        else:
            try:
                num_words = self.wave_dict[num]
                output = output.replace(num, num_words)
            except:
                output = self._label_7(tagging)

        return output

    def _label_7(self, tagging):
        tagging = tagging.replace(",", "").replace("∼", "~")
        regex = r"\d+"
        wave_regex = r"\d+~\d+\D*"
        output = tagging[:]

        # ~처리
        wave_match = re.search(wave_regex, output)
        if wave_match:
            nums = re.findall(r"\d+", wave_match.group())

            for c in nums:
                num_words = self.num2word.number_to_kor(c)
                output = output.replace(c, num_words)
            output = output.replace("~", " 에서 ")

        num = re.findall(regex, output)
        for n in num:
            if n == '0':
                output = output.replace(n, '영', 1)
            else:
                num_words = self.num2word.number_to_kor(n)
                output = output.replace(n, num_words, 1)

        output = output.replace("~", " 에서 ")

        return output

    def _label_8(self, tagging):
        tagging = tagging.replace(",", "").replace("∼", "~")
        regex = r"\d+"
        output = tagging[:]

        num = re.findall(regex, output)
        for n in num:
            if n == '0':
                output = output.replace(n, '영', 1)
            else:
                num_words = self.num2word.number_to_kor2(n)
                output = output.replace(n, num_words, 1)

        output = output.replace("~", " 에서 ")

        return output

    def _label_9(self, tagging):
        regex = r"\d+\.\d+"
        score_regex = r"\d+.*-.*\d+|\d+.*:.*\d+"
        output = tagging[:]

        if re.search(regex, output):
            num = re.search(regex, output).group()
            # 할푼리가 아니라면 그냥 소수점으로
            if len(num) != 5:
                return self._label_3(tagging)

            # 할푼리
            decimal_part = num.split(".")
            baseball = ['할', '푼', '리']
            if decimal_part[0] == '0':
                output = output.replace("0.", "")
                decimal = list(decimal_part[1])
                for i in range(len(decimal)):
                    num_i = self.num2word.number_to_han(decimal[i])
                    if int(decimal[i]) > 0:
                        result = num_i + baseball[i]
                        output = output.replace(decimal[i], result, 1)
                    else:
                        output = output.replace(decimal[i], "")

            # 날짜
            else:
                num = num.replace(".", "", 1)
                output = output.replace(".", "", 1)

                for n in num:
                    num_words = self.num2word.number_to_han(n)
                    output = output.replace(n, num_words, 1)

        elif re.search(score_regex, output):
            regex = r"\d+"
            num_list = re.findall(regex, output)
            for n in num_list:
                if n == "0":
                    num_word = "영"
                else:
                    num_word = self.num2word.number_to_han(str(n))
                output = output.replace(str(n), num_word)
            output = output.replace(":", " 대 ").replace("-", " 대 ")
        else:
            return self._label_5(output)

        return output


if __name__ == '__main__':
    mecab = Mecab()
    label2num = Label2Num(mecab)
    print(label2num.generate("이 공은 홀에서 약 6ｍ 떨어진 지점으로 향했고 우즈는 결국 버디 퍼트에 성공했다."))
    print(label2num.sentence_list)
    print(label2num.labels)


