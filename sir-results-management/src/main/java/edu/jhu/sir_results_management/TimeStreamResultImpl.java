package edu.jhu.sir_results_management;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import edu.jhu.Messages.SimResults;
import software.amazon.awssdk.services.timestreamwrite.model.MeasureValueType;
import software.amazon.awssdk.services.timestreamwrite.model.Record;
import software.amazon.awssdk.services.timestreamwrite.model.RejectedRecordsException;
import software.amazon.awssdk.services.timestreamwrite.model.WriteRecordsRequest;

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
    public void storeResults(SimResults results) {

        List<Record> records = new ArrayList<>();
        long time = results.getTime().getSeconds() * 1000 + results.getTime().getNanos() / 1000;

        Record numInfected = Record.builder()
                .dimensions(timestreamConfig.dimensions())
                .measureValueType(MeasureValueType.BIGINT)
                .measureName("num_infected")
                .measureValue(Integer.toString(results.getNumInfected()))
                .time(String.valueOf(time)).build();

        Record numSusceptible = Record.builder()
                .dimensions(timestreamConfig.dimensions())
                .measureValueType(MeasureValueType.BIGINT)
                .measureName("num_susceptible")
                .measureValue(Integer.toString(results.getNumSusceptible()))
                .time(String.valueOf(time)).build();

        Record numRecovered = Record.builder()
                .dimensions(timestreamConfig.dimensions())
                .measureValueType(MeasureValueType.BIGINT)
                .measureName("num_recovered")
                .measureValue(Integer.toString(results.getNumRecovered()))
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
