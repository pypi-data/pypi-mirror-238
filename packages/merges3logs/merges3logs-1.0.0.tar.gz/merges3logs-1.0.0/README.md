# merges3logs

Download cloudfront logs from S3 and merge them into a single log file for the day.

## Installation

```bash
pip install merges3logs
```

## Usage

Set up the config file as documented below.

Run:

```bash
merges3logs path/to/config.ini
```

This will pick up the logs from yesterday (UTC).  To run for a different date, run:

```bash
merges3logs path/to/config.ini --date YYYY-MM-DD
```

## When to Run

Some log lines for a given date will show up in the log files dated the following day.
This is because the last bit of one day doesn't get flushed until the following day, and
the file written will have that days date.  These dates are all in UTC.  Depending on
your logging configuration, it could take hours for all the last logs for a day to get
flushed to S3.

So, you probably want to run this program at least a few hours after midnight, UTC.

Any logs you download for the following day are cached and not re-downloaded the next day.

## Configuration

The bulk of the configuration is done via a ".ini"-style configuration file.  Here is
an example:

```ini
[AWS]
AccessKey = XXX
SecretKey = XXX

[S3]
BucketName = mylogsbucket
Prefix = path/to/logfileprefix_log-%%Y-%%m-%%d-
MaxWorkers = 10

[Local]
CacheDir = /path/to/mylogsbucketcache
DestDir = /path/to/merged-logs
DestFilename = webworkers-cloudfront-%%Y-%%m-%%d.gz
RemoveFiles = False
```

Details:

- AWS specifies your access and secret keys.
- S3.BucketName is the name of your bucket.
- S3.Prefix is the "prefix" of your log file names for a certain date.  An S3 prefix
  is everything after the bucket name up to and including the date, with the date
  encoded using "strftime()" format, however the "%"s need to be doubled (because
  INI format otherwise interprets them).
- S3.MaxWorkers is the number of download jobs that will run to get logs.  Depending
  on your logging configuration in Cloudfront and how widely your services are accessed,
  this can be tens or hundreds of thousands of log files a day.  So running downloads
  in parallel can really speed it up.
- Local.CacheDir is the path to a directory to store the downloaded log files.
  This directory will need to have a cleanup job set up to prevent it from growing
  unbounded.  See also "Local.RemoveFiles".
- Local.DestDir is the directory that the merged log files will be written to.
- Local.DestFilename is the name of the file that will be written in the DestDir
  with "strftime()" format to specify the date.
- Local.RemoveFiles, if "True" will delete the days files from the cache directory
  after a successful run.  If "False", they are kept and you will need to set up a
  cron job or similar to delete them.  Probably most useful for testing, so
  repeated downloads are unnecessary.  Default is "True".

## Cleanup

merges3logs will download the log files into a cache directory, and then work from
the files there.  You can use "Local.RemoveFiles" to delete them after the run, or
set up a cron job for example:

```bash
find /path/to/cachedir -type f -mtime +3 -exec rm {} +
```

You will also need to clean up the destination log directory, though it does grow
much more slowly (logs are compressed and only one file per day).  Something like
using logrotate or:

```bash
find /path/to/merged-logs -type f -mtime +60 -exec rm {} +
```

## Author

Written by Sean Reifschneider, Oct 2023.

## License

CC0 1.0 Universal, see LICENSE file for more information.

<!-- vim: ts=4 sw=4 ai et tw=85
-->
