#include <stdio.h>
#include "api.h"

int simple(int num)
{
	printf("The input is %d\n", num);
	return num+2;
}

int sum(int a, int b)
{
	return a + b;
}
