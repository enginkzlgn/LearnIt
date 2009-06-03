#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <stdio.h>

#define MAXBUF 1024

/**
 * MY UDP Server 
*/

int main(int argc,char** argv){
	//status for server
	int udpSocket,returnStatus=0,addrlen=0;
	// sockets for client and server
	struct sockaddr_in udpServer,udpClient;
	char buf[MAXBUF];

	udpSocket=socket(AF_INET,SOCK_DGRAM,0); // datagram socket

	if(udpSocket==-1){
		fprintf(stderr,"Udp soket yaratılamadı\n");
		exit(1);
	}else{
		printf("Udp soket yatarıldı\n");
	}
	udpServer.sin_family =AF_INET;
	udpServer.sin_addr.s_addr=htonl(INADDR_ANY);
	udpServer.sin_port=9955; //my udp port

	returnStatus=bind(udpSocket,(struct sockaddr*)&udpServer,sizeof(udpServer));

	if(returnStatus==0){
		fprintf(stderr,"Bind işlemi tamamlandı\n");
	}else{
		fprintf(stderr,"Bind adreslenme tamamlanmadı\n");
		close(udpSocket);
		exit(1);
	}
	while(1){ //endless loop
		addrlen=sizeof(udpClient);
		returnStatus=recvfrom(udpSocket,buf,MAXBUF,0,(struct sockaddr*)&udpClient,&addrlen);
		if(returnStatus==-1){
			fprintf(stderr,"Beklenen mesaj alınmadı\n");
		}else{
			printf("Beklenen mesaj: %s\n",buf);
			strcpy(buf,"_OK_");
			returnStatus=sendto(udpSocket,buf,strlen(buf)+1,0,(struct sockaddr*)&udpClient,sizeof(udpClient));

			if(returnStatus==-1){
				fprintf(stderr,"Beklenen mesaj gönderilmedi\n");
			}else{
				printf("Beklenen mesaj gönderildi\n");
			}
		}
	}
	close(udpSocket);
	return 0;
}




