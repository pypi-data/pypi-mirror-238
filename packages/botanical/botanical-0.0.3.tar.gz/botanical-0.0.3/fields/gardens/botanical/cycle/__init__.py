

import time

'''
	cycle.presents ([])
	cycle.presents ([], {})
'''
class presents:
	def __init__ (this, * positionals):
		this.positionals = positionals [0]
		
		if (len (positionals) >= 2):
			this.keywords = positionals [1]
		else:
			this.keywords = {}


def params (fn, fn_params, delay = 1, loop = 0):
	try:
		return fn (* fn_params [ loop ]);			
	except Exception as E:
		print ("cycle didn't work.", E)

	time.sleep (1)
	
	return params (fn, fn_params, loop = loop + 1)


'''

'''
def loops (
	* positionals, 
	** keywords
):
	fn = positionals [0]
	fn_presents = positionals [1] 
	
	this_loops = keywords ["loops"],
	
	if ("loops" in keywords):
		this_loops = keywords ["loops"]
	else:
		this_loops = 1
	
	if ("delay" in keywords):
		this_delay = keywords ["delay"]
	else:
		this_delay = 1
		
	if ("loop_number" in keywords):
		this_loop_number = keywords ["loop_number"]
	else:
		this_loop_number = 1

	print ("keywords:", keywords)
	
	if (this_loop_number > this_loops):
		raise Exception (f"The loop limit was reached.")

	try:
		return fn (
			* fn_presents.positionals,
			** fn_presents.keywords
		);			
	except Exception as E:
		print ("cycle didn't work.", Exception)

	time.sleep (float (this_delay))
	
	return loops (
		fn, 
		fn_presents, 
		
		loops = this_loops,
		delay = this_delay,
		
		loop_number = this_loop_number + 1
	)
	
