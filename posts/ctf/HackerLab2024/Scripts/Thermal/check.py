dangerous_functions = ['pcntl_alarm','pcntl_fork','pcntl_waitpid','pcntl_wait','pcntl_wifexited','pcntl_wifstopped','pcntl_wifsignaled','pcntl_wifcontinued','pcntl_wexitstatus','pcntl_wtermsig','pcntl_wstopsig','pcntl_signal','pcntl_signal_get_handler','pcntl_signal_dispatch','pcntl_get_last_error','pcntl_strerror','pcntl_sigprocmask','pcntl_sigwaitinfo','pcntl_sigtimedwait','pcntl_exec','pcntl_getpriority','pcntl_setpriority','pcntl_async_signals','error_log','system','exec','shell_exec','popen','proc_open','passthru','link','symlink','syslog','ld','mail']

result = ["exec","system","passthru","shell_exec","escapeshellarg","escapeshellcmd","proc_close","proc_open","popen","show_source","posix_kill","posix_mkfifo","posix_getpwuid","posix_setuid","posix_setpgid","posix_setsid","posix_setgid","posix_seteuid","posix_setegid","exec_p","shell_"]

yay = []

for i in dangerous_functions:
    if i not in result:
        yay.append(i)
    
print(yay)
