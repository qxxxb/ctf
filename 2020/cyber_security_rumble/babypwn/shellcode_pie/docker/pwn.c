#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

#define MD5_DIGEST_LENGTH 16

unsigned char char_to_repr(char in) {
    if (in >= '0' && in <= '9')
	return in - '0';
    if (in >= 'a' && in <= 'f')
	return in - 'a' + 0xa;
    if (in >= 'A' && in <= 'F')
	return in - 'A' + 0xa;
    assert("not in hex digit range" && 0);
}

void hex_to_binary(char *in, unsigned char* out, size_t length) {
    size_t i;
    assert("length must be even" && (length % 2) == 0);

    length /= 2;
    for (i = 0; i < length; i++) {
        out[i] = char_to_repr(in[i * 2]) << 4 | char_to_repr(in[i * 2 + 1]);
    }
}

int check_user_hash(char* flag) {
    unsigned char user_md5[MD5_DIGEST_LENGTH * 2 + 1];
    unsigned char flag_md5[MD5_DIGEST_LENGTH];

    printf("&flag_md5: %p\n", &flag_md5);
    printf("&user_md5: %p\n", &user_md5);

    gets(user_md5);
    hex_to_binary(user_md5, user_md5, strlen(user_md5));

    return 0;
}

int main() {
    char flag[0x500];
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);

    printf("main:      %p\n", main);
    printf("cuh:       %p\n", check_user_hash);

    printf("&flag:     %p\n", &flag);

    /* read flag */
    int fd = open("flag.txt", O_RDONLY);
    assert("unable to open flag file" && fd >= 0);
    flag[read(fd, flag, sizeof(flag))] = '\0';
    close(fd);

    puts("Prompt goes here");

    /* if md5 is correct, print flag */
    if(check_user_hash(flag)) {
        puts(flag);
    } else {
        puts("nope");
    }

    return 0;
}
