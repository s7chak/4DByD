import subprocess


def openfile(File,Line=""):
    Path = File+":"+Line
    subprocess.Popen(['code', '-g', Path])
