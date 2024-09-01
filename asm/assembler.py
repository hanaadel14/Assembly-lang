class Assembler(object):
    def __init__(self, asmpath='', mripath='', rripath='', ioipath='') -> None:
        """
        

        Initializes 7 important properties of the Assembler class:
        -   1) self.__address_symbol_table (dict): stores labels (scanned in the first pass)
            as keys and their locations as values.
        -   2) self.__bin (dict): stores locations (or addresses) as keys and the binary
            representations of the instructions at these locations (job of the second pass)
            as values.
        -   3) self.__asmfile (str): the file name of the assembly code file. This property
            is initialized and defined in the read_code() method.
        -   4) self.__asm (list): list of lists, where each outer list represents one line of
            assembly code and the inner list is a list of the symbols in that line.
            for example:
                ORG 100
                CLE
            will yiels __asm = [['org', '100'] , ['cle']]
            Notice that all symbols in self.__asm are in lower case.
        -  5) self.__mri_table (dict): stores memory-reference instructions as keys, and their
            binary representations as values.
        -  6) self.__rri_table (dict): stores register-reference instructions as keys, and their
            binary representations as values.
        -  7) self.__ioi_table (dict): stores input-output instructions as keys, and their
            binary representations as values.

        The constructor receives four optional arguments:
        -   asmpath (str): path to the assembly code file.
        -   mripath (str): path to text file containing the MRI instructions. 
        -   rripath (str): path to text file containing the RRI instructions. 
        -   ioipath (str): path to text file containing the IOI instructions. 
            The file should include each intruction and its binary representation separated by a space in a
            separate line. Their must be no empty lines in this file.
        """
        super().__init__()
        # Address symbol table dict -> {symbol: location}
        self.__address_symbol_table = {}
        # stores labels as keys , their location as values (1st pass)
        self.__bin = {}
        # stores locations/addresses as keys , binary representation of inst as values (2nd pass)
        if asmpath:
            self.read_code(asmpath)
            #self.__asmfile (str): the file name of the assembly code file. This property is initialized and defined in the read_code() method.
        self.__mri_table = self.__load_table(mripath) if mripath else {}
        # memory-reference instructions
        self.__rri_table = self.__load_table(rripath) if rripath else {}
        # register reference instructions 
        self.__ioi_table = self.__load_table(ioipath) if ioipath else {}
        #input output instructions 
        #each intruction and its binary representation separated by a space in a separate line. Their must be no empty lines in this file.

    def read_code(self, path: str):
        """
        opens testcode.asm file and stores it in self.__asmfile.
        Returns None
        """ 
        assert path.endswith('.asm') or path.endswith('.S'), \
            'file provided does not end with .asm or .S'
        self.__asmfile = path.split('/')[-1]  # on unix-like systems
        with open(path, 'r') as f:
            # remove '\n' from each line, convert it to lower case, and split it by the whitespaces between the symbols in that line 
            #list has symbols and instructions 
            self.__asm = [s.rstrip().lower().split() for s in f.readlines()]

    def assembler(self, inp='') -> dict:
        assert self.__asm or inp, 'no assembly file provided'
        if inp:
            assert inp.endswith('.asm') or inp.endswith('.S'), \
                'file provided does not end with .asm or .S'
        # if assembly file was not loaded, load it.
        if not self.__asm:
            self.read_code(inp)
        self.__rm_comments()
        # remove comments from loaded assembly code.
        self.__first_pass()
        # do first pass
        self.__second_pass()
        #do second pass 
        # The previous two calls should store the assembled binary code inside self.__bin. So the final step is to return self.__bin
        return self.__bin

    # PRIVATE METHODS
    def _load_table(self, path) -> dict:
        #loads any of ISA tables (MRI, RRI, IOI)
        
        with open(path, 'r') as f:
            t = [s.rstrip().lower().split() for s in f.readlines()]
        return {opcode: binary for opcode, binary in t}

    def _islabel(self, string) -> bool:
        # returns True if string is a label (ends with ,) otherwise False
       return string.endswith(',')

    def _rm_comments(self) -> None:
         #remove comments from code, list of lists
       
        for i in range(len(self.__asm)):
            for j in range(len(self.__asm[i])):
                if self.__asm[i][j].startswith('/'):
                    del self.__asm[i][j:]
                    break

    def _format2bin(self, num: str, numformat: str, format_bits: int) -> str:
        """
        converts num from numformat (hex or dec) to binary representation with
        max format_bits. If the number after conversion is less than format_bits
        long, the formatted text will be left-padded with zeros.
        """
        #Arguments:
         #num (str): the number to be formatted as binary. It can be in either decimal or hexadecimal format.
         #numformat (str): the format of num; either 'hex' or 'dec'.
         #format_bits (int): the number of bits 
      
        if numformat == 'dec':
            return '{:b}'.format(int(num)).zfill(format_bits)
        elif numformat == 'hex':
            return '{:b}'.format(int(num, 16)).zfill(format_bits)
        else:
            raise Exception('format2bin: not supported format provided.')

    def __first_pass(self) -> None:
        lc=0
        for i in range (len(self.__asm)):
             if (self._islabel(self._asm[i][0])):
               self._address_symbol_table[self.asm[i][0][0:3]]=self._format2bin(str(lc),'dec',12)
               lc +=1
             elif self.__asm[i][0]=='org':
                lc=int(self.__asm[i][1],16)
             elif self.__asm[i][0]=='end':
                print(self.__address_symbol_table)
                return
             else:
                lc +=1

    def __second_pass(self) -> None:
        lc=0
        for i in range (len(self.__asm)):
            if (self.__asm[i][0]=='org'):
                lc = int (self.__asm[i][1],16)
            elif (self.__asm[i][0]=='end'):
                return
            elif len(self._asm[i])>2 and self._asm[i][1] == 'dec':
                self._bin[self.format2bin(str(lc),'dec',12)]= self.format2bin(str(self._asm[i][2]),'dec',16) 
                lc  +=1
            elif len(self._asm[i])>2 and self._asm[i][1]== 'hex':
                self._bin[self.format2bin(str(lc),'dec',12)]=self.format2bin(str(self._asm[i][2]),'hex',16) 
                lc  +=1
            instruction= self._asm[i][1] if self.islabel(self.asm[i][0]) else self._asm[i][0]
            bit_15 ='0'
            if instruction in self.__mri_table.keys():
                address= str(self._address_symbol_table[self._asm[i][1]])
                opcode=str(self.__mri_table[instruction])
                self._bin[self._format2bin(str(lc),'dec', 12)]= bit_15 +opcode +address
                lc +=1
            elif instruction in self.__rri_table.keys():
                self._bin[self.format2bin(str(lc),'dec',12)]= str(self._rri_table[instruction])
                lc +=1
            elif instruction in self.__ioi_table.keys():
                self.bin[self.format2bin(str(lc),'dec',12)]= str(self.__ioi_table[instruction])
                lc +=1