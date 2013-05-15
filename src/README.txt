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


Command line scripts:

    create_rules.py  delete_rules.py  list_rules.py  update_rules.py

Example files:
    
    example0.rules  example1.rules  example2_updates.rules  example3.json  example4_updates.rules

Scripts have parameter descriptions that can be viewed with the -h flag.  E.g.,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./list_rules.py -h
Usage: list_rules.py [options]

Options:
  -h, --help            show this help message and exit
  -u URL, --url=URL     Rules end point url
  -p, --pretty-print    Prettier printing of output.
  -e PATTERN, --regex-match-rule=PATTERN
                        List only rules matching pattern (Python REs)
  -x TAGPATTERN, --regex-match-tag=TAGPATTERN
                        List only rules with tag matching pattern (Python REs)
  -m RULE, --match-rule=RULE
                        List only rules matching rule (Exact)
  -t TAG, --match-tag=TAG
                        List only rules with tags matching tag (Exact)
  -c, --csv             Csv printing of output (with tab delimiter)

To delete all of your rules:

>>~/Gnip-Python-PowerTrack-Rules/src$ ./delete_rules.py -d
=== Deleting rules ===
OK - 3 rules deleted,

To retrieve rules from the Gnip servers:

>>~/Gnip-Python-PowerTrack-Rules/src$ ./list_rules.py 
{"rules": []}

Let's make some simple rules, first off, with not tags,

>>~/Gnip-Python-PowerTrack-Rules/src$ cat example0.rules 
bieber lang:ja
gaga lang:es
obama

>>~/Gnip-Python-PowerTrack-Rules/src$ ./create_rules.py example0.rules 
OK - 3 rules created,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./list_rules.py -p
{
   "rules": [
      {
         "tag": null, 
         "value": "bieber lang:ja"
      }, 
      {
         "tag": null, 
         "value": "gaga lang:es"
      }, 
      {
         "tag": null, 
         "value": "obama"
      }
   ]
}

Now make some slightly more complicated rules with tags. The rules file uses tabs to
separate rules and tags:

>>~/Gnip-Python-PowerTrack-Rules/src$ ./create_rules.py -d example1.rules 
OK - 8 rules created,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./list_rules.py -p
{
   "rules": [
      {
         "tag": "musician", 
         "value": "bieber"
      }, 
      {
         "tag": "musician", 
         "value": "gaga"
      }, 
      {
         "tag": "POTUS", 
         "value": "obama"
      }, 
      {
         "tag": "POTUS", 
         "value": "taft"
      }, 
      {
         "tag": null, 
         "value": "dog OR doggy OR dogs"
      }, 
      {
         "tag": "pets", 
         "value": "canary OR parrot OR parakeet"
      }, 
      {
         "tag": "pets", 
         "value": "cat OR kitty OR kitten"
      }, 
      {
         "tag": "pets", 
         "value": "ground OR hog -day"
      }
   ]
}


Oops, we don't want ground OR hog--those are pets, we wanted ground (AND) hog.  Also,
we want to tag the dog rule with "pets" as well.  Here is the update file (columns are
existing rule(tab)replacement rule(tab)new tag):

>>~/Gnip-Python-PowerTrack-Rules/src$ cat example2_updates.rules 
dog OR doggy OR dogs    dog OR doggy OR dogs    pets
ground OR hog -day  ground hog -day pets

>>~/Gnip-Python-PowerTrack-Rules/src$ ./update_rules.py example2_updates.rules 
OK - Successfully updated dog OR doggy OR dogs OR GNIPNULLRULE to dog OR doggy OR dogs.
OK - Successfully updated ground OR hog -day to ground hog -day.

>>~/Gnip-Python-PowerTrack-Rules/src$ ./list_rules.py -p
{
   "rules": [
      {
         "tag": "musician", 
         "value": "bieber"
      }, 
      {
         "tag": "musician", 
         "value": "gaga"
      }, 
      {
         "tag": "POTUS", 
         "value": "obama"
      }, 
      {
         "tag": "POTUS", 
         "value": "taft"
      }, 
      {
         "tag": "pets", 
         "value": "canary OR parrot OR parakeet"
      }, 
      {
         "tag": "pets", 
         "value": "cat OR kitty OR kitten"
      }, 
      {
         "tag": "pets", 
         "value": "dog OR doggy OR dogs"
      }, 
      {
         "tag": "pets", 
         "value": "ground hog -day"
      }
   ]
}

Let's use JSON formated rules instead:

>>~/Gnip-Python-PowerTrack-Rules/src$ cat example3.json 
{"rules": [{"tag": "teen idol", "value": "bieber"}, {"tag": "teen idol", "value": "gaga"}, {"tag": "teen idol:POTUS", "value": "obama"}, {"tag": "candidate", "value": "romney"}, {"tag": "pets", "value": "dog"}, {"tag": "pets", "value": "cat -mouse -mice -rat"}]}

Let's make a new set of rules (and use the -d flag to delete all of the old rules):

>>~/Gnip-Python-PowerTrack-Rules/src$ ./create_rules.py -dj example3.json 
OK - 6 rules created,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./list_rules.py -p
{
   "rules": [
      {
         "tag": "teen idol", 
         "value": "bieber"
      }, 
      {
         "tag": "teen idol", 
         "value": "gaga"
      }, 
      {
         "tag": "teen idol:POTUS", 
         "value": "obama"
      }, 
      {
         "tag": "candidate", 
         "value": "romney"
      }, 
      {
         "tag": "pets", 
         "value": "dog"
      }, 
      {
         "tag": "pets", 
         "value": "cat -mouse -mice -rat"
      }
   ]
}

This time, create the same new rule set (deleting the old with -d) and append a
universal negation clause to every rule on creation.  In this case, we want to remove
activities with the term "hate":

>>~/Gnip-Python-PowerTrack-Rules/src$ ./create_rules.py -dj example3.json -a"-hate"
OK - 6 rules created,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./list_rules.py -p
{
   "rules": [
      {
         "tag": "teen idol", 
         "value": "bieber -hate"
      }, 
      {
         "tag": "teen idol", 
         "value": "gaga -hate"
      }, 
      {
         "tag": "teen idol:POTUS", 
         "value": "obama -hate"
      }, 
      {
         "tag": "candidate", 
         "value": "romney -hate"
      }, 
      {
         "tag": "pets", 
         "value": "dog -hate"
      }, 
      {
         "tag": "pets", 
         "value": "cat -mouse -mice -rat -hate"
      }
   ]
}

Now do it with version number "V1" and the creation date appended to the tags:

>>~/Gnip-Python-PowerTrack-Rules/src$ ./create_rules.py -dj example3.json -a"-hate" -b"V1:$(date +%Y-%m-%d)"
OK - 6 rules created,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./list_rules.py -p
{
   "rules": [
      {
         "tag": "teen idol:V1:2013-05-15", 
         "value": "bieber -hate"
      }, 
      {
         "tag": "teen idol:V1:2013-05-15", 
         "value": "gaga -hate"
      }, 
      {
         "tag": "teen idol:POTUS:V1:2013-05-15", 
         "value": "obama -hate"
      }, 
      {
         "tag": "candidate:V1:2013-05-15", 
         "value": "romney -hate"
      }, 
      {
         "tag": "pets:V1:2013-05-15", 
         "value": "dog -hate"
      }, 
      {
         "tag": "pets:V1:2013-05-15", 
         "value": "cat -mouse -mice -rat -hate"
      }
   ]
}

We can also delete rules selected by partial match of the rule or tag:

>>~/Gnip-Python-PowerTrack-Rules/src$ ./delete_rules.py -h
Usage: delete_rules.py [options]

Options:
  -h, --help            show this help message and exit
  -u URL, --url=URL     Input url
  -e PATTERN, --regex-match-rule=PATTERN
                        List only rules matching pattern (Python REs)
  -x TAGPATTERN, --regex-match-tag=TAGPATTERN
                        List only rules with tag matching pattern (Python REs)
  -m RULE, --match-rule=RULE
                        List only rules matching rule (Exact)
  -t TAG, --match-tag=TAG
                        List only rules with tags matching tag (Exact)
  -d, --delete          Set this flag to delete, without -d, prospective
                        changes are shown but not executed.

By rule match is too strict unless we type in the whole rule,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./delete_rules.py -tcandidate
=== Proposed rule deletions shown but not executed, use -d to execute ===

>>>===SHOWING LOCAL RULES -- May NOT RELECT SERVER STATUS===<<<
{"rules": []}

But by regex, we get a match,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./delete_rules.py -xcandidate
=== Proposed rule deletions shown but not executed, use -d to execute ===

>>>===SHOWING LOCAL RULES -- May NOT RELECT SERVER STATUS===<<<
{"rules": [{"tag": "candidate:V1:2013-05-15", "value": "romney -hate"}]}

Add the -d flag to execute the change on the Gnip servers,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./delete_rules.py -dxcandidate
=== Deleting rules ===
OK - 1 rules deleted,

>>~/Gnip-Python-PowerTrack-Rules/src$ ./list_rules.py -p
{
   "rules": [
      {
         "tag": "teen idol:V1:2013-05-15", 
         "value": "bieber -hate"
      }, 
      {
         "tag": "teen idol:V1:2013-05-15", 
         "value": "gaga -hate"
      }, 
      {
         "tag": "teen idol:POTUS:V1:2013-05-15", 
         "value": "obama -hate"
      }, 
      {
         "tag": "pets:V1:2013-05-15", 
         "value": "dog -hate"
      }, 
      {
         "tag": "pets:V1:2013-05-15", 
         "value": "cat -mouse -mice -rat -hate"
      }
   ]
}

==
Gnip-Python-PowerTrack-Rule by Scott Hendrickson see LICENSE.txt for details.
