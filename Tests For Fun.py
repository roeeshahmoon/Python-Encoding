from String import BytePairDecodeError
from String import String as String
def comment_fun(s):
    '''formats strings to create VPL comments'''
    print('Comment :=>> ' + s)


def grade_fun(num):
    '''formats a number to create a VPL grade'''
    print('Grade :=>> ' + str(num))


grade=0;


try:
    # Using readlines()
    file1 = open('HW3.py', 'r')
    Lines = file1.readlines()
    to_exit = False
    count = 0
    # Strips the newline character
    for line in Lines:
        if "import" in line:
            count += 1
            comment_fun("In line {} you used import: {}".format(count, line.strip()))
            to_exit = True
    if to_exit:
        comment_fun("The work was not tested")
        grade_fun(grade)
        exit(0)

except Exception as e:
    comment_fun("Check for import failed" + str(e))

try:
    my_str = String("aaabdaaabac")
    ans = my_str.byte_pair_encoding()
    if "#d#ac" == ans and ans.rules == ['! = aa', '" = !a', '# = "b']:
        grade += 6
        comment_fun("Passed test number 1")
    else:
        comment_fun("Test 1: byte_pair_encoding does not work properly")


except Exception as e:
    comment_fun("Crash in Test 1:" + str(e))

try:
    my_str = String("Hello world")
    ans = my_str.cyclic_bits(8)
    if "ello worldH" == ans:
        grade += 6
        comment_fun("Passed test number 2")
    else:
        comment_fun("Test 2: cyclic_bits does not work properly")


except Exception as e:
    comment_fun("Crash in Test 2:" + str(e))

try:
    my_str = String("Hello world")
    ans = my_str.cyclic_chars(15)
    if "Wt{{~/'~\"{s" == ans:
        grade += 6
        comment_fun("Passed test number 3")

    else:
        comment_fun("Test 3: cyclic_chars does not work properly")
except Exception as e:
    comment_fun("Crash in Test 3:" + str(e))

try:
    my_str = String("Hello world")
    ans = my_str.base64()
    if "SGVsbG8gd29ybGQ" == ans:
        grade += 6
        comment_fun("Passed test number 4")
    else:
        comment_fun("Test 4: cyclic_chars does not work properly")

except Exception as e:
    comment_fun("Crash in Test 4:" + str(e))

try:
    my_str = String("Hello world")
    old_my_str = String("Hello world")
    my_str.base64()
    ans = old_my_str == my_str
    if ans:
        grade += 6
        comment_fun("Passed test number 5")
    else:
        comment_fun("Test 5: The original string was changed following an action")

except Exception as e:
    comment_fun("Crash in Test 5:" + str(e))

try:
    my_str = String("Hello world")
    ans = my_str.base64()
    if isinstance(ans, String):
        comment_fun("Passed test number 6")
        grade += 5
    else:
        comment_fun("Test 6: The returned object is not a String type")

except Exception as e:
    comment_fun("Crash in Test 6:" + str(e))


try:
    h = String("qwertyui")
    h_byte = h.byte_pair_encoding()
    h_back = h_byte.decode_byte_pair()
    comment_fun("Test 7: BytePairDecodeError not received")

except BytePairDecodeError as e:
    grade += 5
    comment_fun("Passed test number 7")
except Exception as e:
    if Exception != BytePairDecodeError:
        e = "Exception which catch is incorrect"
    comment_fun("Crash in Test 7:" + str(e))

grade_fun(grade)