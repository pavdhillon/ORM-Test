import json

# Load the JSON data from the file
with open('response.json', 'r') as file:
    data = json.load(file)

# Initialize sums
input_token_sum = 0
output_token_sum = 0

# Iterate through the JSON structure
for item in data:
    if 'Output' in item:
        for output in item['Output']:
            input_token_sum += output.get('InputToken', 0)
            output_token_sum += output.get('OutputToken', 0)

# Print the results
print(f"Sum of all InputToken values: {input_token_sum}")
print(f"Sum of all OutputToken values: {output_token_sum}")
