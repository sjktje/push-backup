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
import os
import platform
import sys

class Error():
    pass

class ErrorUnknownConfigOption(Error):
    """Exception used when unknown config options are found."""
    def __init__(self, conf):
        print "Found unknown configuration option: " + str(conf)
        sys.exit(1)

class ErrorMissingConfigOption(Error):
    def __init__(self, e):
        print "Missing configuration option: " + str(e)
        sys.exit(1)

class ErrorNonexistentPath(Error):
    def __init__(self, path):
        print "Nonexistent backup path: " + path
        sys.exit(1)


class Config():
    """Store configuration options

    The following data is saved:

    my_name (string): name of this machine
    frequency (int): how often to backup (in minutes)
    log_file (string): log for rsync transfer info
    verbosity* (int): verbosity of script
    daemonize (bool): whether to daemonize or not

    Settings marked with '*' can be changed from the command line.
    """
    def __init__(self):
        """Load configuration file

        Load json formatted configuration file, backup.json. Exception
        ErrorUnknownConfigOption is raised if unknown configuration options
        are found.
        """
        self.config = json.load(open('../backup.json', 'r'))
        self.servers = []

        try:
            for x in ['frequency', 'log_file', 'log_level', 'verbosity',
                      'daemonize', 'my_name']:
                setattr(self, x, self.config['general'][x])
                del(self.config['general'][x])
            if not self.my_name:
                self.my_name = platform.node()
        except KeyError, e:
            # Set defaults
            if x is 'my_name':
                setattr(self, x, platform.node())
            if x is 'verbosity':
                setattr(self, x, 0)
            else:
                raise ErrorMissingConfigOption(e)

        if self.config['general']:
            raise ErrorUnknownConfigOption(self.config['general'])

        for s in self.config['backup_servers']:
            for path in s['paths']:
                if not os.path.exists(path):
                    raise ErrorNonexistentPath(path)
            self.servers.append(ConfigServer(s))


class ConfigServer():
    """Store information about a backup server

    Each ConfigServer object stores the following information:

    host (string): hostname of backup server
    port (int): port of backup server
    user (string): ssh username
    ssh_key_file (string): rsa/dsa key file used to log in to host
    compression (boolean): whether to compress rsync traffic or not
    bwlimit (string): bandwidth limit
    paths (list of strings): paths to backup

    If additional configuration entries are found, raise exception
    ErrorUnknownConfigOption.
    """
    def __init__(self, server_info):
        try:
            for x in ['host', 'port', 'user', 'ssh_key_file', 'compression',
                      'bwlimit', 'remote_path', 'paths']:
                setattr(self, x, server_info[x])
                del(server_info[x])
        except KeyError, e:
            raise ErrorMissingConfigOption(e)

        if server_info:
            raise ErrorUnknownConfigOption(server_info)


if __name__ == "__main__":
    conf = Config()

    print conf.frequency
    print conf.log_file

    for x in conf.servers:
        print x.host
        for y in x.paths:
            print y

