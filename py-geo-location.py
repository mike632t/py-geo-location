#!/usr/bin/python3
#
#-- py-location.py
#
#   Get current location.
#
#   Requires:           python3
#
#   This program is free software: you can redistribute it and/or modify it
#   under  the terms of the GNU General Public License as published by  the
#   Free Software Foundation, either version 3 of the License, or (at  your
#   option) any later version.
#
#   This  program is distributed in the hope that it will  be  useful,  but
#   WITHOUT   ANY   WARRANTY;   without even  the   implied   warranty   of
#   MERCHANTABILITY  or  FITNESS  FOR A PARTICULAR  PURPOSE.  See  the  GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <http://www.gnu.org/licenses/>. 
#
#   16 Apr 26   0.1   - Initial version - MT
#
VERSION = "0.1"
URI = ('http://ip-api.com/json')

import os, sys, signal

class location(object):

  def __init__(self):
    self.location = []
    self.status = 0 
    self.error = None
    self.update()

  def update(self): # Get geo-location data from URI
    import urllib.request, urllib.error
    import json
    self.status = 0  # Clear any current errors
    self.error = ''
    try: 
      _socket = urllib.request.urlopen(URI)
      _data=_socket.read()
      _url = _socket.geturl()
      _socket.close()
      if _url != URI: # Did the request result in a redirect (if so the query string was invalid)
        raise urllib.error.HTTPError(url=_url, code=302, msg="Invalid query",hdrs=None,fp=None)
      self.location = json.loads(_data)
      if _debug:
        self.dump()
    except urllib.error.URLError as _Error:
      self.status = -1
      sys.stderr.write (getattr(_Error.reason, "strerror", str(_Error.reason)) + '\n') # Get just the error text
      exit(self.status)
    except urllib.error.HTTPError as _Error:
      self.status = _Error.code
      if _Error.code == 404:
        _err = ' not found.'
        sys.stderr.write ('Error : ' + str(_Error.code) + ' - ' + URI + _err)
        self.error = URI + _err
      if _Error.code == 302:
        _err = ' invalid query.'
        sys.stderr.write ('Error : ' + str(_Error.code) + ' - ' + URI + _err)
        self.error = URI + _err
      else:
        sys.stderr.write ('Error : ' + str(_Error.code) + ' - ' + _Error.reason)
        self.error = str(_Error.reason)
      sys.stderr.write ('\n')
      exit(self.status) 
    except Exception:
      import traceback
      self.status = -1
      sys.stderr.write (traceback.format_exc())
      exit(self.status)

  def list(self): # Print Weather data.
    import time, calendar
    if not _debug:  # Don't print anything if debug is enabled... 
      if _verbose:
        _output = 'Location : \t\t'
        _output += self.location['city'] + '\n'
        _output += 'Country : \t\t'
        _output += self.location['country'] + '\n'
        _output += 'Lat/Long : \t\t'
        _output += '%+05.2f' % float(self.location['lat']) + '/' + '%+05.2f' % float(self.location['lon']) + '\n'
        _output += 'ISP : \t\t\t'
        _output += self.location['isp'] + '\n'
        _output += 'Public IP Address : \t'
        _output += self.location['query']
      else:
        _output = self.location['city'] + ', ' + self.location['countryCode']
      sys.stderr.write (_output  + '\n')

  def dump(self): # Print location data.
    import json
    sys.stderr.write (json.dumps(self.location, indent=4) + "\n") # Dump dictionary as JSON.


if __name__ == '__main__': 

  def _about():
    sys.stdout.write(
      "Usage: " + sys.argv[0] + "\n" +
      "Display current location (based on public IP address).\n" + "\n" +
      "  -?, --help               display this help and exit\n" +
      "      --version            output version information and exit\n" +
      "      --debug              dump raw data as JSON\n" +
      "\nExample:\n" +
      "  " + os.path.basename(sys.argv[0]) + "\n")
    raise SystemExit
    
  def _version():
    sys.stdout.write(os.path.basename(sys.argv[0]) + " " + str(VERSION) +"\n"
      "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.\n"
      "This is free software: you are free to change and redistribute it.\n"
      "There is NO WARRANTY, to the extent permitted by law.\n")
    raise SystemExit
    
  def _error(_error):
    sys.stderr.write(os.path.basename(sys.argv[0]) + ": " + _error + "\n")
    raise SystemExit

  try:      
    _debug = False
    _verbose = False

    _count = 1
    _appid = ""
    while _count < len(sys.argv):
      _arg = sys.argv[_count]
      if _arg[:1] == "-" and len(_arg) > 1:
        if _arg.lower() in ["--help", "-?"]:
          _about()
        elif _arg.lower() in "--version":
          _version()
        elif _arg.lower() in "--verbose":
          _verbose = True
        elif _arg.lower() in ["--debug"]:
          _debug = True
        else:
          if _arg[:2] == "--":
            _error ("unrecognized option -- '" + (_arg[1:] + "'"))
          else:
            _error ("invalid option -- '" + (_arg[1:] + "'"))
      else:
        _error("Invalid parameter -- '" + (_arg + "'"))  # No arguments allowed
      _count += 1

    _location = location() # Get the current location based on IP address
    _location.list()

  except KeyboardInterrupt: # Ctrl-C
    pass
  except Exception: # Catch all other errors - otherwise the script will just fail silently!
    import traceback
    sys.stderr.write (traceback.format_exc())
    exit(1)

  exit(0)
