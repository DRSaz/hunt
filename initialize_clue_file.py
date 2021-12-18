import json
hunt_file = "./hunt_data"
hunt_data = {}


clue_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for c in clue_letters:
    hunt_data[c]= "Not Found"
    
    
with open(hunt_file,'w') as f:
    json.dump(hunt_data,f,indent=4)
with open(hunt_file,'r') as f:
    clues = json.load(f)
print(hunt_data)
