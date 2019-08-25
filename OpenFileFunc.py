import subprocess


def openfile(File,Line=""):
    Path = File+":"+Line
    subprocess.Popen(['code', '-g', Path])

openfile('Parse_Code.txt','43')
#openfile('Parse_Code.txt')
#openfile('/Users/jass/Documents/Master Summer/Parse_Code.txt')
#openfile('Test.code-workspace')
