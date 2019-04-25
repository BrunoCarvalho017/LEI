import sys, json

json_file = open(sys.argv[1])
json_data = json.load(json_file)

dataToSendBack = "Hello from analisador"
print(json_data)
sys.stdout.flush()