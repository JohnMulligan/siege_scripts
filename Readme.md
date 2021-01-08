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

### All metrics by timestamp

siege_to_plotly_by_metric.py

This is messy. But it rolls up the various log files by timestamp, grouping them within a time window and showing all of the siege outputs graphed against it on the y axis.


Shows you on a (messy) line graph the average metric at each concurrency level.
