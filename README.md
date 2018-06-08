# kiwi_currency_converter

#
# Hi everyone, who is so blessed to read my code! GLHF
#


#
# Installation
#
1. Prepare your Python 3 environment
2. Install dependencies *pip -r requirements.txt*
3. Get executable permissions to CLI *chmod u+x currency_converter.py*
4. Start uWSGI
5. Start NGINX

#
# Pros
#
1. On the fly data
2. None hardcoded data

#
# Cons
#
1. If cache DB is empty, will some response time degradation
2. If some of 2 source service die, it will break for pieces
3. It wants much more comments, but code is understandable (IMHO)

#
# Some "nice-to-have"
#
1. Support of different source
2. Much more testing, I wrote it after work, so my morality was in very low level :D

#
# Missing
#
1. uWSGI ini file
2. NGINX config

#
# P.S.
#
# I don't like PEP-8 standard, I love my style :)
# Sorry for all code in master branch. I forget switch to devel branch. And when I uploaded code, I got it...

