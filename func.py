import getpass
import sys
import requests

# from IPython.core import release
# from ipython_genutils.py3compat import builtin_mod, PY3, unicode_type, safe_unicode
# from IPython.utils.tokenutil import token_at_cursor, line_at_cursor
# from traitlets import Instance, Type, Any, List, Bool

# from .comm import CommManager
# from .kernelbase import Kernel as KernelBase
# from .zmqshell import ZMQInteractiveShell


import sys, time, os

class Functions:
    def read_logs(self):
            thefile = open('./jupyter.log','r')
            thefile.seek(0,2)
            while True:
                print("reading....")
                line = thefile.readline()
                if not line:
                    time.sleep(1)
                    continue
                yield line



    def yuuvis_post(self):
        key = ""
        #relative path to your content file
        contentFilePath = '/Users/subhayuchakravarty/Downloads/2019 BCG UT Coffee Chats Flyer.pdf'
        #relative path to your metadata file
        metaDataFilePath = '/Users/subhayuchakravarty/Downloads/metadata.json'

        headerDict = {}
        paramDict = {}
        baseUrl = 'https' + '://' + 'api.yuuvis.io'

        header_name = 'Content-Type'
        headerDict['Content-Type'] = 'multipart/form-data, application/x-www-form-urlencoded'

        header_name = 'Ocp-Apim-Subscription-Key'
        headerDict['Ocp-Apim-Subscription-Key'] = key

        session = requests.Session()

        multipart_form_data = {
            'data' :('data.json', open(metaDataFilePath, 'rb'), 'application/json'),
            'cid_63apple' : ('content.pdf', open(contentFilePath, 'rb'), 'application/pdf')
        }

        response = session.post(str(baseUrl+'/dms/objects'), files=multipart_form_data, headers=headerDict)
        print(response.json())


    def do_execute(self, code, silent, store_history=True,
            user_expressions=None, allow_stdin=False):
            shell = self.shell # we'll need this a lot here

            self._forward_input(allow_stdin)

            reply_content = {}
            # try:
            #     res = shell.run_cell(code, store_history=store_history, silent=silent)
            # finally:
            #     self._restore_input()

            # if res.error_before_exec is not None:
            #     err = res.error_before_exec
            # else:
            #     err = res.error_in_exec

            # if res.success:
            #     reply_content[u'status'] = u'ok'
            # else:
            #     reply_content[u'status'] = u'error'

            #     reply_content.update({
            #         u'traceback': shell._last_traceback or [],
            #         u'ename': unicode_type(type(err).__name__),
            #         u'evalue': safe_unicode(err),
            #     })

            #     # FIXME: deprecated piece for ipyparallel (remove in 5.0):
            #     e_info = dict(engine_uuid=self.ident, engine_id=self.int_id,
            #                   method='execute')
            #     reply_content['engine_info'] = e_info


            # # Return the execution counter so clients can display prompts
            # reply_content['execution_count'] = shell.execution_count - 1

            # if 'traceback' in reply_content:
            #     self.log.info("Exception in execute request:\n%s", '\n'.join(reply_content['traceback']))


            # # At this point, we can tell whether the main code execution succeeded
            # # or not.  If it did, we proceed to evaluate user_expressions
            # if reply_content['status'] == 'ok':
            #     reply_content[u'user_expressions'] = \
            #                  shell.user_expressions(user_expressions or {})
            # else:
            #     # If there was an error, don't even try to compute expressions
            #     reply_content[u'user_expressions'] = {}

            # # Payloads should be retrieved regardless of outcome, so we can both
            # # recover partial output (that could have been generated early in a
            # # block, before an error) and always clear the payload system.
            # reply_content[u'payload'] = shell.payload_manager.read_payload()
            # # Be aggressive about clearing the payload because we don't want
            # # it to sit in memory until the next execute_request comes in.
            # shell.payload_manager.clear_payload()

            return reply_content
