int multiple_logical_ops() {
    int *a, *b;
    if (*a == *b) {
        *a = 2;
    }
    else if (*a < *b) {
        *a = 2;
    }
    else if (*a > *b) {
        *a = 2;
    }
    else if (*a != *b) {
        *a = 2;
    }
    else if (*a >= *b) {
        *a = 2;
    }
    else if (*a <= *b) {
        *a = 2;
    }



    if ((*a == *b) || (*a == *b)) {
        *a = 2;
    }
    else if ((*a == *b) && (*a == *b)) {
        *a = 2;
    }
    else if (! (*a == *b)) {
        *a = 2;
    }
}