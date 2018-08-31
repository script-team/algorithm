import pexpect


def ssh_command(user, host, password, command):
    ssh_new_key = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s' % (user, host, command))
    i = child.expect([pexpect.TIMEOUT, ssh_new_key, 'password: '])
    if i == 0:
        print('ERROR!')

        print('SSH could not login. Here is what SSH said:')

        print(child.before, child.after)

        return None
    if i == 1:
        child.sendline('yes')
        child.expect('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0:
            print('ERROR!')

            print('SSH could not login. Here is what SSH said:')

            print(child.before, child.after)

            return None
    child.sendline(password)
    return child


if __name__ == "__main__":
    while True:
        children = ssh_command("user_name", "host_ip", "password", "cat /proc/meminfo")
        if children is not None:
            break
        else:
            print('trying to reconnect!')
        children.expect(pexpect.EOF)
    mem = children.before.decode()
    print(mem)
