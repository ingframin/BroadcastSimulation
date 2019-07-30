#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <unistd.h>

int main(int argc, char* argv[]){
    char cwd[PATH_MAX];
     if (getcwd(cwd, sizeof(cwd)) != NULL) {
       printf("Current working dir: %s\n", cwd);
   } else {
       perror("getcwd() error");
       return 1;
   }
    char base[6+PATH_MAX] = "PATH=";
    char* runtime = "\\brdsim\\bin";
    char program[80] = "java -Xmx8G -jar build/jar/BroadcastSimulation.jar ";
    strcat(base,cwd);
    strcat(base,runtime);
    if(argc>1){
        strcat(program,argv[1]);
    }
   
    printf("%s\n",base);
    putenv(base);
    system(program);
    return 0;
}