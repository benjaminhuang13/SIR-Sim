package edu.jhu.sir_results_management;

public interface IEventQueueHandler {
   void handleSimResults(String results);
   void handleExportResults(String results);
}
