#!/usr/bin/env python3

import re

def main(arguments):
	config=dict()
	positional=[]
	pattern=re.compile(r"(?:-(?:a|b|d|f|h|x|i|k|r|v|V)|--(?:alpha|beta|delta|file|help|initial|kernel|list-methodologies|methodology|report|variance|version))(?:=.*)?$")
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
			if option=="alpha":
				if attached_value is not None:
					config["alpha"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["alpha"]=None
					consuming,needing,wanting="alpha",1,1
			elif option=="beta":
				if attached_value is not None:
					config["beta"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["beta"]=None
					consuming,needing,wanting="beta",1,1
			elif option=="delta":
				if attached_value is not None:
					config["delta"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["delta"]=None
					consuming,needing,wanting="delta",1,1
			elif option=="file":
				if attached_value is not None:
					config["file"]=[attached_value]
					consuming,needing,wanting="file",0,8
					attached_value=None
				else:
					config["file"]=[]
					consuming,needing,wanting="file",1,9
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
					config["initial"]=[attached_value]
					consuming,needing,wanting="initial",0,1
					attached_value=None
				else:
					config["initial"]=[]
					consuming,needing,wanting="initial",1,2
			elif option=="kernel":
				if attached_value is not None:
					config["kernel"]=[attached_value]
					consuming,needing,wanting="kernel",0,8
					attached_value=None
				else:
					config["kernel"]=[]
					consuming,needing,wanting="kernel",1,9
			elif option=="list-methodologies":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "list-methodologies"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["list-methodologies"]=True
			elif option=="methodology":
				if attached_value is not None:
					config["methodology"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["methodology"]=None
					consuming,needing,wanting="methodology",1,1
			elif option=="report":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "report"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["report"]=True
			elif option=="variance":
				if attached_value is not None:
					config["variance"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["variance"]=None
					consuming,needing,wanting="variance",1,1
			elif option=="version":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "version"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["version"]=True
			elif option=="a":
				if attached_value is not None:
					config["alpha"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["alpha"]=None
					consuming,needing,wanting="alpha",1,1
			elif option=="b":
				if attached_value is not None:
					config["beta"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["beta"]=None
					consuming,needing,wanting="beta",1,1
			elif option=="d":
				if attached_value is not None:
					config["delta"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["delta"]=None
					consuming,needing,wanting="delta",1,1
			elif option=="f":
				if attached_value is not None:
					config["file"]=[attached_value]
					consuming,needing,wanting="file",0,8
					attached_value=None
				else:
					config["file"]=[]
					consuming,needing,wanting="file",1,9
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
					config["initial"]=[attached_value]
					consuming,needing,wanting="initial",0,1
					attached_value=None
				else:
					config["initial"]=[]
					consuming,needing,wanting="initial",1,2
			elif option=="k":
				if attached_value is not None:
					config["kernel"]=[attached_value]
					consuming,needing,wanting="kernel",0,8
					attached_value=None
				else:
					config["kernel"]=[]
					consuming,needing,wanting="kernel",1,9
			elif option=="r":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "report"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["report"]=True
			elif option=="v":
				if attached_value is not None:
					config["variance"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["variance"]=None
					consuming,needing,wanting="variance",1,1
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
