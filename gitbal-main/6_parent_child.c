#include <stdio.h>
#include <unistd.h>
#include <string.h>

#define MAX_SIZE 100

int main() {
    int p2c[2], c2p[2];
    pid_t pid;
    char msg[MAX_SIZE], reply[MAX_SIZE];

    if (pipe(p2c) == -1 || pipe(c2p) == -1 || (pid = fork()) < 0) {
        perror("Error");
        return 1;
    }

    if (pid) {  // Parent
        close(p2c[0]); close(c2p[1]);
        printf("Parent, enter your message: ");
        fgets(msg, MAX_SIZE, stdin);  // Take input from parent
        msg[strcspn(msg, "\n")] = 0;  // Remove the newline character
        write(p2c[1], msg, strlen(msg) + 1);
        read(c2p[0], reply, MAX_SIZE);
        printf("Parent received: %s\n", reply);
    } else {  // Child
        close(p2c[1]); close(c2p[0]);
        read(p2c[0], reply, MAX_SIZE);
        printf("Child received: %s\n", reply);
        printf("Child, enter your response: ");
        fgets(msg, MAX_SIZE, stdin);  // Take input from child
        msg[strcspn(msg, "\n")] = 0;  // Remove the newline character
        write(c2p[1], msg, strlen(msg) + 1);
    }

    return 0;
}
