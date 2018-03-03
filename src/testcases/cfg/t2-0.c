void main()
{
	 int *f2,*********f8,****s3;
	 int *f1;
	 int i3;
	 int ***i2;
	 int **i1;
	 int *iftmp0;

	 i2 = &i1;
	 *f2 = 4;


	 if(*f1 != 0)
	 {
		*f2 = 4;
		*f2 = 4;
		 if(*f2 != 0){
				*iftmp0 = 1;
				*f2=4;
		 }
		 else {
			*iftmp0 = 0;
			if(*f2 != 1) {
				*iftmp0 = 1;
				*f2=4;
			}
			else {
				*iftmp0 = 1;
				*f2=4;
			}
				*f2 = 4;
		 }
	 }
	else {
		*iftmp0 = 0;
		*f2 = 4;
	}
	 **i1 = *iftmp0;

}
