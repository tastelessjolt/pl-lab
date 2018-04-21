int f(int a) {
	int *b;
	return *b;
}

void main() {
	int *b;
	*b = f(3) + *b;
}
