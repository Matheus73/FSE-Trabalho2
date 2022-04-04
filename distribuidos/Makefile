MAINFILE := main
BINFILE := app
INCFOLDER := inc
SRCFOLDER := src
OBJFOLDER := obj

CC := gcc
LF := -lwiringPi -pthread
CFLAGS := -Wextra -Wall -pedantic
SRCFILES := $(wildcard $(SRCFOLDER)/*.c)

all: clean $(SRCFILES:$(SRCFOLDER)/%.c=$(OBJFOLDER)/%.o)
	$(CC) $(CFLAGS) obj/*.o -o $(BINFILE) $(LF)

obj/%.o: src/%.c
	$(CC) $(CFLAGS) -c $< -o $@ -I./inc $(LF)

terreo: $(BINFILE)
	./$(BINFILE) configuracao_andar_terreo.json

1andar: $(BINFILE)
	./$(BINFILE) configuracao_andar_1.json

.PHONY: clean
clean:
	rm -rf obj/*
	rm -rf $(BINFILE)
