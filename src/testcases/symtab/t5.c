// empty returns
// but not recommended
int fun (int a) {
    int *p;
    p = &a;
    if (*p > 0) {
        return;
    }
    // do something else
}

void main () {
    int a, b;
    int *p;
    p = &a;
    *p = -1;

    *p = fun (*p); // the programmer doesn't what is returned
}