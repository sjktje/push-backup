#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (c) 2012 Svante Kvarnström <sjk@ankeborg.nu>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
# this list of conditions and the following disclaimer.  
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import sys


class Error():
    pass

class ErrorUnknownConfigOption(Error):
    def __init__(self, conf):
        self.conf = conf
        

class Config():
    def __init__(self):
        self.config = json.load(open('backup.json', 'r'))
        general = config_general()


class ConfigGeneral():
    def __init__(self):
        self.config = json.load(open('backup.json', 'r'))
        
        for x in ['frequency', 'log_file', 'log_level', 'verbosity',
        'daemonize']:
            setattr(self, x, self.config['general'][x])
            del(self.config['general'][x])

        if self.config['general']:
            ''' 
            Entries left in the dictionary? Then they're options unknown to
            us! Let's complain about it.
            '''
            raise ErrorUnknownConfigOption(self.config['general'])
                
try:
    conf = ConfigGeneral()
except ErrorUnknownConfigOption as e:
    print "Unknown config options were found:"
    print e.conf
    sys.exit()

print conf.frequency
print conf.log_file
