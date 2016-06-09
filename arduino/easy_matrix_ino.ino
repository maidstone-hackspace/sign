int ROWS = 8;         // number of rows on the matrix
int DISPLAY_COUNT = 2;// how many max chips do we have connected
int MODE = 0;         // 0 = individual, 1=block when implemented
int ANIMDELAY = 100;  // animation delay, deafault value is 100
int INTENSITYMIN = 0; // minimum brightness, valid range [0,15]
int INTENSITYMAX = 8; // maximum brightness, valid range [0,15]

int DIN_PIN = 2;      // data in pin
int CS_PIN = 3;       // load (CS) pin
int CLK_PIN = 4;      // clock pin

// MAX7219 registers
byte MAXREG_DECODEMODE = 0x09;
byte MAXREG_INTENSITY  = 0x0a;
byte MAXREG_SCANLIMIT  = 0x0b;
byte MAXREG_SHUTDOWN   = 0x0c;
byte MAXREG_DISPTEST   = 0x0f;

byte byteRead;
byte byteValue;
byte byteDisp;
char byteReadBuffer[8];
String readString;


void clear(int disp) {
  for (int row=0; row < ROWS; row++) {
    setRegistry(disp, row, B00000000);
  }
}

void clearAll() {
  for (int disp=0; disp < DISPLAY_COUNT; disp++) {
    clear(disp);
  }
}

void setup ()
{
  Serial.begin(115200);
  Serial.println("Startup");

  pinMode(DIN_PIN, OUTPUT);
  pinMode(CLK_PIN, OUTPUT);
  pinMode(CS_PIN, OUTPUT);

  for (int disp=0; disp < DISPLAY_COUNT; disp++) {
     // initialization of the MAX7219
     setRegistry(disp, MAXREG_SCANLIMIT, 0x07);
     setRegistry(disp, MAXREG_DECODEMODE, 0x00);  // using an led matrix (not digits)
     setRegistry(disp, MAXREG_SHUTDOWN, 0x01);    // not in shutdown mode
     setRegistry(disp, MAXREG_DISPTEST, 0x00);    // no display test
     setRegistry(disp, MAXREG_INTENSITY, 0x0f & INTENSITYMIN);
     clear(disp);
   }

}


int count = 0;
void loop ()
{
  // second beat
  //setRegistry(MAXREG_INTENSITY, 0x0f & INTENSITYMAX);
  //delay(ANIMDELAY);
  
  // switch off
  //setRegistry(MAXREG_INTENSITY, 0x0f & INTENSITYMIN);
  //delay(ANIMDELAY);
  
  // second beat
  //setRegistry(MAXREG_INTENSITY, 0x0f & INTENSITYMAX);
  //delay(ANIMDELAY);
  
  // switch off
  //setRegistry(MAXREG_INTENSITY, 0x0f & INTENSITYMIN);
  //delay(ANIMDELAY*6);

    if (count > 64){
      //clear();
    }

   if(Serial.available() > 2) {
      byteDisp = Serial.read();
      byteRead = Serial.read();
      byteValue = Serial.read();
      if(byteRead==0){
        clear(byteDisp);
      }
      
      setRegistry(byteDisp, byteRead, byteValue);
      Serial.println(byteDisp);
      //Serial.println(byteValue);
      Serial.println("ok");
     count += 1;
    }

  delay(5);
}


void setRegistry(byte targetDisplay, byte reg, byte value)
{
  digitalWrite(CS_PIN, LOW);
  
  for(int disp=0;disp < DISPLAY_COUNT;disp++){
    //Serial.println(disp);
    if(disp == targetDisplay){
        putByte(reg);   // specify register
        putByte(value); // send data
        continue;
    }
    
    putByte(0);   // specify register
    putByte(0); // send data
  
  }

  digitalWrite(CS_PIN, LOW);
  digitalWrite(CS_PIN, HIGH);
  //digitalWrite(CS_PIN, HIGH);
}

void putByte(byte data)
{
  byte i = 8;
  byte mask;
  while (i > 0)
  {
    mask = 0x01 << (i - 1);        // get bitmask
    digitalWrite( CLK_PIN, LOW);   // tick
    if (data & mask)               // choose bit
      digitalWrite(DIN_PIN, HIGH); // send 1
    else
      digitalWrite(DIN_PIN, LOW);  // send 0
    digitalWrite(CLK_PIN, HIGH);   // tock
    --i;                           // move to lesser bit
  }
}
