import click
import subprocess

@click.command()
def test():
    """ Test the command can execute"""
    subprocess.run(["echo","hello world"])

@click.command()
def start():
    """Start your vm"""
    subprocess.run(["gcloud", "compute" , "instances", "start",
                "lewagon-data-eng-vm-le-baronysard"])

@click.command()
def stop():
    """Stop your vm"""
    subprocess.run(["gcloud", "compute" , "instances", "stop",
                "lewagon-data-eng-vm-le-baronysard"])

@click.command()
def connect():
    """Connect to your vm"""
    subprocess.run(["code", "--folder-uri",
        "vscode-remote://ssh-remote+aloysbernardwagon@35.233.108.68/home/aloysbernardwagon/code/le-baronysard"])
