#pragma once

typedef struct umiTemp{
    float temperature;
    float humidity;
}umiTemp;

umiTemp read_dht_data(int dht_pin);

