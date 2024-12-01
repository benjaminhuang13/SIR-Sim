package edu.jhu.sir_results_management;

import java.util.ArrayList;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.timestreamwrite.TimestreamWriteClient;
import software.amazon.awssdk.services.timestreamwrite.model.Dimension;

@Configuration
public class TimestreamConfiguration {

    @Value("${cloud.aws.region.static}")
    private String region;

    //@Value("${cloud.aws.az}")
    //private String az;
    //@Value("${cloud.aws.timestream.host}")
    //private String host;
    @Value("${cloud.aws.timestream.database}")
    private String database;

    @Value("${cloud.aws.timestream.table}")
    private String table;

    @Bean
    public TimestreamWriteClient writeClient() {
        return TimestreamWriteClient.builder()
                .region(Region.US_EAST_1)
                .build();
    }

    @Bean
    public List<Dimension> dimensions() {
        List<Dimension> dimensions = new ArrayList<>();

        dimensions.add(Dimension.builder().name("region").value(region).build());
        //dimensions.add(Dimension.builder().name("az").value(az).build());
        //dimensions.add(Dimension.builder().name("hostname").value(host).build());

        return dimensions;
    }

    public String getDatabaseName() {
        return database;
    }

    public String getTableName() {
        return table;
    }

}
