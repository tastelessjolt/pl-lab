int* fun (int *a) {
    int *p;

    *p = 425;

    p = fun (p);
    *p = *p + 454; 
}

void main () {
    int a;
    int *p;
    p = &a;

    p = fun(p);
}