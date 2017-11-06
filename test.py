import os
import sys
import random
import string
import sig


def do_test_sig(input_text,
                key_json,
                payload_correct_json,
                payload_wrong_json):
    print('\nTest Start')
    # Writes Signature, Payload file
    os.system("python3 sig.py -p " + key_json + " < " + input_text)
    os.system("python3 sig.py -s " + key_json + " < " + input_text)

    # Verifies a wrong payload and a correct json
    print('Test verifying correct payload.json')
    os.system("python3 sig.py -v " + payload_correct_json)
    with open('verify') as verify:
        line = verify.readline()
        if line == 'True':
            print('\t\t\t\t\tPass!')
        else:
            print('Not Pass!')
        verify.close()
    print('Test verifying wrong payload.json')
    os.system("python3 sig.py -v " + payload_wrong_json)
    with open('verify') as verify:
        line = verify.readline()
        if line == 'False':
            print('\t\t\t\t\tPass!')
        else:
            print('Not Pass!')
        verify.close()
    print('Test verifying my payload.json')
    os.system("python3 sig.py -v payload.json")
    with open('verify') as verify:
        line = verify.readline()
        if line == 'True':
            print('\t\t\t\t\tPass!')
        else:
            print('Not Pass!')
        verify.close()
    print('Test making and verifying 10 Strings')
    counter = 0
    for i in range(10):
        random_string = ''.join(random.choice(string.ascii_uppercase
                                + string.digits) for _ in range(27))
        with open('temporary_text_file_for.test', 'w') as openfile:
            openfile.write(random_string)
            openfile.close()
        os.system("python3 sig.py -p " + key_json
                  + " < temporary_text_file_for.test")
        os.system("python3 sig.py -v payload.json")
        with open('verify') as verify:
            line = verify.readline()
            print('\t' + random_string, end='\t')
            if line == 'True':
                print('Pass!')
                counter += 1
            else:
                print('Not Pass!')
            verify.close()
    print('\t\t\t\t\tPassed %d tests out of 10' % (counter))


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print('Testing with following inputs')
        print('Input Text:              ' + sys.argv[1])
        print('Input key:               ' + sys.argv[2])
        print('Input correct payload:   ' + sys.argv[3])
        print('Input wrong payload:     ' + sys.argv[4])

        do_test_sig(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print('Default test running')
        print('Input Text:              ./input.txt')
        print('Input key:               examples/key.json')
        print('Input correct payload:   examples/payload.correct.json')
        print('Input wrong payload:     examples/payload.wrong.json')

        do_test_sig('input.txt',
                    'examples/key.json',
                    'examples/payload.correct.json',
                    'examples/payload.wrong.json')
