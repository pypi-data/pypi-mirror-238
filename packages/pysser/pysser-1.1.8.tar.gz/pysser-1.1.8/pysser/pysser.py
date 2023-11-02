  


import sys





class Pysser():
    def __init__(self,interval=0.1):
        self.sser = None
        if sys.platform.startswith('linux'):
            from .ssermainlinux import ssermain
            self.sser = ssermain(interval=interval)
        else:
            from .ssermainwin import ssermain
            self.sser = ssermain(interval=interval)

    def init(self,port,baudrate,timeout) -> None:
        self.sser.init(port=port,baudrate=baudrate,timeout=timeout)

        
    def flush(self):
        self.sser.flush()

    def close(self) -> None:
        self.sser.close()

    def open(self):
        self.sser.open()

    def is_open(self):
        return self.sser.is_open()
    
    def docommand(self, command, no_response=False, timeout=3, size=1):
        return self.sser.docommand(command=command,no_response=no_response,timeout=timeout,size=size)
    
    def read(self,size=1):
        return self.sser.read(size=size)