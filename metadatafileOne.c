# include "stdlib.h"
# include "stdio.h"
# include "string.h"
# include "dirent.h"



typedef struct unit1
{
	char coor1[4];
	char coor2[4];
	char F[9];
}UNIT1;



void func(const char* PATH)
{
	DIR* dp = NULL;
	FILE*fp;
	fp = fopen("metadatafile","w");
	fputs("# \n \n",fp);
	if ((dp = opendir(PATH)) == NULL)
	{
		printf("ERROR: Open %s \n",PATH);
	}
	else
	{
		struct dirent* target = NULL;
			
		char delim[] = "-_.";
		while ((target = readdir(dp))!= NULL)
		{
			if (target-> d_type == 8 && strstr(target->d_name,".dat"))
			{
				
				UNIT1* myunit = (UNIT1* )malloc(sizeof(UNIT1));
				fprintf(fp,"./%s\t",target->d_name);
				strcpy(myunit->coor1,strtok(target->d_name,delim));
				strcpy(myunit->coor2,strtok(NULL,delim));
				strcpy(myunit->F,strtok(NULL,delim));
				fprintf(fp,"%s.%s\t%d\n",myunit->coor1,myunit->coor2,atoi(myunit->F)*2);
				free(myunit);
			}
		}
	}
}


int main(int argc, char* argv[])
{

	char* PATH = NULL;
	
	PATH = argv[1];
	

	func(PATH);
	return 0;
}
