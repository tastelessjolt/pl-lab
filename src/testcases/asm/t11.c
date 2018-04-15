float gl;
float *pt;

float f (int* a, float b, int* c, int* d, int* e) {
    float *p;
    float q;

    p = &q;
    a = c;

    return *pt;
}

void main () {
    int *ptr;
    pt = &gl;
    *pt = f(ptr, *pt, ptr, ptr, ptr);
}

