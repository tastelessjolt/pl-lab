void main()
{
	p = *p;
	*&p = &p;
	&&p = 5;
}