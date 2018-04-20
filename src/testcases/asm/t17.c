float gf1;
float* gf2;

int floating_arith() {
    float *a, *b, *c;
    *a = *b + *c;
    *a = *b - *c;
    *a = *b * *c;
    *a = *b / *c;
    *a = -*b;

    a = &gf1;
    a = gf2;

    *a = 2.5;
}

int floating_logic() {
    float *a, *b, *c;
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