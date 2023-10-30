# newcat

print (cat) only new lines in files (after previous run of newcat). This is useful to parse recent log records.

## Install
~~~
pipx install newcat
~~~

## Example
~~~bash
$ echo This is line 1 > /tmp/test.log

# works like normal /bin/cat now
$ newcat /tmp/test.log 
This is line 1

# only new lines are printed
$ echo This is line 2 >> /tmp/test.log
$ newcat /tmp/test.log 
This is line 2

# no new lines => nothing on stderr
$ newcat /tmp/test.log 

# despite file is having two lines
$ cat /tmp/test.log 
This is line 1
This is line 2
~~~

## How does this magic work?
newcat stores some info about file (including position in file) in *state file*. Default state file is `/tmp/.newcat.state`, but can be overriden with `NEWCAT_STATE` environment variable or `-s` / `--state` option. Normally, newcat prints file content starting from this position (which was saved before), thus lines which were already printed before, will not be printed on new newcat run.

Sometime file content it rewritten (e.g. after `echo New content > /tmp/test.log`). To detect this situation newcat checks two things:
- file inode changed
- file size is less then old printed position

if any of these conditions are met, file considered as rewritten and newcat prints it from the beginning.
Note: this is not absolutely reliable, and there is a chance that sometimes newcat will not detect when file is overwritten.


