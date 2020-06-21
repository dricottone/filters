#!/usr/bin/env python3

import re

def main(arguments):
	config=dict()
	positional=[]
	pattern=re.compile(r"(?:-(?:d|h|x|i|m|n|o|r|s|v|V)|--(?:delta|distribution|help|initial|list-distributions|mu|number|offset|report|sigma|version))(?:=.*)?$")
	consuming,needing,wanting=None,0,0
	attached_value=None
	while len(arguments) and arguments[0]!="--":
		if consuming is not None:
			if config[consuming] is None:
				config[consuming]=arguments.pop(0)
			else:
				config[consuming].append(arguments.pop(0))
			needing-=1
			wanting-=1
			if wanting==0:
				consuming,needing,wanting=None,0,0
		elif pattern.match(arguments[0]):
			option = arguments.pop(0).lstrip('-')
			if '=' in option:
				option,attached_value=option.split('=',1)
			if option=="delta":
				if attached_value is not None:
					config["delta"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["delta"]=None
					consuming,needing,wanting="delta",1,1
			elif option=="distribution":
				if attached_value is not None:
					config["distribution"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["distribution"]=None
					consuming,needing,wanting="distribution",1,1
			elif option=="help":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "help"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["help"]=True
			elif option=="initial":
				if attached_value is not None:
					config["initial"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["initial"]=None
					consuming,needing,wanting="initial",1,1
			elif option=="list-distributions":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "list-distributions"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["list-distributions"]=True
			elif option=="mu":
				if attached_value is not None:
					config["mu"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["mu"]=None
					consuming,needing,wanting="mu",1,1
			elif option=="number":
				if attached_value is not None:
					config["number"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["number"]=None
					consuming,needing,wanting="number",1,1
			elif option=="offset":
				if attached_value is not None:
					config["offset"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["offset"]=None
					consuming,needing,wanting="offset",1,1
			elif option=="report":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "report"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["report"]=True
			elif option=="sigma":
				if attached_value is not None:
					config["sigma"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["sigma"]=None
					consuming,needing,wanting="sigma",1,1
			elif option=="version":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "version"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["version"]=True
			elif option=="d":
				if attached_value is not None:
					config["delta"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["delta"]=None
					consuming,needing,wanting="delta",1,1
			elif option=="h":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "help"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["help"]=True
			elif option=="x":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "help"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["help"]=True
			elif option=="i":
				if attached_value is not None:
					config["initial"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["initial"]=None
					consuming,needing,wanting="initial",1,1
			elif option=="m":
				if attached_value is not None:
					config["mu"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["mu"]=None
					consuming,needing,wanting="mu",1,1
			elif option=="n":
				if attached_value is not None:
					config["number"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["number"]=None
					consuming,needing,wanting="number",1,1
			elif option=="o":
				if attached_value is not None:
					config["offset"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["offset"]=None
					consuming,needing,wanting="offset",1,1
			elif option=="r":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "report"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["report"]=True
			elif option=="s":
				if attached_value is not None:
					config["sigma"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["sigma"]=None
					consuming,needing,wanting="sigma",1,1
			elif option=="v":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "version"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["version"]=True
			elif option=="V":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "version"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["version"]=True
		else:
			positional.append(arguments.pop(0))
	if needing>0:
		message=(
			f'unexpected end while parsing "{consuming}"'
			f' (expected {needing} values)'
		)
		raise ValueError(message) from None
	for argument in arguments[1:]:
		positional.append(argument)
	return config,positional

if __name__=="__main__":
	import sys
	cfg,pos = main(sys.argv[1:])
	cfg = {k:v for k,v in cfg.items() if v is not None}
	if len(cfg):
		print("Options:")
		for k,v in cfg.items():
			print(f"{k:20} = {v}")
	if len(pos):
		print("Positional arguments:", ", ".join(pos))
