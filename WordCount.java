import java.io.IOException;
import java.util.StringTokenizer;

public class WordCount {
    public static class Map extends Mapper<Object, Text, Text, IntWritable> {
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());

            while (itr.hasMoreTokens()) {
                context.write(new Text(itr.nextToken()), new IntWritable(1));
            }
        }
    }

    public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable> throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable val : values) sum += val.get();
        context.write(key, new IntWritable(sum));
    }

    public static void main(String[] args) throws Exception {
        Configuration
    }
}