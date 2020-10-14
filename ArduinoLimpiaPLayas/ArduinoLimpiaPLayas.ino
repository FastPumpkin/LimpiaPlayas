#include <ros.h>
#include <actuadores/HBridgeDriver.h>


int l1_pwm = 45;
int r1_pwm = 44;
int r2_pwm = 2;
int l2_pwm = 3;


ros::NodeHandle nh;


void movimiento(int l1, int r1, int r2, int l2){
  analogWrite(l1_pwm,l1);
  analogWrite(r1_pwm,r1);
  analogWrite(l2_pwm,l2);
  analogWrite(r2_pwm,r2);
  }

void callback(const actuadores::HBridgeDriver& motor){
  movimiento(motor.motor_1,motor.motor_2,motor.pwm_1,motor.pwm_2);
}


ros::Subscriber<actuadores::HBridgeDriver>sub("motor_driver", &callback);


void setup() {
  nh.initNode();
  nh.subscribe(sub);
  
  pinMode(l1_pwm,OUTPUT);
  pinMode(r1_pwm,OUTPUT);
  pinMode(l2_pwm,OUTPUT);
  pinMode(r2_pwm,OUTPUT);

}


void loop() {
  nh.spinOnce();
  delay(100);
  
 

}
