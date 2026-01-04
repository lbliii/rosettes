abstract class Example implements Runnable {
    private final int count;
    protected volatile boolean running;
    
    synchronized void process() throws Exception {
        if (running) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } finally {
                running = false;
            }
        }
    }
}