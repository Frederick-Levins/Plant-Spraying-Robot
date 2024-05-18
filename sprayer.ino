// Frederick Levins and Parker Murphy
// Main arduino code for sprayer functionality. 

#include<Servo.h>



// intial positioning and coordinate variables
Servo x, y;
int width = 640, height = 480;
int xpos = 90, ypos = 55;
int i, j;

void setup() {

  // Open serial at same baud rate as rapsberry pi
  Serial.begin(9600);
  x.attach(9);
  y.attach(10);

  x.write(xpos);
  y.write(ypos);

  pinMode(8, OUTPUT);

  digitalWrite(8, LOW);

}
const int angle = 2;


void loop() {
  // check if pi communicating, grab data coordinates to set direction and position with angle and movement
  if (Serial.available() > 0) {
    int x_mid, y_mid;
    if (Serial.read() == 'X')
    {
      x_mid = Serial.parseInt();
      digitalWrite(8, HIGH);

      i = 1;

      if (Serial.read() == 'Y')
        y_mid = Serial.parseInt();
        j = 1;
    } else {
      digitalWrite(8, LOW);
    } 

    //offset X 
    x.write(180 - x_mid);
    y.write(y_mid);

  // do nothing when Pi not communicating 
  } else {
    digitalWrite(8, LOW);
  }
}