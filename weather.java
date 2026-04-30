import java.io.IOException;

import javax.naming.Context;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Mapper;
import org.apache.hadoop.io.Reducer;
import org.apache.hadoop.io.Job;

public class weather {
    public static class Map extends Mapper<Object, Text, Text, Text> {
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String[] parts = value.toString().split(",");

            if (parts.length == 4){
                String temp = parts[1];
                String dew = parts[2];
                String wind = parts[3];

                context.write(new Text("avg"), new Text(temp + "," + dew + "," + wind));
            }
        }
    }

    public static class Reduce extends Reducer<Text, Text, Text, Text> {
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            int sumTemp = 0, sumDew = 0, sumWind = 0, count = 0;

            for (Text val : values) {
                String[] nums = val.toString().split(",");

                sumTemp += Integer.parseInt(nums[0]);
                sumDew += Integer.parseInt(nums[1]);
                sumWind += Integer.parseInt(nums[2]);
                count++;
            }
        }
    }
}
