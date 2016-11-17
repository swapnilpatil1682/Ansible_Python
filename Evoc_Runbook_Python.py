from commands import *

def run_command(cmd):
    print 'Running: "%s"' % cmd
    status, text = getstatusoutput(cmd)
    exit_code = status >> 8 # high byte
    signal_num = status % 256 # low byte
    print 'Status: x%04x' % status
    print 'Signal: x%02x (%d)' % (signal_num, signal_num)
    print 'Exit  : x%02x (%d)' % (exit_code, exit_code)
    print 'Core? : %s' % bool(signal_num & (1 << 8)) # high bit
    print 'Output:'
    print text
    print

#run_command('cd /root/; tar -xf azkaban-solo-server-2.5.0.tar.gz')

print'***************** Untar the azkaban folder ***************************************'
run_command('cd /root/; tar -xf azkaban-solo-server-2.5.0.tar.gz')

print'***************** Create a linux Group nzhdusr *************************************'
run_command('groupadd nzhdusr')

print'***************** Create a linux User nzhdusr *************************************'
run_command('useradd -g nzhdusr nzhdusr')

print'***************** Assign Owner and group to /evoc folder **************************'
run_command('sudo chown nzhdusr /evoc')
run_command('sudo chgrp nzhdusr /evoc')

print'**** Create local application metadata directory and assign ownership to nzhdusr ***';
run_command('sudo -u nzhdusr mkdir -p /home/nzhdusr/dev/evoc ;')

print'**** Change user and go to that dir ************************************************';
run_command('su nzhdusr -c cd /home/nzhdusr/dev/evoc/')

print'**** Copy the build file *************************************************************';
run_command('cp /evoc/build/target/evoc-1.0.0-SNAPSHOT.tar.gz /home/nzhdusr/dev/evoc/')

print'**** Untar and remove tar file ************************************************';
run_command('cd /home/nzhdusr/dev/evoc/; tar -xf evoc-1.0.0-SNAPSHOT.tar.gz; rm -f evoc-1.0.0-SNAPSHOT.tar.gz ')


run_command('cd /home/nzhdusr/dev/evoc/; rm -rf current')

print'**** Create current symlink to the extract folder in the same directory  *********';
run_command('ln -s /home/nzhdusr/dev/evoc/evoc-1.0.0-SNAPSHOT /home/nzhdusr/dev/evoc/current')

print'**** Make all shell scripts executable ********************************************';
run_command('find ./ -type d -exec chmod 755 {} \; find ./ -name "*.sh" -type f -exec chmod +x {} \;')

print'**** Run setups  ******************************************************************';
run_command('su nzhdusr -c cd /home/nzhdusr/dev/evoc/current/releases/; bin/setup.sh all 0.0.0;bin/setup.sh all 0.0.1')
run_command('')
