#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/*
 * compiled with:
 * gcc -m32 -fno-stack-protector -no-pie right_address.c -o right_address
 *
 */

#define MSG_LEN 255
#define ADDR_LEN 100
#define NUM_OPTIONS 6

char* order_arr[NUM_OPTIONS] = {
                        "Order 100 units of sodium bicarbonate",
                        "Order 100 units of ethylene glycol",
                        "Order 100 units of acetylsalicylic acid",
                        "Order 100 units of ethylchlorohol permanganesium",
                        "Order 100 units of aluminum chlorohydrate",
                        "Exit"
};

void print_spy_instructions() {
    char msg[MSG_LEN];
    FILE* messages = fopen("flag", "r");
    if(messages == NULL) {
        printf("Trouble getting messages file, red alert!\n");
    }
    fgets(msg, MSG_LEN, messages);
    printf("%s", msg);
    return;
}

void process_order(int order_num) {
    char address[ADDR_LEN];
    int purchase_num = 0;
    printf("Currently ordering: %s\n", order_arr[order_num - 1]);
    printf("Enter delivery address: ");
    gets(address);
    printf("Processing...\n");
    // Pretend to spit out a fake error to unsuspecting companies who try to make a purchase from us
    sleep(5);
    printf("Looks like we are not allowed to deliver to that address due to legal restrictions, sorry!\n");
    return;
}


int main(void) {
    setvbuf(stdout, 0, 2, 0);

    char option[MSG_LEN];
    printf("Welcome to the Massive Incomprehensible Corporation Helping Irritating Gordon Appleby Naysayers ordering system!\n");
    int prompt_again = 1;
    while(prompt_again) {
        int order_num = 0;
        for(int i = 0; i < NUM_OPTIONS; i++) {
            printf("%d. %s\n", i+1, order_arr[i]);
        }
        do {
            printf("Please enter the number for your choice: ");
            if(fgets(option, sizeof option, stdin) == NULL) {
                printf("fgets error\n");
                exit(-1);
            }
            sscanf(option, "%d", &order_num);
        } while(1 > order_num || NUM_OPTIONS < order_num);
        if(order_num == 4) {
            // Usually the secret information system, disabled until this round of audits blows over...
            printf("Sorry, temporarily out of stock!\n");
            // print_spy_instructions();
        } else if(order_num < NUM_OPTIONS) {
            // Fake options
            process_order(order_num);
        } else {
            // Exit
            prompt_again = 0;
        }
    }
    printf("Thanks for stopping by!\n");
}
