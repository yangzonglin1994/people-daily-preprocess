import re


test_str = 'abc\n\nsdf\nsdf\n\n\n'
result = re.split('\n+', test_str)
print('dim:', len(result))
test_str = 'a  b  '
result = re.split('\s+', test_str)
print('dim:', len(result))
