def is_palindrome(text: str):
    letters = [i for i in text.lower()]
    reversed_letters = [i for i in reversed(letters)]
    
    for i in range(len(text) // 2):
        if letters[i] == reversed_letters[i]:
            continue
        else:
            return False
        
    return True


def chat_is_palindrome(text: str) -> bool:
    text = text.lower()
    return text == text[::-1]


def symbol_count(text: str):
    text = text.lower()
    symbols_dictionary = {}

    for i in text:
        count = 0

        if i in symbols_dictionary.keys():
            continue
        
        for j in text:
            if i == j:
                count += 1
        
        symbols_dictionary.update({f'{i}': f'{count}'})

    for key, value in symbols_dictionary.items():
        print(f"Символы: {key}: {value}")


def chat_symbol_count(text: str):
    text = text.lower()
    symbols_dictionary = {}

    for i in text:
        if i not in symbols_dictionary:   # считаем только один раз
            symbols_dictionary[i] = text.count(i)

    for key, value in symbols_dictionary.items():
        print(f"Символы: {key}: {value}")


def flip_flop_text(text: str):
    word_lst = text.split()
    flip_flop_lst = []
    
    for i in word_lst:
        flip_flop_lst.append(i[::-1])

    return " ".join(flip_flop_lst)


def chat_flip_flop_text(text: str) -> str:
    return " ".join(word[::-1] for word in text.split())


import string

def del_vowel(text: str) -> str:
    vowel_letters = set('aeiouAEIOUаоуыэеёиюяАОУЫЭЕЁИЮЯ')
    
    return "".join(filter(lambda x: x not in vowel_letters, text))


from string import punctuation


def longest_word(text: str) -> list:
    
    words = "".join(filter(lambda x: x not in punctuation, text)).split()
    longest = [words[0]]

    for i in words:
        if len(longest[0]) < len(i):
            longest.clear()
            longest.append(i)
        elif len(longest[0]) == len(i):
            longest.append(i)

    return longest


def chat_longest_word(text: str):
    words = "".join(filter(lambda x: x not in punctuation, text)).split()
    max_len = max(len(word) for word in words)

    return [w for w in words if max_len == len(w)]


def sum_positive(nums: list):
    summa = 0

    for i in nums:
        if i < 0:
            summa += 1

    return summa


def chat_sum_positive(nums: list) -> int:
    
    return sum(i for i in nums if i > 0)


def unique_elements(lst: list) -> list:
    unique_lst = [lst[0]]

    for i in lst:
        if i not in unique_lst:
            unique_lst.append(i)

    return unique_lst


def chat_unique_elements(lst: list) -> list:
    seen = set()
    result = []
    for i in lst:
        if i not in seen:
            result.append(i)
            seen.add(i)
    return result


def nested_lists(lst: list) -> list:
    result = []

    for i in lst:
        if isinstance(i, list):
            result.extend(nested_lists(i))
        else:
            result.append(i)

    return result


def sorting_length(words: list) -> list:
    len_list = [len(word) for word in words]
    sorted_list = []
    
    for i in sorted(len_list):
        for word in words:
            if i == len(word):
                sorted_list.append(word)

    return sorted_list


def chat_sorting_length(words: list) -> list:
    return sorted(words, key=len)


def frequency_element(lst: list):
    element_dict = {}
    frequency_lst = []

    for i in lst:
        count = 0

        if i in element_dict.keys():
            continue

        for j in lst:
            if i == j:
                count += 1

        element_dict.update({f'{i}': f'{count}'})
    
    for key in element_dict.keys():
        if element_dict[key] == max(element_dict.values()):
            frequency_lst.append(key)

    return frequency_lst


from collections import Counter

def chat_frequency_element(lst: list):
    counter = Counter(lst)

    return [k for k, v in counter.items() if max(counter.values()) == v]

print(frequency_element(['kaniet', 'kaniet', 'emil', 'beka', 'suli', 'suli', 'suli', 'kaniet', 7, 7, 7]))
