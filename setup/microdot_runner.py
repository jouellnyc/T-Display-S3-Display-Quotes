""" Inital Setup """
from common import setup_file, quotes_dir

import uos
import ujson
import machine

import gc
gc.collect()


from .microdot import Microdot
app = Microdot()

index_page='''<!doctype html>
              <html>
              <head>
              <title> Setup for Quotes </title>
              </head>
              
              <body>
              
              Welcome to Setup for Quotes! <BR>
              
              Please Select the Quotes Group you want to see:
              
              <P>
            
              <form action="/setup/" method="POST" enctype="application/x-www-form-urlencoded">
              
              <select name="quotes" id="quotes">
              
              <option value="1">Buddhist</option>
              <option value="2">Famous Quotes</option>
              <option value="3">Happy Quotes</option>
              
              </select>
              
              <br>
              <P>
              
              <input type="submit" value="Submit" style="height:50px; width:200px" />
                            
              <br>
              
              </form>
              
              </body>
              </HTML>
'''



setup_reply_page='''<!doctype html>
                  <HTML>
                  <head>
                      <title>  Quotes Setup Complete, Please Reboot </title>
                  </head>
                  
                  <body>
                      Quotes Setup Complete!
                      
                      Please Click Reboot button and then: <P>
                      
                      <OL>
                      <LI>Wait 60 seconds for the device to show your Team Score
                      <LI>Remember to put this device back on the original Wifi Network
                      </OL>
                      
                      This web page will NOT refresh!
                      
                      <P>
                      
                      <form action="/reboot/" method="GET">
                      <input type="submit" value="Reboot" style="height:50px; width:200px; font-size:30px">
                      </form>


                  </body>
                  </HTML>
                '''


def write_setup_file():
    fh=open(setup_file,'w')
    
def write_quote_file(quote_type, type_file=None):
    """ NOTE spaces come over as spaces w/o any need to convert  """
    fh=open(type_file,'w')
    fh.write(f"QUOTE_TYPE={quote_type}\n")
    fh.close()
    
@app.route('/')
def index(request):
    return index_page, 200, {'Content-Type': 'text/html'}

@app.route('/setup/', methods=['POST'])
def setup(req):
    if req.method == 'POST':
        quote_type = int(req.form.get('quotes'))
        if quote_type:
            try:
                write_quote_file(quote_type,type_file=f"{quotes_dir}/quote_type.txt")
                write_setup_file()
            except OSError as e:
                print(e)
                return '<HTML><TITLE>Error</TITLE>' + str(e) + '</HTML>', 200, {'Content-Type': 'text/html'}
            else:
                return setup_reply_page, 200, {'Content-Type': 'text/html'}
        else:
            return '<HTML><TITLE>Error: Select a Quote</TITLE>' + "Please Select a Quote" + '</HTML>', 200, {'Content-Type': 'text/html'}
        
            
@app.route('/reboot/', methods=['GET'])
def reboot(req):
    machine.reset()


""" Start Microdot """
print("MicroDot Starting")
app.run(host='0.0.0.0', port=80)
####################




            