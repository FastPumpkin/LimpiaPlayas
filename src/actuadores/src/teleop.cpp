#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Int32.h>
#include "actuadores/HBridgeDriver.h"

sensor_msgs::Joy XboxControler;
std_msgs::Float32 rt;
std_msgs::Float32 lt;
std_msgs::Float32 stick;

actuadores::HBridgeDriver motor;


void callback(const sensor_msgs::Joy& joy){
    XboxControler = joy;
   
    stick.data = XboxControler.axes[0];
    rt.data =  XboxControler.axes[5];
    rt.data = -rt.data * 127 +127;
    lt.data = XboxControler.axes[2];
    lt.data = -lt.data*127+127;
    if(stick.data > -0.2 & stick.data < 0.2){
        if(rt.data>0){
        motor.motor_2 = rt.data;
        motor.pwm_2 = rt.data;
        motor.motor_1 = 0;
        motor.pwm_1 = 0;

        }
        else{
        motor.motor_2 = 0;
        motor.pwm_2 = 0;
        motor.motor_1 = lt.data;
        motor.pwm_1 = lt.data;

        }
    }
    else{
        if(stick.data > 0.2){
            if(rt.data > 0){
                motor.motor_2 = 0;
                motor.pwm_2 = rt.data;
                motor.motor_1 = rt.data;
                motor.pwm_1 = 0;
            }
            else{
                motor.motor_1 = 0;
                motor.pwm_1 = lt.data;
                motor.motor_2 = lt.data;
                motor.pwm_2 = 0;

            }

        }
        else{
            if(rt.data > 0){
                motor.motor_2 = rt.data;
                motor.pwm_2 = 0;
                motor.motor_1 = 0;
                motor.pwm_1 = rt.data;

            }
            else{
                motor.motor_1 = lt.data;
                motor.pwm_1 = 0;
                motor.motor_2 = 0;
                motor.pwm_2 = lt.data;

            }
        }
    }
 

}

int main(int argc, char **argv){
    ros::init(argc, argv, "jostick");
    ros::NodeHandle n;
    ros::Publisher pub = n.advertise<actuadores::HBridgeDriver>("motor_driver",1000);
    ros::Subscriber sub = n.subscribe("joy", 100, callback);
    ros::Rate loop_rate(10);
    while(ros::ok()){
        
        pub.publish(motor);

        ros::spinOnce();
        loop_rate.sleep();

    }
    return 0; 
}