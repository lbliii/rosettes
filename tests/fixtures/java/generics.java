public class Box<T extends Comparable<T>> {
    private T value;
    
    public <U> void process(List<? super U> items) {
        // Generic method
    }
}