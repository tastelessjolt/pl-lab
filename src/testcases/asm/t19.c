int gf1;
int *gf2;

int floating_arith()
{
    int *a, *b, *c;
    *a = *b + *c;
    *a = *b - *c;
    *a = *b * *c;
    *a = *b / *c;
    *a = -*b;

    a = &gf1;
    a = gf2;

    *a = 25;
}

int floating_logic()
{
    int *a, *b, *c;
    if (*a == *b)
    {
        *a = 2;
    }
    else if (*a < *b)
    {
        *a = 2;
    }
    else if (*a > *b)
    {
        *a = 2;
    }
    else if (*a != *b)
    {
        *a = 2;
    }
    else if (*a >= *b)
    {
        *a = 2;
    }
    else if (*a <= *b)
    {
        *a = 2;
    }

    if ((*a == *b) || (*a == *b))
    {
        *a = 2;
    }
    else if ((*a == *b) && (*a == *b))
    {
        *a = 2;
    }
    else if (!(*a == *b))
    {
        *a = 2;
    }
}