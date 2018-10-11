from directory import GUDirectory

directory = GUDirectory()
results = directory.simple_search("derek acosta")
for result in results:
	print(result)
