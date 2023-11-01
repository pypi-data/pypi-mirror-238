

'''
	python3 status.py cycle/status_1.py
'''

import botanical.cycle as cycle
import time

def check_1 ():
	def fn (* params):
		print (params)
			
		param_1 = params [0]
		print (param_1)

		assert (param_1 == 3)
	
		return 99
		
	returns = cycle.params (
		fn, 
		[
			[ 1 ],
			[ 2 ],
			[ 3 ]	
		],
		delay = 1
	)

	assert (returns == 99)

checks = {
	"check 1": check_1
}




#