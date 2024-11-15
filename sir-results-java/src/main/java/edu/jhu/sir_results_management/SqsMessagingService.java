package edu.jhu.sir_results_management;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.google.protobuf.InvalidProtocolBufferException;
import com.google.protobuf.util.JsonFormat;

import edu.jhu.Messages;
import io.awspring.cloud.sqs.annotation.SqsListener;
import software.amazon.awssdk.services.sqs.SqsAsyncClient;

@Service
public class SqsMessagingService implements IEventQueueHandler {

    @Autowired
    SqsConfiguration configuration;

    @Autowired
    IResultsStorage resultsStorage;

    private SqsAsyncClient client;

    @SqsListener(value = "results")
    public void receiveResultFromQueue(String results) {
        handleSimResults(results);
    }

    @Override
    public void handleSimResults(String results) {
        Messages.SimResults.Builder myBuilder = Messages.SimResults.newBuilder();
        try {
            JsonFormat.parser().merge(results, myBuilder);
        } catch (InvalidProtocolBufferException e) {
            // TODO - Handle Error
            e.printStackTrace();
            return;
        }

        resultsStorage.storeResults(myBuilder.build());
    }

    @Override
    public void handleExportResults(String results) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'handleExportResults'");
    }
}
