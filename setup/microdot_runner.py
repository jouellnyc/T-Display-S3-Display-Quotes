""" Inital Setup """
from common import setup_file, quotes_dir

import uos
import ujson
import machine

import gc
gc.collect()

wifi_file='/hardware/wifi_config.py'

from .microdot import Microdot
app = Microdot()

index_page='''<!doctype html>
              <html>
              <head>
              <title> Setup for Quotes </title>
              </head>
              
              <body>
              
              Welcome to Setup for Quotes!
              
              <BR>
              <P>
              <BR>
            
              Please Select Quotes you want to see:
              
              <P>
            
              <form action="/setup/" method="POST" enctype="application/x-www-form-urlencoded">
              
              <select name="quotes" id="quotes">
              
              <option value="1">Buddhist</option>
              <option value="2">Famous Quotes</option>
              <option value="3">Happy Quotes</option>
              
              </select>
              
              <P>
              <br>
              <P>
              
              Please enter your Wifi Name and password:
             
              <P>
              <BR>
              
              
              <br>
              Wifi Name <input type="text" name="ssid" >
              
              <P>
              
              Password <input type="text" name="password" enctype="application/x-www-form-urlencoded">
                            
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

def write_wifi_creds(ssid, pswd):
    """ NOTE spaces in the SSID come over as spaces w/o any need to convert  """
    try:
        fh=open(wifi_file,'w')
        fh.write(f"SSID='{ssid}'\n")
        fh.write(f"PSWD='{pswd}'")
        fh.close()
    except Exception as e:
        return f'Cannot open {wifi_file} {str(e)}'
    else:
        return 0
    
@app.route('/')
def index(request):
    return index_page, 200, {'Content-Type': 'text/html'}

@app.route('/setup/', methods=['POST'])
def setup(req):
    if req.method == 'POST':
        
        quote_type = int(req.form.get('quotes'))
        
        print(quote_type)
        
        if quote_type:
            
            try:
                write_quote_file(quote_type,type_file=f"{quotes_dir}/quote_type.txt")
                write_setup_file()
            except OSError as e:
                print(e)
                return '<HTML><TITLE>Error</TITLE>' + str(e) + '</HTML>', 200, {'Content-Type': 'text/html'}
                
            ssid     = req.form.get('ssid')
            password = req.form.get('password')
            print(ssid)
            print(password)
            
            if ssid and password:
                if write_wifi_creds(ssid, password) == 0:
                    return setup_reply_page, 200, {'Content-Type': 'text/html'}
                else:
                    return '<HTML><TITLE>Password and SSID Write Error</TITLE></HTML>', 200, {'Content-Type': 'text/html'}
            else:
                return 'Please send Password and SSID', 200, {'Content-Type': 'text/html'}
        else:
            return '<HTML><TITLE>Error: Select a Quote</TITLE>' + "Please Select a Quote" + '</HTML>', 200, {'Content-Type': 'text/html'}
        
        
        
        
            
@app.route('/reboot/', methods=['GET'])
def reboot(req):
    machine.reset()


""" Start Microdot """
print("MicroDot Starting")
app.run(host='0.0.0.0', port=80)
####################




            