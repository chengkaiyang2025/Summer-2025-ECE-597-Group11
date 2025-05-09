from services.email_process import HuggingFaceModelProcess_1
from tests.test_case import *

h = HuggingFaceModelProcess_1()

print(h.process(message1,""))
print(h.process(message2,""))
print(h.process(message3,""))
print(h.process(message4,""))
print(h.process(message5,""))
