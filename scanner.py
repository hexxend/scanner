#!/usr/bin/env python
# hexxend
# 
# Requires Python2.7
#
#Copyright (C) 2019  HexXend
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#hexxend@protonmail.com

import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)

def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('UPESTAY\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print '[+]%d/tcp open' % tgtPort
        print '[+] ' + str(results)
    except:
        screenLock.acquire()
        print '[-]%d/tcp closed' % tgtPort
    finally:
        screenLock.release()
        connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print "[-] Cannot resolve '%s': Unknown host" % tgtHost
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print '\n[+] Scan Results for: ' + tgtName[0]
    except:
        print '\n[+] Scan Results for: ' + tgtIP
    
    setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()

def main():
    parser = optparse.OptionParser('usage%prog ' +\
        '-H <target host> -p <target port>')

    parser.add_option('-H', dest='tgtHost', type='string', \
       help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', \
       help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')

    if (tgtHost == None) | (tgtPorts[0] == None):
        print '[-] You must specify a target host and port[s].'
        exit(0)

    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()

