import os
import subprocess

def exec_sys_cmd(sys_cmd):
  sp = subprocess.Popen(sys_cmd.split(), stdout=subprocess.PIPE)
  out, err = sp.communicate()
  if out is not None: out = out.decode('utf-8').rstrip('\n')
  if err is not None: err = err.decode('utf-8').rstrip('\n')
  assert err is None or err == '', f'{err} when running \"{sys_cmd}\".'
  return (out)


def boot_remote_host(wol_cmd, local_nic, remote_host, remote_host_mac):
  boot_cmd    = [wol_cmd, '-i', local_nic , remote_host_mac]

  for i in range (int(me.config['REMOTE_BOOT_MAX_TIME'])):
    time.sleep(1)
    output,error = me.exec_sys_cmd(detect_cmd)
    me.write_log(log_file, '[' + me.config['REMOTE_HOST'] + '] : ' + output + error)
    if me.config['REMOTE_HOST'] in output:
      me.write_log(log_file, 'Remote Host Started :' + me.config['REMOTE_HOST'])
      return


if __name__ == "__main__":
  print (exec_sys_cmd("cmd"))
  pass


