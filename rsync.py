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

import os
import re
import subprocess
import sys

def is_executable(f):
    """Check if file exists and is set executable"""
    return os.path.isfile(f) and os.access(f, os.X_OK)

def exists_in_path(program):
    """Check if program is in PATH.

    Return True if it is, return False if it is not.
    """
    for path in os.environ["PATH"].split(os.pathsep):
        if is_executable(os.path.join(path, program)):
            return True
    return False

class Rsync():
    """Handle calls to the rsync program

    The rsync class requires a ConfigServer object to be passed to it.
    """
    switches = [
            '--acls', '--archive', '--compress', '--crtimes', '--delete',
            '--delete-excluded', '--devices', '--fake-super',
            '--fileflags', '--group', '--hard-links',
            '--human-readable', '--link-dest', '--log-file=~/rsync.log',
            '--numeric-ids', '--one-file-system', '--owner', '--partial',
            '--perms', '--relative', '--specials',
            '--times', '--xattrs'
    ]

    def __init__(self, server):
        if not server:
            print "Rsync() was called without a ConfigServer object. This is a bug."
            sys.exit(1)

        self.server = server

        #if sys.platform == 'darwin':
        #    set darwin-specific flags

    def run(self):
        for path in self.server.paths:
            rsync_cmd = "rsync "
            for a in self.switches:
                rsync_cmd += ' ' + a

            # XXX: Things shouldn't be rsynced to remote_path but to
            # remote_path/our-name.YYYY-MM-DD_HH-MM or something.
            rsync_cmd += " {} {}:'{}'".format(path, self.server.host,
                                              self.server.remote_path)
            print rsync_cmd

    def exists_rsync(self):
        """Check if rsync program is in PATH"""
        if exists_in_path('rsync'):
            return True
        else:
            return False

    def check_version(self, required):
        """Check if the rsync program is of the required version

        Feed check_version a version in tuple format, for example (3,0,9). If
        that version of rsync (or newer) is installed, return True, otherwise
        False.
        """
        version_line = subprocess.check_output(
                ['rsync', '--version']
                ).split("\n")[0]
        version = re.match(
            'rsync\s+version\s((?:\d+\.){2}\d+)\s+protocol\sversion\s\d+',
            version_line)

        our_version = tuple(map(int, version.group(1).split('.')))

        if our_version < required:
            return False
        else:
            return True


if __name__ == "__main__":
    rsync = Rsync({'bwlimit': 400})

    if not rsync.exists_rsync():
        print "rsync does not seem to be installed -- " + \
            "at least it is not in your PATH."
        sys.exit(1)

    if not rsync.check_version((3,0,9)):
        print "The version of rsync installed on this system is too old. " + \
                "Please upgrade!"
        sys.exit(1)
