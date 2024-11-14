How to use localization:

1. Init a localization for a certain language. 
<b>pybabel init -i locales/messages.pot -d locales -D messages -l en</b>

2. Creating template:
<i>pybabel extract -k _:1,1t -k _:1,2 -k __ --input-dirs=. -o locales/messages.pot</i>

3. Creating localized templates files for all localizations:
<i>pybabel update -d locales -D messages -i locales/messages.pot</i>

4. Compiling files from .mo to .po:
<i>pybabel compile -d locales -D messages</i>

