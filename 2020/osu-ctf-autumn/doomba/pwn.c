#include "cJSON.h"
#include <stdio.h>
#include <stdlib.h>


char apikey[5000];

typedef struct {
    int cmd_type;
    int x, y;
} Command;

int process_commands() {
    Command command_queue[8];
    char jsonData[2048];

    while (1) {
        printf("JSON > ");
        fgets(jsonData, 2048, stdin);
        cJSON *json = cJSON_ParseWithLength(jsonData, 2048);
        if (!json) break;

        cJSON *commands = cJSON_GetObjectItemCaseSensitive(json, "commands");
        if (!commands) break;
        
        int idx = 0;
        cJSON *item;
        while (item = cJSON_GetArrayItem(commands, idx++)) {
            cJSON *cmdIdNode = cJSON_GetObjectItemCaseSensitive(item, "cmdId");
            cJSON *xNode = cJSON_GetObjectItemCaseSensitive(item, "x");
            cJSON *yNode = cJSON_GetObjectItemCaseSensitive(item, "y");
            if (!cJSON_IsNumber(cmdIdNode) || !cJSON_IsNumber(xNode) || !cJSON_IsNumber(yNode)) break;
            Command cmd;
            cmd.cmd_type = cmdIdNode->valueint;
            cmd.x = xNode->valueint;
            cmd.y = yNode->valueint;
            command_queue[idx] = cmd;
        }
        
        for (int x=0; x<idx; x++) {
            if (command_queue[x].cmd_type == 99) {
                system("reboot");
            }
            // Other commands to-be-implemented
        }
        printf("OK\n");
        cJSON_Delete(json);
    }
    return 0;
}


int main(int argc, char* argv[]) {
    // Magic to make output work
    setvbuf(stdout, 0, 2, 0);

    printf("vacuum cleaner v1.0\n");
    printf("Please enter API key (5000 characters, super secure): ");
    fread(apikey, 1, 5000, stdin);

    process_commands();
    printf("\nGoodbye!\n");
}