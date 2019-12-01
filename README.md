# Mental Health Support (README.md)
**Mental Health Support** is a lightweight web app designed to help users who struggle with mental health and wellbeing, with a low
barrier-to-entry mental health tracking journal/tool and available resources. The app does not get users bogged down with details,
rather focusing on simplicity and minimalism.

## Motivation
This project exists as I am acutely aware of issues related to mental health and wellbeing, having faced them most my life, and
having many loved ones with similiar hardships. I was inspired by the Google Trusted Contacts app when I first saw it a couple
years ago https://contacts.google.com/trustedcontacts/, and wanting to reduce the mental health stigma and provide support for
others, as with depression for example it can be hard to reach out for help due to percieved/real barriers. The project design and
scope was beta tested with several individuals to make sure that it's potential for beneficial impact could be generalized to a
wide audience.

## Build Status
The project currently operates in the intended manner, i.e., a user can register/login, write/read journal entries, and
register/contact a Support Contact, all in a mobile-optimized web app. Desired elements to be added in the future include: web.apk
integration (so that users could download the app to their mobile), and a data export feature (so that users could download their
data either for their own needs, or to possible share with a mental health professional). I would also love to coordinate with a
mental health professional in the future to build out resources and better structured journaling methodology (with improved
impact).

## Code/Tech/Framework Used
Python Flask backend (controller), SQL database (model), bootstrap/jinja-styled html webpages (view).

## Screenshots
The homepage features a minimalist, clean design, and gets the user directly to the key function of the app: writing a
journal entry: ![Image of the main screen (homepage)](/static/images/mainscreen.png "Main Screen")

## Features
This web app is unique in that it uses the Cognitive Distortions framework for mental health journaling. By structuring the
journal entry input in this manner, it allows for constructive journaling rather than boundless self-writes that might
prove detrimental in allowing users to negatively thought spiral. The Support Contact implementation is something that I
have never encountered before. In times of mental illness, perceieved/real barriers can prevent an individual from reaching
out to their support network. By having a direct push button contact method for the Support Contact, this helps mitigate that
problem.

## Initiatlization
This project currently lives in the CS50 IDE. To initiatlize, execute "Flask Run" in a command terminal that has
been opened up to the main folder where all the files/sub-folders are stored.

## How to use?
1. User is directed to log-in screen if not logged in. Select "Register" at top right.
2. Register for an account. Upon successful registration, user will be logged in.
3. The homepage is the 'Write' page, where user can write a journal entry. At least one of the 5 text fields must be filled out.
4. The user will be directed to the 'Read' page (also available in the navbar). User can select an entry to read.
5. Once an entry is selected, user will be directed to their journal entry based on that selection.
6. The 'Get Help' page features a list of helpful resources. If logged in, the user also has the option to contact their Support Contact directly via a button push.
7. The user can change their password/support contact in the 'About' page.
8. They can also choose to delete all their data if they click the button at the very bottom of the 'About' page and then confirm on the 'Delete' page.

Video walkthrough available here: <https://www.youtube.com/watch?v=EBItSfOlaXU>

## Credits
Resources used are commented throughout the project. I would like to thank my friends who helped try out the web app.