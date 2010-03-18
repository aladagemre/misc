public class Reverse {
    
    public static void main(String[] args){
	int[] array = {1,2,3,4,5};
	Reverse r = new Reverse();
	r.reverse(array, 0, 4);
	
	for (int i=0; i<5; i++){
	    System.out.print(array[i] + " ");
	}
    }
    
    
    public void reverse(int[] a, int left, int right){
	int temp;
	
	while(left<right){
	    temp = a[right];
	    a[right] = a[left];
	    a[left] = temp;
	
	    left++;
	    right--;
	}	
    }
    
}