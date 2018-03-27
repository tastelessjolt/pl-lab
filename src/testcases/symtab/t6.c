void fun (int *a) {
    int *p;

    *p = 425;

    fun (p);
    *p = *p + 454; 
}   