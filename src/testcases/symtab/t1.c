int *n, *p;
int *q, *global;

// int ***fun(int *);
// int ***fun(int *);
// int ***fun();
int *fun1(int **b, int *a);
float *fun2(int *);
float *fun3(int***, int* a, int* b);

void main () {
    int *a, **b; 
    *b = a + (-fun1 (b, a));
}

int ***fun(int *a)
{
    int *an, *qas;
    if (*a == 2)
    {
        int *q;
        *q = 3;
    }
    else
    {
        int *p;
    }
}

int *fun1(int **b, int *a)
{
    return a;
}

float *fun3(int ***ad, int *adfs, int *bf)
{
    float *fad, af;
    *fad = 3.4;
    return fad;
}

int errortests(int a) {
    int *p;
    int b;
    // These two don't/shouldn't work
    // p = & &b;
    // p = &*b;
    
    *p = *&b; // this works/should work
}