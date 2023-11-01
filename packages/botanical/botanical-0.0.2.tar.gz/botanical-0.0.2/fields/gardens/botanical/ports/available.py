


'''
	import botanical.ports.available as available_port
	port = available_port.find ()
'''

import socket

#
#	https://stackoverflow.com/a/36331860/2600905
#
def find ():
    with socket.socket () as this_socket:
        this_socket.bind (('', 0))
        return this_socket.getsockname () [1]

	