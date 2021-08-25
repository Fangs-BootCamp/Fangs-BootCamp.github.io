#!/usr/bin/env python3

import binascii
import logging
import optparse
import sys

try:
    import serial
except ImportError:
    print ("ERROR:")
    print ("You are missing the PySerial library")
    print ("Please install it before continuing")
    sys.exit(0)

class Calculator:

    def __init__(this,serialPort, logLvl=logging.INFO):
       
        # setup logger
        this.log = logging.getLogger( type(this).__name__)
        this.log.setLevel(logLvl)
        this.log.debug("Created")

        this._version = 2019.1

        #setup serial port
        baud = 9600
        this.serial = serial.Serial(serialPort, baud)
        if this.serial.isOpen():
            this.log.debug('Connected to serial device: %s at baud: %d' 
                                % (serialPort, baud) )
        
        #setup mappings
        this.symMap = {
                '&' : 0xfe, '|' : 0xfd, 
                '~' : 0xfc, '^' : 0xfb, 
                '+' : 0xfa, '-' : 0xf9, 
                # inc is bad
                '*' : 0xf7, '%' : 0xf6 
                    }

        this.wordMap = {
                'and' : 0xfe, 'or'  : 0xfd, 
                'not' : 0xfc, 'xor' : 0xfb, 
                'add' : 0xfa, 'sub' : 0xf9, 
                'inc' : 0xf8, 
                'mult': 0xf7, 'mod' : 0xf6 
                }

        this.popPeekMap = {
                'peek' : 0xff, 'pop' : 0xf5 
                } 


    def help(this):
        ''' returns a help message '''

        astr =  [
                'Welcome to the Calculator Interface', 
                ' Please type one command at at time, followed by <enter>, ',
                ' and I will relay those to the FPGA.',
                ' Supported Commands: ', 
                '   0-244: Push the corresponding number to the stack',
                '   ' + ','.join(this.symMap.keys()) + ': Apply operator to stack',
                '   ' + ','.join(this.wordMap.keys()) + ': Apply operator to stack',
                '   ' + ','.join(this.popPeekMap.keys()) + ': return value from stack',
                '   exit,quit: quit the program', 
                '   help: display this message',
                ]
        return '\n'.join(astr)

    def push(this,value):
        '''push the corresponding value to the FPGA'''

        this.log.debug('pushing value:%d' % value)

        assert( isinstance( value, int))
        assert( (value >= 0) and (value <= 244))
        
        binValue = value.to_bytes(1, byteorder='little')
	
        this.log.debug('raw: %s' % str(binValue))

        this.serial.write(binValue)

    #
    #
    #
    def symbol(this,op):
        ''' push the corresonding operation that corresponds to the 
            symbol to the FPGA '''

        try:
            value = this.symMap[op]
            this.log.debug('pushing op:%s (symbol)' % op)
            bin_value = value.to_bytes( length=1, byteorder='little')
            this.serial.write(bin_value)
        except KeyError:
            this.log.err('symbol %s not found!' % op)
    
    #
    #
    #
    def word(this,op):
        ''' push the corresonding operation that corresponds to the 
            word to the FPGA '''

        try:
            value = this.wordMap[op]
            this.log.debug('pushing op:%s (word)' % op)
            bin_value = value.to_bytes( length=1, byteorder='little')
            this.serial.write(bin_value)
        except KeyError:
            this.log.err('word %s not found!' % op)
   
    #
    #
    #
    def peek(this):
        this.log.debug('peeking')
        return this._popPeek('peek')
    
    #
    #
    #
    def pop(this):
        this.log.debug('poping')
        return this._popPeek('pop')

    #
    #
    #
    def _popPeek(this, popPeek):
        ''' does both peek and pop operations
            do not call directly
        '''

        value = this.popPeekMap[popPeek]
        bin_value = value.to_bytes( length=1, byteorder='little')

        this.serial.write(bin_value)
        bin_rx = this.serial.read(1)

        if len(bin_rx) < 1:
            print ('Serial Read Error: Nothing received!')
        
        this.log.debug( 'raw bytes: ' + str(bin_rx) )
        rx = int.from_bytes(bin_rx, byteorder='little')
        
        return str(rx)

    #
    #
    #
    def version(this):
        return 'Calculator Version: ' + str(this._version)
        
####################################
#
#       MAIN
#
####################################

if __name__ == '__main__':
    #
    # Parse options
    #
    parser = optparse.OptionParser()
    parser.add_option('-s', '--serial', 
        action='store', dest='serial',
        help='Serial Port of the FPGA' )
    parser.add_option('-d', '--debug',
        action='store_true', dest='debug', 
        help='Set the debug flag', default=False)
    parser.add_option('-v', '--version',
        action='store_true', dest='version', 
        help='Print the version', default=False)
   
    options, args = parser.parse_args()

    if options.version:
        calc = Calculator(serialPort = options.serial)
        print (str(calc.version()))
        sys.exit(0)

    # serial required
    if not ( options.serial):
        parser.error('-s (Serial Port) missing')

    #
    # Calculator input
    # (decide on debug level)
    #
    if options.debug:

        logging.basicConfig ( level = logging.WARN,
            format='%(levelname)s  %(name)s: %(message)s') 

        calc = Calculator(serialPort = options.serial, logLvl=logging.DEBUG)
    else:
        calc = Calculator(serialPort = options.serial)

    #
    # Print out calculator help
    #
    print (calc.help())

    #
    # Main loop
    #
    while True:
        
        # read in a line, split on space
        keys = input('> ')
        keys = keys.split(' ')
        
        #parse every word individually
        for word in keys:
            print ('processing word: ' + str(word))

            try:
                value = int(word) 

                if (value < 0) or (value > 244):
                    print ('ERROR: Value %d too large!' % value)
                    print ('Ignorning line.')
                    break
                else:
                    calc.push(value)

            except ValueError:

                wordL= word.lower()
                if 'peek' in wordL:
                    value = calc.peek()
                    print ('PEEK returned: ' + str(value))

                elif 'pop' in wordL:
                    value = calc.pop()
                    print ('POP returned: ' + str(value))

                elif wordL in [ 'and', 'or', 'not', 'xor', 'add', 
                                    'sub', 'inc', 'mult', 'mod']:
                    calc.word(wordL)

                elif wordL in [ '&', '|', '~', '^', '+', '-', '*', '%']:
                    calc.symbol(wordL)

                elif 'help' in wordL:
                    print(calc.help())

                elif wordL in ['quit','exit']: 
                    print ('Exiting...')
                    sys.exit(0)

                else:
                    print ('Unrecognized input: %s' % wordL)
                    print ('Ignorning line.')
                    break
