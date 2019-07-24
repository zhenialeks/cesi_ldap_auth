import os, sys

activate_this='/opt/cesi/venv/bin/activate_this.py'

sys.path.append('/opt/cesi/cesi')

with open(activate_this) as file_:
	exec(file_.read(), dict(__file__=activate_this))


from run import configure

app, _ = configure('/opt/cesi/defaults/cesi.conf.toml')

application = app