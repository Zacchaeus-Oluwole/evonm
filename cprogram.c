#include <wiringPi.h>
#include <stdio.h>

#define BUTTON_PIN 0   // GPIO17
#define LED_PIN 1      // GPIO18

int main(void) {
    if (wiringPiSetup() == -1) {
        printf("wiringPi setup failed\n");
        return 1;
    }

    pinMode(BUTTON_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);

    pullUpDnControl(BUTTON_PIN, PUD_UP);

    printf("Press the button to control the LED\n");

    while (1) {
        
        if (digitalRead(BUTTON_PIN) == LOW) {
            digitalWrite(LED_PIN, HIGH);  // Turn LED on
            printf("LED ON\n");
        } else {
            digitalWrite(LED_PIN, LOW);   // Turn LED off
            printf("LED OFF\n");
        }

        delay(100);
    }

    return 0;
}
