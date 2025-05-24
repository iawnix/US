# include "stdlib.h"
# include "stdio.h"
# include "string.h"
# include "dirent.h"
# include "ctype.h"
# include "unistd.h"

typedef struct unit1
{
	char x[8];
	char y[8];
}UNIT1;

// x1_2y2_4.dat
void splitdatName(UNIT1* my,char* mystr)
{   
	//printf("%s\n",mystr);
    for(int i = 0 ;mystr[i] != '\0';i++)
	{
		if (mystr[i] == '.')
		{
			mystr[i] = '\0';
		}
        if (isalpha(mystr[i]))
        {
            mystr[i] = ' ';
        }
        if (mystr[i] == '_')
        {
            mystr[i] = '.';
        }
	}
    sscanf(mystr," %s %s",my->x,my->y);
	//printf("Num:x=%s|y=%s\n",my->x,my->y);
}

void func(const char* PATH,char* XF,char*YF)
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
	
		while ((target = readdir(dp))!= NULL)
		{
			if (target-> d_type == 8 && strstr(target->d_name,".dat"))
			{
				UNIT1* myunit = (UNIT1* )malloc(sizeof(UNIT1));
				fprintf(fp,"./%s\t",target->d_name);
				splitdatName(myunit,target->d_name);
				fprintf(fp,"%s\t%s\t%d\t%d\n",myunit->x,myunit->y,atoi(XF)*2,atoi(YF)*2);
				free(myunit);
			}
		}
	}
}


int main(int argc, char* argv[])
{

	char* PATH = NULL;
	char* XF = NULL;
	char* YF = NULL;
	
	PATH = argv[1];
	XF = argv[2];
	YF = argv[3];
	func(PATH,XF,YF);
	return 0;
}
