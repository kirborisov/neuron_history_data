from typing import List
import hashlib
import sys
import json
import numpy as np
import os, psutil


class History:

    history_arr = []
    score_dict = {}
    count_dupl = 0
    limit_mem = 3.7 * 10**9
    limit_mem_finish = 5.7 * 10**9
    iteration = 0
    filepath_history = 'history_data.npy'
    flag_dump = False

    def set_history(self, sequence:List, score:float) -> None:
        """
        Params:
        sequence (list) - массив длинной 500 (int) положительных чисел
        score (float) - от 0 до 1
        """
        if self._check_limit_memory() == False:
            return False

        hash_sequence = self._generate_hash(sequence)

        ex_sequence = self.score_dict.get(hash_sequence)

        if ex_sequence:
            ex_score = ex_sequence
            if ex_score > score:
                self.score_dict.update(hash_sequence=score)
            self.count_dupl += 1

        else:
            self.score_dict[hash_sequence] = score
            self.history_arr.append(sequence)

    def is_it_dupe_sequence(self, sequence:List) -> bool:
        """
        Params:
        sequence (list) - массив длинной 500 (int) положительных чисел
        Return: Bool

        проверяет, есть ли такая в истории. Если есть True если нет False
        """
        if self.history_dict.get(hash_sequence):
            return True
        else:
            return False

    def save_history(self, filepath:str) -> None:
        history_data = {
                    'history_arr':self.history_arr,
                    'score_dict':self.score_dict,
                    'count_dupl':self.count_dupl,
                   }
        np.save(filepath, history_data)

    def load_history(self, filepath:str) -> None:
       """ Загружает данные истории с диска. """
       history_data = np.load(filepath, allow_pickle=True)[()]
       self.history_arr = history_data.get('history_arr')
       self.score_dict = history_data.get('score_dict')
       self.count_dupl = history_data.get('count_dupl')

    def _generate_hash(self, sequence:List):
        """
        Params:
        sequence (list) - массив длинной 500 (int) положительных чисел

        Return: hash md5
        """

        return hashlib.md5(sequence.tobytes()).hexdigest()


    def _check_limit_memory(self) -> None:
        """
        При достижении порога 3gb, должна вывести максимально точное время на
        работу функции и кол-во дубликатов найденных в истории.
        После этого данные истории должны записаться на диск и загрузиться.
        После загрузки, истории, порог увеличивается до 5gb и генерация
        продолжается.
        При достижении порога, должна вывести максимально точное время на
        работу функции, с момента загрузки, и кол-во дубликатов найденных в
        истории.

        """
        self.iteration += 1

        if self.iteration%10**4 == 0:
            process = psutil.Process(os.getpid())
            memory_current = process.memory_info().rss
            print(f'Номер итерации: {self.iteration}')
            if not self.flag_dump and memory_current > self.limit_mem:
                self.save_history(self.filepath_history)
                self.load_history(self.filepath_history)
                self.flag_dump = True

            if memory_current > self.limit_mem_finish:
                return False
