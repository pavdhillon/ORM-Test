user_input = input("Enter your username: ")
query = "SELECT * FROM users WHERE username = '" + user_input + "';"
execute_query(query)  # This can be exploited
