package edu.jhu.sir_results_management;

import java.time.Duration;
import java.time.Instant;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.test.context.SpringBootTest;

import com.google.protobuf.Timestamp;

import edu.jhu.Messages;

@SpringBootTest
@EnableAutoConfiguration(exclude = {DataSourceAutoConfiguration.class})
public class TimeStreamIT {

    @Autowired
    IResultsStorage resultsStorage;

    //@Test
    public void writeResultsTest() {
        Instant now = Instant.now();
        Timestamp time = Timestamp.newBuilder()
                .setSeconds(now.getEpochSecond())
                .setNanos(now.getNano())
                .build();

        Messages.DailyResult result = Messages.DailyResult.newBuilder()
                .setNumInfected(1)
                .setNumRecovered(2)
                .setNumSusceptible(3)
                .setTime(time)
                .build();

        Messages.SimResults results = Messages.SimResults.newBuilder()
                .addResults(result)
                .build();

        resultsStorage.storeResults(results);
    }

    //@Test
    public void oneHourTest() throws InterruptedException {
        Instant startTime = Instant.now();
        boolean isRunning = true;

        while (isRunning) {
            resultsStorage.storeResults(createSimResults());
            Thread.sleep(3600);

            isRunning = Duration.between(startTime, Instant.now()).toHours() == 0;
        }
    }

    private Messages.SimResults createSimResults() {
        Instant now = Instant.now();
        Timestamp time = Timestamp.newBuilder()
                .setSeconds(now.getEpochSecond())
                .setNanos(now.getNano())
                .build();

        Messages.DailyResult result = Messages.DailyResult.newBuilder()
                .setNumInfected(1)
                .setNumRecovered(2)
                .setNumSusceptible(3)
                .setTime(time)
                .build();

        Messages.SimResults results = Messages.SimResults.newBuilder()
                .addResults(result)
                .build();

        return results;
    }

}
