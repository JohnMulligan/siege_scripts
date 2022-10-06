This should be revised to capture the verbose (or semi-verbose) logging.

siege.sh currently outputs timestamp, number of workers, and a json dictionary.

	1665023195
	110
	enslaved_links

	{	"transactions":			        7513,
		"availability":			      100.00,
		"elapsed_time":			      299.88,
		"data_transferred":		       63.53,
		"response_time":		        4.29,
		"transaction_rate":		       25.05,
		"throughput":			        0.21,
		"concurrency":			      107.48,
		"successful_transactions":	        7513,
		"failed_transactions":		           0,
		"longest_transaction":		       18.38,
		"shortest_transaction":		        0.25
	}

The dictionary does not appear in the log files, and the high and low ends are actually quite interesting against the average. You could use this to draw a crude violin graph or banded line chart. If you were really into CI stuff you could capture the truly verbose outputs. But for a normal person, the well-formatted json dump here is great, and nohup.out should replace the logs in the workflow.


In order to reliably scale up its number of processes, siege needs

* a "modern" os and a few cpu's
* a medium-length run (5 mins seems to work)

Consider folding the new siege.sh parameters in with the existing dockerstats scripts.




# Siege scripter and results grapher

This collection scripts a stress-testing of endpoints

Requires plotly module and Python 3

## Scripted siege run

* install siege on the machine that will be hitting the target server
   * [git repo](https://github.com/JoeDog/siege)
   * [website](https://www.joedog.org/siege-home/)
   * or just `sudo apt-get install -y siege` on ubuntu
* put targeted endpoints in 'links' subdirectory
   * in named .txt file(s)
   * full url's separated by line breaks
   * and siege does POST (again: https://www.joedog.org/siege-manual/)
* run shell script
   * set parameters in siege.sh script file
   * I advise running this in background on a vm as it can take a while
   * the script will iterate
      * over the range of parameters defined at the head of siege.sh (stepping up concurrency)
      * over the endpiont url .txt files in the 'links' subdirectory (for each concurrency level)
* siege will stack up the results in .log files by endpoint in the 'logs' subdirectory

## Output processing

* run siege_to_plotly scripts and point it at the output directory where your logfile(s) live
* e.g., `python3 siege_to_plotly_by_endpoint_class.py logs`
* it will create standalone html plotly line graphs of the various endpoints' performance
* I broke out siegelogparser.py as its own module to facilitate people making their own graphs

## Current outputs

### Response time versus transaction rate

siege_to_plotly_by_endpoint_class.py

Shows you where the different endpoints peak out performance-wise. You'll typically see the transaction rate max out and then response times begin to climb quickly as queues form up.

---------
## Below is deprecated for the time being
### All metrics by timestamp

siege_to_plotly_by_metric.py

This is messy. But it rolls up the various log files by timestamp, grouping them within a time window and showing all of the siege outputs graphed against it on the y axis.


Shows you on a (messy) line graph the average metric at each concurrency level.
