cnt = 0
base64str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


class CyclicCharsError(Exception):
    pass
class Base64DecodeError(Exception):
    """Raised when the input value is not Decode in Base 64"""
    pass


class CyclicCharsDecodeError(Exception):
    """Raised when the input value is not CyclicChars"""
    pass


class BytePairError(Exception):
    """Raised when the input value is BytePairError"""
    pass


class BytePairDecodeError(Exception):
    """Raised when the input value is BytePairError"""
    pass


class String(str):
    def __init__(self, str):
        super().__init__()
        self.str = str
        self.rules = []

    def __add__(self, other):
        if isinstance(other,str):
            return String(self.str + other)
        return String(self.str + other.str)

    def get_pairs(self) -> 'dict':
        pairs = []
        last_pair = ()
        for i in range(len(self) - 1):
            pair = self[i], self[i + 1]
            if pair != last_pair:
                pairs.append(pair)
                last_pair = pair
            else:
                last_pair = ()

        freq1 = {}

        for c in pairs:
            freq1[c] = pairs.count(c)
        return freq1

    def base64(self) -> 'String':
        '''
        Encode the String (self) to a base64 string
        :return: a new instance of String with the encoded string.
        '''
        global base64str
        # print("We working on: ", self)
        Binary_ASCII_values = [bin(ord(char))[2:].zfill(8) for char in
                               self]  # כל תו במחרוזת מעביר ליוניקוד לאחר מכן לבינארי
        # print(Binary_ASCII_values)

        long_str = "".join(Binary_ASCII_values)  # מחרוזת ארוכה של הכל
        # print(long_str)
        six_binary_list = []
        if len(long_str) % 6 == 0:
            n = len(long_str) // 6
        else:
            n = (len(long_str) // 6) + 1
        for digits_6 in range(n):
            six_binary_list.append(long_str[:6])
            long_str = long_str[6:]
        if len(six_binary_list[n - 1]) != 6:  # מרפד באפסים משמאל את המספר האחרון
            six_binary_list[n - 1] = six_binary_list[n - 1].ljust(6, '0')
        # print(six_binary_list)

        decimal_list = [int(var, 2) for var in six_binary_list]  # מדפיס את המספר העשרוני
        # print(decimal_list)
        res_lst = []
        for digit in decimal_list:
            res_lst.append(base64str[digit])
        res_str = "".join(res_lst)

        return String(res_str)

    def byte_pair_encoding(self) -> 'String':
        '''
        Encode the String (self) to a byte pair string
        :return: a new instance of String with the encoded string.
        :exception: BytePairError
        # '''
        Other = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'"""
        Digits = "0123456789"
        UpperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        LowerCase = "abcdefghijklmnopqrstuvwxyz"
        self.rules = []
        resh = self.rules.copy()

        Group = None
        dict = self.histogram_of_chars()
        if dict['other printable'] == 0:
            Group = Other
        elif dict['digits'] == 0:
            Group = Digits
        elif dict['upper'] == 0:
            Group = UpperCase
        elif dict['lower'] == 0:
            Group = LowerCase
        if Group == None:
            raise BytePairError()

        pairs = self.get_pairs()
        # print(pairs)
        while set(pairs.values()) != {1}:
            max_pair = max(pairs, key=pairs.get)
            max_pair = "".join(max_pair)

            self = self.replace(max_pair, Group[0])
            rule = Group[0] + " = " + max_pair
            resh.append(rule)
            Group = Group[1:]
            pairs = String(self).get_pairs()
            self = String(self)
        self.rules = resh
        my_str = String(self)
        my_str.rules = resh
        # print(self.rules)
        return my_str

    def cyclic_bits(self, num: int) -> 'String':
        '''
        Encode the String (self) to a cyclic bits string
        :return: a new instance of String with the encoded string.
        '''
        Binary_ASCII_values = [bin(ord(char))[2:].zfill(8) for char in self]
        # print(Binary_ASCII_values)
        for i in range(num):
            Binary_ASCII_values = [char[1:] + char[0] for char in Binary_ASCII_values]
            # print(Binary_ASCII_values)
        while num >= 8:
            num -= 8
            self = self[1:] + self[0]
            return String(self).cyclic_bits(num)

        decimal_list = [int(var, 2) for var in Binary_ASCII_values]  # מדפיס את המספר העשרוני
        # print(decimal_list)
        res = [chr(num) for num in decimal_list]
        res_str = "".join(res)
        return String(res_str)

    def cyclic_chars(self, num: int) -> 'String':
        '''
        Encode the String (self) to a cyclic chars string
        :return: a new instance of String with the encoded string.
        :exception: CyclicCharsError
        '''
        lst = [ord(i) for i in self.str]
        if max(lst) >= 127 or min(lst) <= 31:
            raise CyclicCharsError
        lst_chars = []

        for i, char in enumerate(self):
            remainder = 0
            char = self[i]
            num_ord = ord(char)
            num_new_ord = num_ord + num
            # print(char, '-->', num_ord, '-->', num_new_ord, 'will need to be:', chr(num_new_ord))

            if num_new_ord >= 127:
                num_new_ord = num_new_ord % 127
                remainder = num_new_ord % 127
            while 0 <= num_new_ord <= 31 or num_new_ord >= 127:
                num_new_ord += 1
                num_new_ord = num_new_ord % 127
            num_new_ord += remainder

            new_char = chr(num_new_ord)
            # print(char, 'converted to ->', new_char)
            lst_chars.append(new_char)
            # print(lst_chars)
            new_str = "".join(lst_chars)
            output = String(new_str)
        # bol = isinstance(new_str, String)
        # print(bol)
        return output

    def histogram_of_chars(self) -> dict:
        '''
        calculate the histogram of the String (self). The bins are
        "control code", "digits", "upper", "lower" , "other printable"
        and "higher than 128".
        :return: a dictonery of the histogram. keys are bins.
        '''
        hist_dict = {"control code": 0,
                     "digits": 0,
                     "upper": 0,
                     "lower": 0,
                     "other printable": 0,
                     "higher than 128": 0}
        for idx, char in enumerate(self):
            num = ord(char)
            if 0 <= num <= 127:
                if 0 <= num <= 31 or num == 127:
                    hist_dict["control code"] += 1
                if 48 <= num <= 57:
                    hist_dict["digits"] += 1
                if 65 <= num <= 90:
                    hist_dict["upper"] += 1
                if 97 <= num <= 122:
                    hist_dict["lower"] += 1
                if 32 <= num <= 47 or 58 <= num <= 64 or 91 <= num <= 96 or 123 <= num <= 126:
                    hist_dict["other printable"] += 1
            if 128 <= num:
                hist_dict["higher than 128"] += 1

        return hist_dict

    def decode_base64(self) -> 'String':
        '''
        Decode the String (self) to its original base64 string.
        :return: a new instance of String with the endecoded string.
        :exception: Base64DecodeError
        '''
        six_binary_list = []
        eight_binary_list = []
        global base64str
        for char in base64str:
            if char in base64str:
                continue
            else:
                raise Base64DecodeError()

        res_lst = list(self)
        # print(res_lst)
        for char in res_lst:
            i = base64str.index(char)
            # print(i)
            num = bin(i)
            num = num[2:].zfill(6)
            # print(num)
            six_binary_list.append(num)
        long_binary_str = "".join(six_binary_list)
        if len(long_binary_str) % 8 == 0:
            n = len(long_binary_str) // 8
        else:
            n = (len(long_binary_str) // 8) + 1

        for digits_8 in range(n):
            eight_binary_list.append(long_binary_str[:8])
            long_binary_str = long_binary_str[8:]

        if len(eight_binary_list[n - 1]) != 8:  # מרפד באפסים משמאל את המספר האחרון
            eight_binary_list[n - 1] = eight_binary_list[n - 1].ljust(8, '0')

        # print(eight_binary_list)
        decimal_list = [int(var, 2) for var in eight_binary_list if int(var, 2) > 0]
        # print(decimal_list)
        res_lst = [chr(num) for num in decimal_list]
        # print(res_lst)
        res_string = "".join(res_lst)

        return String(res_string)

    def decode_byte_pair(self) -> 'String':
        '''
        Decode the String (self) to its original byte pair string.
        Uses the property rules.
        :return: a new instance of String with the endecoded string.
        :exception: BytePairDecodeError
        '''

        rules = self.rules.copy()
        # print(rules)

        if not isinstance(rules, list):
            raise BytePairDecodeError

        if not rules:
            raise BytePairDecodeError

        while rules:
            chr_to_replace = rules[-1][0]
            pair_to_replace = rules[-1][-2] + rules[-1][-1]
            self = self.replace(chr_to_replace, pair_to_replace)
            rules = rules[:-1]
        my_str = self
        # x = isinstance(my_str, str)
        # print('need to be False: ->',x)
        return my_str

    def decode_cyclic_bits(self, num: int) -> 'String':
        '''
        Decode the String (self) to its original cyclic bits string.
        :return: a new instance of String with the endecoded string.
        '''
        Binary_ASCII_values = [bin(ord(char))[2:].zfill(8) for char in self]
        # print(Binary_ASCII_values)
        for i in range(num):
            Binary_ASCII_values = [char[-1] + char[:-1] for char in Binary_ASCII_values]
            # print(Binary_ASCII_values)
        while num >= 8:
            num -= 8
            self = self[-1] + self[:-1]
            return String(self).decode_cyclic_bits(num)

        decimal_list = [int(var, 2) for var in Binary_ASCII_values]  # מדפיס את המספר העשרוני
        # print(decimal_list)
        res = [chr(num) for num in decimal_list]
        res_str = "".join(res)
        return String(res_str)

    def decode_cyclic_chars(self, num: int) -> 'String':
        '''
        Decode the String (self) to its original cyclic chars string.
        :return: a new instance of String with the endecoded string.
        :exception: CyclicCharsDecodeError
        '''

        num = -num
        asc = {i - 32: chr(i) for i in range(32, 127)}
        return String("".join([asc[(ord(i) - 32 + num) % 95] for i in self.str]))


