import os


def nginx_container(host_port):
    try:
        if host_port == None:
            os.system("docker run -it -d --name nginx_container nginx")
        else:
            
           os.system(f"docker run -it -d --name nginx_container -p {host_port}:80 nginx")
    except:
        print("Could not execute command")
        
def ubuntu_container(host_port, container_port):
    try:
        if host_port == None:
           os.system("docker run -it -d --name ubuntu_container ubuntu")
        else:
            os.system(f"docker run -it -d --name ubuntu_container -p {host_port}:{container_port} ubuntu")
    except:
        print("Could not execute command")