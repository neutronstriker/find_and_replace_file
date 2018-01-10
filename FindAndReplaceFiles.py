#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 12:43:54 2017

@author: Srinivas NFind and replace file utility

Description: Searches for the file passed in parameter in the directory passed in the parameter
and replaces it with the provided file.


syntax : FindAndReplaceFiles.py <path_to_search_in> <file_to_replace_with>

It doesn't take CASE into account on Windows, but Considers it in linux.

"""

import fnmatch
import os
import sys
from subprocess import PIPE, Popen

#we could also use the below command to do what the cmdline() is doing
#but it seems os.popen() will be phased out in future. So to make sure the
#the script is compatible with future versions of python I choose that option.
#os.popen('cat /etc/services').read()

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def replaceFile(path,filename):
    if os.name == 'nt':
        #windows copy function
        
        command = 'copy /y '+filename+' '+path
        #sys.stdout.write('Command = '+command )
        #os.system(command)
    
        output  = cmdline(command)
        #print output
        if output.find('1 file(s) copied') == -1:
            #failed to copy
            return 0
    elif os.name == 'posix':
        #linux copy function
        sys.stdout.write('\nLinux system command not implemented yet!\n')
    else:
        sys.stdout.write('\nError! Undefined Operating system.')

    # we will also have to write error handling here, for example if the file to be replaced
    # can't be overwritten because we don't have permissions or if it is open.
    return 1

def usage():
    sys.stdout.write('Usage:\nFindAndReplaceFiles.py <path_to_search_in> <filename>')







try:

    if len(sys.argv) != 3:
        usage()
        exit(0)
    
    sys.stdout.write('Please wait Processing...')    
    
    fileName_to_search = sys.argv[2]
    root_dir = sys.argv[1]
    #scan dir and generate report
    
    
    
    #we can later add an option if required to take filename input from user at starting.    
    resultFileName = 'found.csv'
    
    
    fresult = open('./'+resultFileName,'w')
    
    fresult.write('File to be found is:, '+fileName_to_search+'\n')
    fresult.write('File was found in,Replace status\n')
    
    
    
    
    
    matches = []
    
    #had to use sys.stdout.write because print() by default sends the next print() call to
    #newline, and there are someways to avoid it like either placing comma after the string (which will give a whitespace)
    #or from __future__ print_function (only for python 2.6+) which will make print() behave as python 3.x print() and then we can use 
    # print(data,end=''), but I didn't want any special dependencies so I decided to got with sys.stdout.write().
    
    
    #search current directory for the file
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, fileName_to_search):
            
            #test
            #print 'root '+str(root)+'\n'        
            #print 'dirnames '+str(dirnames)+'\n'
            #print 'filename '+str(filename)+'\n'
            
            #if we give comma after print then next print statement won't go to newline        
            #print '.',        
            sys.stdout.write('.')        
            
            #foundFileName = os.path.join(root, filename)
            if replaceFile(root,fileName_to_search) == 1:
                fresult.write(root+',Success\n')
            else:
                fresult.write(root+',Failed\n')
            matches.append(root)
            
    #print matches
    
    if not matches:
        #print fileName_to_search +' found'
        sys.stdout.write('\n'+fileName_to_search +' found')
        sys.stdout.write('\nPress any key to exit.')
    else:
        sys.stdout.write('\nDone, Output in \"'+ resultFileName + '\"\nPress any key to exit.')
    #print '\npress any key to exit'
    
    
    raw_input()
        
    fresult.close()

except Exception as e:
    sys.stdout.write('\nError occurred, Please find the Error details below:\n')
    sys.stdout.write(str(e))
    sys.stdout.write('\nPress any key to exit.')
    raw_input()

