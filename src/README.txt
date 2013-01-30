Gnip-Python-PowerTrack-Rules
============================

Gnip PowerTrack rules management library and utilities.

Install with:
    pip install gnip-powertrack-rules

Edit the sample_config.cfg file with your credentials and your favorite stream rule management
url. Copy or move to .gnip.

Utilities will check the local directory for .gnip. If you want to use a different location
try:

    export GNIP_CONFIG_FILE=... in your environment.


EXAMPLES:
=========

$ ./list_rules.py -h
Usage: list_rules.py [options]

Options:
  -h, --help            show this help message and exit
  -u URL, --url=URL     Input url
  -p, --pretty-print    Prettier printing of output.
  -m PATTERN, --match-pattern=PATTERN
                        List only rules matching pattern (Python REs)
  -t MATCHTAG, --match-tag=MATCHTAG
                        List only rules with tags matching pattern (Python
                        REs)
  -c, --csv             Csv printing of output (with tab delimiter)


> ./list_rules.py 
{"rules": [{"tag": "musician", "value": "bieber"}, {"tag": "musician", "value": "gaga "}, {"tag": "candidate", "value": "obama"}, {"tag": "candidate", "value": "romney "}, {"tag": null, "value": "dog"}, {"tag": null, "value": "cat -mouse -mice -rat"}]}


$ ./list_rules.py -p
{
   "rules": [
      {
         "tag": null, 
         "value": "obama"
      }, 
      {
         "tag": null, 
         "value": "romney"
      }, 
      {
         "tag": "musician", 
         "value": "bieber"
      }, 
      {
         "tag": "musician", 
         "value": "gaga "
      }, 
      {
         "tag": null, 
         "value": "dog"
      }, 
      {
         "tag": null, 
         "value": "cat -mouse -mice -rat"
      }
   ]
}

$ ./delete_rules.py -h
Usage: delete_rules.py [options]

Options:
  -h, --help            show this help message and exit
  -u URL, --url=URL     Input url
  -m PATTERN, --match-rule=PATTERN
                        List only rules matching pattern (Python REs)
  -t MATCHTAG, --match-tag=MATCHTAG
                        List only rules with tags matching pattern (Python
                        REs)
  -d, --delete          Set this flag to delete, without -d, prospective
                        changes are shown but not executed.

Warning! this deletes rules from you stream.

$ ./delete_rules.py 
=== Proposed rule deletions shown but not executed ===
{"rules": [{"tag": null, "value": "obama"}, {"tag": null, "value": "romney"}, {"tag": "musician", "value": "bieber"}, {"tag": "musician", "value": "gaga "}, {"tag": null, "value": "dog"}, {"tag": null, "value": "cat -mouse -mice -rat"}]}

> ./create_rules.py -h
Usage: create_rules.py [options]

Options:
  -h, --help          show this help message and exit
  -u URL, --url=URL   Input url
  -j, --json          Interpret input stream as JSON rules
  -d, --delete-rules  Delete existing rules before creating new.


> cat powertrack.rules | ./create_rules.py 
OK - 6 rules created

> cat powertrack.json | ./create_rules.py -dj
OK - 6 rules created


Usage: update_rules.py [options]

Options:
  -h, --help            show this help message and exit
  -u URL, --url=URL     Input url
  -r R1, --current-rule=R1
                        Rule to be replaced.
  -s R2, --update-rule=R2
                        Replacement rule.
  -t T2, --update-tag=T2
                        Replacement rule tag.
  -f, --tab-file        Stdin containing list of updates
                        'rule1<tab>rule2<tab>tab2'

To illustrate the update functionality, use the following sequence. 
Warning! this deletes rules from you stream.

> ./delete_rules.py -d
=== Deleteing rules ===
OK - 5 rules deleted,
> cat powertrack.json | ./create_rules.py -j
OK - 6 rules created,
> ./list_rules.py -c
bieber	None
gaga	None
obama	None
romney	None
dog	None
cat -mouse -mice -rat	None
> cat powertrack.updates | ./update_rules.py -f
OK - Successfully updated bieber to biebers.
OK - Successfully updated gaga to gagas.
OK - Successfully updated obama to obamas.
OK - Successfully updated romney to romnies.
OK - Successfully updated dog to dog.
> ./list_rules.py -c
cat -mouse -mice -rat	None
biebers	musician
gagas	musician
obamas	candidate
romnies	candidate

==
Gnip-Python-PowerTrack-Rule by Scott Hendrickson see LICENSE.txt for details.
