#!/usr/bin/env python
# encoding:utf-8

#################################
# runner wrapper for supervisor
#################################

import commands
import re
import subprocess
import signal
import sys

IMAGE_TAG = "{{rabbitmq_img_name}}:{{rabbitmq_img_tag}}"
SEPERATOR = '\t|\s{2,}'

CONTAINER_NAME = "rabbitmq"
CONTAINER_ID = ""


def enum(**enums):
    return type('Enum', (), enums)


MODE = enum(CREATE="create", START="start", ATTACH="attach")


def main():
    mode = MODE.CREATE
    container_id = ""

    cmd = "docker container ls -a"
    output = get_command_output(cmd)
    if len(output) > 1:
        for line in output[1:]:
            items = re.split(SEPERATOR, line)
            if items[-1] == CONTAINER_NAME:
                if items[4].lower().startswith("up"):
                    mode = MODE.ATTACH
                elif items[4].lower().startswith("exited"):
                    mode = MODE.START
                container_id = items[0]
                break

    if mode == MODE.CREATE:
        cmd = "docker run " \
              "--name=%s " \
              "-h {{ ansible_hostname }} " \
              "-p 25672:25672 -p {{ rabbitmq_port }}:5672 -p 15672:15672 -p 5671:5671 -p 4369:4369 " \
              "-e RABBITMQ_VM_MEMORY_HIGH_WATERMARK={{ rmq_vm_mem_hi_watermark }} " \
              "-v {{ rmq_data_dir_on_host }}:/var/lib/rabbitmq/:rw " \
              "-v /etc/hosts:/etc/hosts:rw " \
              "%s" % (CONTAINER_NAME, IMAGE_TAG)
    elif mode == MODE.START:
        cmd = "docker container start -a %s" % container_id
    elif mode == MODE.ATTACH:
        cmd = "docker container attach %s" % container_id
    else:
        raise Exception("unknown execute mode")

    proc = subprocess.Popen(cmd.split())

    global CONTAINER_ID
    if container_id:
        CONTAINER_ID = container_id
    else:
        # get container id from docker ps
        cmd = "docker ps"
        output = get_command_output(cmd)
        if len(output) > 1:
            for line in output[1:]:
                items = re.split(SEPERATOR, line)
                if items[-1] == CONTAINER_NAME:
                    CONTAINER_ID = items[0]
                    break
    # wait until subprocess return
    try:
        proc.wait()
    except KeyboardInterrupt:
        exit_hook(None)
    except Exception:
        exit_hook(None)


def get_command_output(cmd):
    status, output = commands.getstatusoutput(cmd)
    if status:
        raise Exception("execute command error")
    else:
        return output.split('\n')


def exit_hook(sig, func=None):
    if CONTAINER_ID:
        cmd = "docker container stop %s" % CONTAINER_ID
        subprocess.call(cmd.split())


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, exit_hook)
    main()
