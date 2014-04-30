#include<stdio.h>
#include<stdlib.h>
#include<math.h>

float degree2radians(float degree){
    return (degree * M_PI)/180.0;
}

float distance(float lat1, float lon1, float lat2, float lon2){
    float R = 6373.0;
    lat1 = degree2radians(lat1);
    lon1 = degree2radians(lon1);
    lat2 = degree2radians(lat2);
    lon2 = degree2radians(lon2);
    
    float dlon = lon2 - lon1;
    float dlat = lat2 - lat1;
    float a = pow( pow((sin(dlat/2)),2) + cos(lat1) * cos(lat2) * (sin(dlon/2)), 2);
    float c = 2*atan2(sqrt(a), sqrt(1-a));
    float result = R*c; //*0.621371;
    return result;    
}


int main(int argc, char *argv[]){
    printf("%f degree = %f radian\n", 90.0, degree2radians(90.0));
    printf("Distance = %f miles\n", distance(0.0, 0.0, 0.0, 1.0));
    return 0;
}
