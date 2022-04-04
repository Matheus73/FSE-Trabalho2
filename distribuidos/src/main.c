#include "dht22.h"
#include "json_config.h"

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <wiringPi.h>
#include <sys/types.h>          /* See NOTES */
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <signal.h>

void quit(){
    exit(0);
}
int socketid;

static const int bcm_2_wPi[] = {30, 31, 8, 9, 7, 21, 22, 11, 10, 13, 12, 14, 26, 23, 15, 16, 27, 0, 1, 24, 28, 29, 3, 4, 5, 6, 25, 2};

void * sentToCentral();
void * receiveFromCentral();

int main(int argc, char **argv){
    wiringPiSetup();

    //receiving json file from command line to setup devices
    Json_Config config;

    if (argc >= 2){
        config = json_config_parse(argv[1]);
    }
    else{
        printf("Erro, o arquivo de inicializacao precisa ser passado como parametro");
        return -1;
    }

    //creating the socket connection
    struct sockaddr_in client;

    socketid = socket(AF_INET, SOCK_STREAM, 0);

    if (socketid == -1) {
        printf("Could not create a socket!\n");
        exit(1);
    }

    client.sin_family = AF_INET;
    client.sin_addr.s_addr = inet_addr(config.ip);
    client.sin_port = htons(config.port);

    while(connect(socketid, (struct sockaddr*) &client, sizeof(client)) < 0){
        printf("Error while conecting to server, trying again\n");
        sleep(1);
    }

    char message[64] = "name=";
    strcat(message,config.name);

    int size = strlen(message);

    if (send(socketid, message, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }
    sleep(1);

    printf("CRIANDO THREADS\n");
    pthread_t sendTempUmi, receiveInputs;

    printf("CRIANDO THREAD TERREO!\n");
    pthread_create(&sendTempUmi, NULL, sentToCentral, NULL);
    pthread_create(&receiveInputs, NULL, receiveFromCentral, NULL);

    pthread_join(sendTempUmi, NULL);
    pthread_join(receiveInputs, NULL);

    return 0;
}

void * receiveFromCentral() {
    while(1){
        char msg[1024];
        if(recv(socketid,msg,1024,0)){
            int code;
            int gpio_value;
            printf("%s\n", msg);
            pinMode(10,OUTPUT);
            int len = strlen(msg);
            for(int i=0;i<len;i++){
                if(msg[i] == '='){
                    msg[i+2] = '\0';

                    code = atoi(&msg[i+1]);

                    msg[i] = '\0';
                    gpio_value = atoi(msg);

                    int pin_number = bcm_2_wPi[gpio_value];

                    if(code == 1){
                        printf("Ligou\n");
                        digitalWrite(pin_number,HIGH);
                    }
                    else if(code == 0){
                        printf("desLigou\n");
                        digitalWrite(pin_number,LOW);
                    }
                    break;
                }

            }
        }
        sleep(1);
    }
}

void * sentToCentral() {
    printf("iniciou\n");
    while(1){
        umiTemp data = read_dht_data(29);
        printf("coletou\n");

        char cod[64]  = "temp=";

        char* tmp = malloc(sizeof(char)*1024);

        gcvt(data.temperature, 6, tmp);
        strcat(cod,tmp);
        strcat(cod,";umid=");
        gcvt(data.humidity, 6, tmp);
        strcat(cod,tmp);

        int size = strlen(cod);

        printf("%s\n", cod);

        if (send(socketid, cod, size, 0) != size) {
            printf("Error: Send failed\n");
            exit(1);
        }

        sleep(1);
    }
}
