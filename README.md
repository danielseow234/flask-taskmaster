# flask-taskmaster
Simple flask website that allows user to create and remove tasks on a todo list.

I used the Flask python package as the backend of the website. I didn't use any CSS as I was kinda lazy so the website looks really blank. I bodged a simple login and sign up system that stores the user details and tasks on an SQLite database, and I used the SQLAlchemy module in python. Flask has a module named Flask-login, which adds user authentication to pages, and adds many more features. Since I didn't use that I had to come up with a way to secure the website for users. 

At first, the link to a specific user's tasks were linked using "/home/'username'". This would be terrible, as other users could simply find out another user's username, and access their home page. To counter this I implemented a randomly generated user ID, that could be used for the link instead like "/home/'user ID'". This isn't the most secure method, as a user's ID could be copied from their web browser, or it could be pulled from the database if there were a breach in security.

If I were to re-do this project, I would definitely implement the flask-login module, and I would use the login-authenticator to secure users' data.
