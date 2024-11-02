package edu.jhu.sir_results_management;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import io.awspring.cloud.sqs.annotation.SqsListener;
import jakarta.annotation.PostConstruct;
import software.amazon.awssdk.services.sqs.SqsAsyncClient;

@Service
public class SqsMessagingService implements IEventQueueHandler {

    @Autowired
    SqsConfiguration configuration;

    private SqsAsyncClient client;

    @SqsListener(value = "results")
    public void receiveResultFromQueue(String results) {
        handleSimResults(results);
    }

    @Override
    public void handleSimResults(String results) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'handleSimResults'");
    }

    @Override
    public void handleExportResults(String results) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'handleExportResults'");
    }
}
