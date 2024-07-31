import os
from skr_web_api import Submission

# email = "kumarshubham209@gmail.com" #os.environ['EMAIL']
# apikey = "4cf2ed7b-3ca4-459f-b9f2-5b52faeeda6e" #os.environ['UTS_API_KEY']
# inputfilename = 'input.txt'
# inst = Submission(email, apikey)
# inst.init_generic_batch("metamap -N", "")
# inst.set_batch_file(inputfilename, inputtext="A spinal tap was performed and oligoclonal bands were detected in the cerebrospinal fluid.\n")
# response = inst.submit()
# print(response.status_code)
# print(response.content.decode('utf-8').replace('NOT DONE LOOP\n', ''))



email = 'kumarshubham209@gmail.com' #os.environ['EMAIL']
apikey = '4cf2ed7b-3ca4-459f-b9f2-5b52faeeda6e' #os.environ['UTS_API_KEY']
inputfilename = 'doc.txt'
inst = Submission(email, apikey)
inst.init_generic_batch("metamap", "-D")
inst.set_batch_file(inputfilename, inputtext="I have fever and cough. Is it flu?\n")
response = inst.submit()
print('response status: {}'.format(response.status_code))
print('content: {}'.format(response.content.decode()))
