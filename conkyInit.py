#!/usr/bin/python3

import os
import pprint
import numbers
import subprocess

class ConkyInit():

    """Docstring for ConkyInit. """

    def __init__(self):
        """TODO: to be defined1. """
        conkies = ['wakaconky', 'gitconky']
        successfulStart = []
        for conky in conkies:
            filePath = os.path.expanduser('~/.wakaconky/.') + conky
            pid = self.callConky(filePath)
            successfulStart.append(pid)

        for pid in successfulStart:
            if not isinstance(pid, numbers.Number):
                print('ERROR ####')
                print('Could not start conky: ' + conkies[successfulStart.index(pid)])
                print('Sorry...')
            else:
                print('Starting conky ' + conkies[successfulStart.index(pid)] +'. PID: ' + str(pid))

    def callConky(self, conkyrc):
        """TODO: Docstring for callConky.

        :conkyrc: TODO
        :returns: TODO

        """
        p = subprocess.Popen(['conky', '-q', '-c', conkyrc])
        pid = p.pid
        return pid


if __name__ == '__main__':
    c = ConkyInit()
