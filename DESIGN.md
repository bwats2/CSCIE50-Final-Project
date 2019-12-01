# Mental Health Support (DESIGN.md)
This web app, per David's suggestion, utilized PSet8 source code as a starting point. Namely, the work that I had done for
register/login and form submission (since I hadn't managed to finish the PSet past this point).

## Model
A SQLite Database (with the CS50IDE phpLiteAdmin) was implemented to structure the 3 relational tables. These tables consist of
"users" (storing userid, username, hashed password), "journal" (storing the journal content, timestamp, and mental health score),
and "supportcontact" (storing the user's Support Contact information: name and email). The tables were structured in this manner
with the userid being the foreign key to link them, in order to organize the data and ensure data integrity. The "users" table is
designed to be relatively untouched after registration, except for password updates, since it contains the key information
that allows this web app to run on the client side. The "supportcontact" table is also relatively untouched, other than updates.
On the other hand, the "journal" table has frequent insertions, and would have been a mess had this not been broken out. Care was
also taken against SQL injection attacks per the standards set in class with named paramters. For journal entry, I relied on the
'text' data type to ensure that users would have enough room for content. I struggled a little bit with date/time stamp, but using
Python was able to correct this (although I am still storing SQL UTC timestamp, python datetime, and epoch time, in case I decided
to change this in the future). For my purposes, the SQL/Python queries are also very easy to returned lists suitable for Jinja,
which was a great benefit of this data model.

## View
In addition to HTML, Bootstrap (css) and Jinja (configured by default in flask) were used for templating. Boostrap was especially
helpful for styling visual elements that would have tricky too otherwise (such as pretty forms, and the nav-bar). Other
features that I discovered, such as Bootstrap's built-in quick validation for email addresses were also very useful. Jinja,
in combination with Python SQL queries, proved very useful as I was able to take the lists that had been returned from the
queries and simply pass them to the templates. Jinja2 then allowed for for/if loops which provided enhanced functionality
such as displaying items only if someone was logged in. I strayed from Javascript because of my lack of comfort (it was
one of the areas of class that I felt moved far too quickly), but I did discover how to use Javascript to implement a
"go back" button, which was very useful. I was unable to figure out how to modify Jinja2 to recognize '/r' as a linebreak.

## Controller
I used Python Flask to serve my web app, mainly because it is what we had used in class and is what I was most familiar
with (internet research did not provide anything to dissuade me from using Flask). Similiar to both PSet7 and PSet8, I
created different routes for different functionality in my webapp (after mapping everything out on paper). The routes relied
heavily on the login decorator, and the get v. post differentiation via if-else statements. Template returns were useful when I
did not necessarily want to inform the user of a page change; conversely, template redirects were useful to notify them of a
change (as the route titles implied function, and if I can figure out the web.apk, the user is notified of such changes when the
mobile browser is run on fullscreen). I did have several 'wants' that I tried to implement via Python, but struggled. I tried to
CORS access issue with CORS-FLASK module, but could not make it work (as it was key to a true webapp/web.apk implementation). I
spent time trying to implement OPENSSL and created self-signed certificates, but realized that was silly as the cloud IDE has
its own certificate, and this is a development instance running from an IDE.