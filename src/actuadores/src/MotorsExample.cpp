#include "ros/ros.h"
#include "std_msgs/UInt8MultiArray.h"
#include "actuadores/HBridgeDriver.h"



int main(int argc, char **argv){
    ros::init(argc,argv,"puente_driver");
    ros::NodeHandle n;
    ros::Publisher pub = n.advertise<actuadores::HBridgeDriver>("motor_driver",1000);
    
    
    ros::Rate loop_rate(10);
    
    while(ros::ok()){
        actuadores::HBridgeDriver m;
        m.motor_1 = 100;
        m.motor_2 = 0;
        m.pwm_1 = 0;
        m.pwm_2 = 100;
        
        pub.publish(m);
        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}