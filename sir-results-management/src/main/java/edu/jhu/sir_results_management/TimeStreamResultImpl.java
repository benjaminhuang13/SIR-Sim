package edu.jhu.sir_results_management;

import java.util.ArrayList;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import software.amazon.awssdk.services.timestreamwrite.model.*;
import software.amazon.awssdk.services.timestreamwrite.model.Record;

/**
 * For more information on Timestream SDK: What is Amazon Timestream for
 * LiveAnalytics? (n.d.). Amazon.Com. Retrieved November 2, 2024, from
 * https://docs.aws.amazon.com/timestream/latest/developerguide/what-is-timestream.html
 */
@Component
public class TimeStreamResultImpl implements IResultsStorage {

    @Autowired
    private TimestreamConfiguration timestreamConfig;

    @Override
    public void storeResults(String results) {

        List<Record> records = new ArrayList<>();
        final long time = System.currentTimeMillis(); // TODO - Is this an input

        Record numInfected = Record.builder()
                .dimensions(timestreamConfig.dimensions())
                .measureValueType(MeasureValueType.BIGINT)
                .measureName("num_infected")
                .measureValue("1000") // TODO
                .time(String.valueOf(time)).build();

        Record numSusceptible = Record.builder()
                .dimensions(timestreamConfig.dimensions())
                .measureValueType(MeasureValueType.BIGINT)
                .measureName("num_susceptible")
                .measureValue("1000") // TODO
                .time(String.valueOf(time)).build();

        Record numRecovered = Record.builder()
                .dimensions(timestreamConfig.dimensions())
                .measureValueType(MeasureValueType.BIGINT)
                .measureName("num_recovered")
                .measureValue("1000") // TODO
                .time(String.valueOf(time)).build();

        records.add(numInfected);
        records.add(numSusceptible);
        records.add(numRecovered);

        WriteRecordsRequest writeRequest = WriteRecordsRequest.builder()
                .databaseName(timestreamConfig.getDatabaseName())
                .tableName(timestreamConfig.getTableName())
                .records(records)
                .build();

        try {
            timestreamConfig.writeClient().writeRecords(writeRequest);
        } catch (RejectedRecordsException e) {
            // TODO - Handle failure
        }
    }

}
