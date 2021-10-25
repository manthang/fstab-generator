
import os
from os import path
import sys
import stat
import socket
import yaml

def validate_address(address):
  try:
    # Check if address is resolvable by local DNS client or /etc/hosts file
    socket.gethostbyname(address)
    return True

  except:
    try:
      # Check if address is an IPv4 address
      octets = address.split(".")
      
      if len(octets) != 4:
        print("The address " + address + " is not valid.")
        return False

      for octet in octets:
        if not isinstance(int(octet), int):
          print("The address " + address + " is not valid.")
          return False
        if int(octet) < 0 or int(octet) > 255:
          print("The address " + address + " is not valid.")
          return False
    
      return True

    except:
      return False

def validate_input(list_of_dicts):
  devices = []
  mount_points = []

  for k, v in list_of_dicts:

    if 'export' in v:
      ### Check if NFS server has a valid hostname or IP address
      if validate_address(k):
        devices.append(k)

      ### Mount points need to be existed and not duplicate.
      if v['export'] in mount_points:
        print("Please use a unique mount point. Duplicate detected is: " + v['export'])
      elif not path.exists(v['export']):
        print("Please create a mount point first. It does not exist: " + v['export'])
      else:
        mount_points.append(v['export'])
    
    else:
      ### Check if filesystems are on block devices.
      if stat.S_ISBLK(os.stat(k).st_mode):
        devices.append(k)
      else:
        print("This file path is not a block device: " + k)
      
      ### Mount points need to be existed and not duplicate.
      if v['mount'] in mount_points:
        print("Please use a unique mount point. Duplicate detected is: " + v['mount'])
      elif not path.exists(v['mount']):
        print("Please create a mount point first. It does not exist: " + v['mount'])
      else:
        mount_points.append(v['mount'])

  if len(mount_points) == len(devices):
      return True

  return False

### Load the YAML input file
yaml_file = sys.argv[1]
if os.path.exists(yaml_file):
  with open(yaml_file,'r') as f_input:
    src_dict = yaml.safe_load(f_input)

### Write the parsed output as a fstab file format
with open(("./fstab"),'w') as f_output:

  for root_key, value in src_dict.items():
    if validate_input(value.items()):

      for k, v in value.items():

        ### Construct nfs records 
        if "nfs" in v.values():
          if "options" in v.keys():
            f_output.write(" ".join([":".join([k,v['mount']]),\
                          v['export'],\
                          v['type'],\
                          ",".join(v['options']),\
                          "\n"]))
          else:
            f_output.write(" ".join([":".join([k,v['mount']]),\
                          v['export'],\
                          v['type'],\
                          "defaults",\
                          "\n"]))
        ### Construct other filesystem (xfs, ext4, etc) records 
        else:
          if "options" in v.keys():
            f_output.write(" ".join([k,v['mount'],\
                          v['type'],\
                          ",".join(v['options']),\
                          "\n"]))
          else:
            f_output.write(" ".join([k,v['mount'],\
                          v['type'],\
                          "defaults",\
                          "\n"]))
