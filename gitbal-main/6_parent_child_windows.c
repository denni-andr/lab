#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAX_SIZE 100

int main() {
    int p2c[2]; // Pipe for Parent-to-Child communication
    int c2p[2]; // Pipe for Child-to-Parent communication

    // Create pipes
    if (pipe(p2c) == -1 || pipe(c2p) == -1) {
        perror("Pipe failed");
        exit(1);
    }

    pid_t pid = fork();

    if (pid < 0) {
        perror("Fork failed");
        exit(1);
    } 
    else if (pid > 0) { // Parent process
        close(p2c[0]); // Close read end of p2c
        close(c2p[1]); // Close write end of c2p

        // Parent sends a message to the child
        char parent_msg[MAX_SIZE];
        printf("Parent, enter your message: ");
        fgets(parent_msg, MAX_SIZE, stdin);
        parent_msg[strcspn(parent_msg, "\n")] = '\0'; // Remove newline character
        write(p2c[1], parent_msg, strlen(parent_msg) + 1);
        close(p2c[1]); // Close write end after sending

        // Wait for child to process the message
        wait(NULL); 

        // Prompt parent to enter child’s response
        char child_response[MAX_SIZE];
        printf("Child, enter your response: ");
        fgets(child_response, MAX_SIZE, stdin);
        child_response[strcspn(child_response, "\n")] = '\0'; // Remove newline character
        write(c2p[1], child_response, strlen(child_response) + 1);
        close(c2p[1]); // Close write end after sending

        // Parent reads the child's response and outputs it
        read(c2p[0], child_response, MAX_SIZE);
        printf("Parent received: %s\n", child_response);
        close(c2p[0]); // Close read end after receiving
    } 
    else { // Child process
        close(p2c[1]); // Close write end of p2c
        close(c2p[0]); // Close read end of c2p

        // Child reads the parent's message
        char parent_msg[MAX_SIZE];
        read(p2c[0], parent_msg, MAX_SIZE);
        printf("Child received: %s\n", parent_msg);
        close(p2c[0]); // Close read end after receiving

        // Child reads the response back from the parent
        char child_response[MAX_SIZE];
        read(c2p[0], child_response, MAX_SIZE);
        close(c2p[1]); // Close write end after receiving

        exit(0);
    }

    return 0;
}
