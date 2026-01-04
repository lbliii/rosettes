void process(int *ptr, int **pptr, void (*callback)(int)) {
    int arr[10];
    int *p = &arr[0];
    *ptr = **pptr;
    callback(*p);
}