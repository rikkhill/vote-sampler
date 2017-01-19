# vote-sampler

Proof-of-concept for estimating the outcome of an election with known results
under different boundaries.

### How it works
We can define a new constituency as a set of postcodes. By randomly resampling from the actual election results in the original constituencies covering those postcodes, and weighted by the original constituencies’ valid voter turnout, we can produce an estimate for the outcome of the new constituency.


### Usage
I'll tell you once I've written it

### Data
This PoC uses the 2015 General Election results from the [Electoral Commission](http://www.electoralcommission.org.uk/find-information-by-subject/elections-and-referendums/), and a 2015 postcode-constituency lookup stolen from
 [here](https://github.com/flashton2003/postcode_to_constituency). The relevant XLSX and TSV files must be present in the `data` directory in order for the ETL process to work.