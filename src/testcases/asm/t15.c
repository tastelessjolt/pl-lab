void fn (int *p, int *q, int *r, int *a, int *b, int *c) {
    int gksd;
    int *gsd;
    *p = *q;
    *r = *a;
    *b = *c;
}

void main () {
    int *p, *q, *r;
    int *a, *b, *c;
    *p = *q;
    *r = *a;
    *b = *c;
}
