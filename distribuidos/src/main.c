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

typedef struct{
    int porta1;
    int janela1;
    int janela2;
    int presenca;
    int fumaca;
    int entrada;
    int saida;
} Inputs;

Inputs inputs_gpio;

Json_Config config;

static const int bcm_2_wPi[] = {30, 31, 8, 9, 7, 21, 22, 11, 10, 13, 12, 14, 26, 23, 15, 16, 27, 0, 1, 24, 28, 29, 3, 4, 5, 6, 25, 2};

void * sentToCentral();
void * receiveFromCentral();
void startWiringPiThreads();

void presencaHandler(){
    char cod[64] = "pres=";
    if(digitalRead(bcm_2_wPi[inputs_gpio.presenca]) == 1){
        strcat(cod,"1");
    } else {
        strcat(cod,"0");
    }

    int size = strlen(cod);

    printf("%s\n", cod);

    if (send(socketid, cod, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }

}

void fumacaHandler(){
    char cod[64] = "fumaca=";
    if(digitalRead(bcm_2_wPi[inputs_gpio.fumaca]) == 1){
        strcat(cod,"1");
    } else {
        strcat(cod,"0");
    }

    int size = strlen(cod);

    printf("--------------%s\n", cod);

    if (send(socketid, cod, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }
}

void janela1Handler(){
    char cod[64] = "jan1=";
    if(digitalRead(bcm_2_wPi[inputs_gpio.janela1]) == 1){
        strcat(cod,"1");
    } else {
        strcat(cod,"0");
    }

    int size = strlen(cod);

    printf("--------------%s\n", cod);

    if (send(socketid, cod, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }

}
void janela2Handler(){
    char cod[64] = "jan2=";
    if(digitalRead(bcm_2_wPi[inputs_gpio.janela2]) == 1){
        strcat(cod,"1");
    } else {
        strcat(cod,"0");
    }

    int size = strlen(cod);

    printf("--------------%s\n", cod);

    if (send(socketid, cod, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }

}

void portaHandler(){
    char cod[64] = "port=";
    if(digitalRead(bcm_2_wPi[inputs_gpio.porta1]) == 1){
        strcat(cod,"0");
    } else {
        strcat(cod,"1");
    }

    int size = strlen(cod);

    printf("--------------%s\n", cod);

    if (send(socketid, cod, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }

}

void entradaPredioHandler(){
    char cod[64] = "ocup=";
    strcat(cod,"1");

    int size = strlen(cod);

    printf("--------------%s\n", cod);

    if (send(socketid, cod, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }

}

void saidaPredioHandler(){
    char cod[64] = "ocup=";
    strcat(cod,"-1");

    int size = strlen(cod);

    printf("--------------%s\n", cod);

    if (send(socketid, cod, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }

}

void entradaSegundoAndarHandler(){
    char cod[64] = "ocup=";
    strcat(cod,"1");

    int size = strlen(cod);

    printf("--------------%s\n", cod);

    if (send(socketid, cod, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }
}

void saidaSegundoAndarHandler(){
    char cod[64] = "ocup=";
    strcat(cod,"-1");

    int size = strlen(cod);

    printf("--------------%s\n", cod);

    if (send(socketid, cod, size, 0) != size) {
        printf("Error: Send failed\n");
        exit(1);
    }
}

void send_initial_state(){
    fumacaHandler();
    sleep(1);
    janela1Handler();
    sleep(1);
    janela2Handler();
    sleep(1);
    presencaHandler();
    /* portaHandler(); */
}

void startWiringPiThreads(){
    for(int i=0;i<config.inputs_len;i++){
        //--------------------- Geral
        if(strcmp(config.inputs[i].tag,"Sensor de Presença") == 0){
            printf("Snesor de presenca configurado\n");
            inputs_gpio.presenca = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_BOTH, presencaHandler);
            presencaHandler();
            sleep(1);
        }
        else if(strcmp(config.inputs[i].tag,"Sensor de Fumaça") == 0){
            printf("Snesor de fumaca configurado\n");
            inputs_gpio.fumaca = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_BOTH, fumacaHandler);
            fumacaHandler();
            sleep(1);
        }

        // --------------------- Terreo
        else if(strcmp(config.inputs[i].tag,"Sensor de Janela T01") == 0){
            inputs_gpio.janela1 = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_BOTH, janela1Handler);
            janela1Handler();
            sleep(1);
        }
        else if(strcmp(config.inputs[i].tag,"Sensor de Janela T02") == 0){
            inputs_gpio.janela2 = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_BOTH, janela2Handler);
            janela2Handler();
            sleep(1);
        }
        else if(strcmp(config.inputs[i].tag,"Sensor de Porta Entrada") == 0){
            inputs_gpio.porta1 = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_BOTH, portaHandler);
            portaHandler();
            sleep(1);
        }
        else if(strcmp(config.inputs[i].tag,"Sensor de Contagem de Pessoas Entrando no Prédio") == 0){
            inputs_gpio.entrada = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_RISING, entradaPredioHandler);
        }
        else if(strcmp(config.inputs[i].tag,"Sensor de Contagem de Pessoas Saindo do Prédio") == 0){
            inputs_gpio.saida = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_RISING, saidaPredioHandler);
        }

        // ---------------- Segundo andar

        else if(strcmp(config.inputs[i].tag,"Sensor de Janela 101") == 0){
            inputs_gpio.janela1 = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_BOTH, janela1Handler);
            janela1Handler();
            sleep(1);
        }
        else if(strcmp(config.inputs[i].tag,"Sensor de Janela 102") == 0){
            inputs_gpio.janela2 = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_BOTH, janela1Handler);
            janela2Handler();
            sleep(1);
        }
        else if(strcmp(config.inputs[i].tag,"Sensor de Contagem de Pessoas Entrando no 2º Andar") == 0){
            inputs_gpio.entrada = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_RISING, entradaSegundoAndarHandler);
        }
        else if(strcmp(config.inputs[i].tag,"Sensor de Contagem de Pessoas Saindo do 2º Andar") == 0){
            inputs_gpio.saida = config.inputs[i].gpio;
            wiringPiISR(bcm_2_wPi[config.inputs[i].gpio], INT_EDGE_RISING, saidaSegundoAndarHandler);
        }
    }

}

int main(int argc, char **argv){
    wiringPiSetup();

    //receiving json file from command line to setup devices

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

    startWiringPiThreads();
    /* send_initial_state(); */

    pthread_t sendTempUmi, receiveInputs;

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
    while(1){
        int pin_number = bcm_2_wPi[ config.dht22[0].gpio ];
        umiTemp data = read_dht_data(pin_number);

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
