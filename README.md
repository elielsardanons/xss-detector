# xss-detector

```
Usage:
usage: xss-detector.py [-h] [--url URL] [--body BODY] [--method METHOD]
                       [--threads THREADS] [--db DB]

Search for Cross-site scripting

optional arguments:
  -h, --help         show this help message and exit
  --url URL          The url to search for XSS (http://victim.com/path?q=help)
  --body BODY        The application/x-www-form-urlencoded body content to
                     send ('param1=value1&param2=value2')
  --method METHOD    request method 'GET' or 'POST' (defaults to "GET")
  --threads THREADS  Number of threads to use while crawling the site
  --db DB            sqlite3 database name. (defaults to 'xss.db')
```

Example:
```
./xss-detector.py --url "https://xss-game.appspot.com/level1/frame?query=aaaa&pepe=jose"
```

# Create sqlite3 database if you want the results being stored in the db
```
sqlite3 xss.db < xss.db.script 
```

# Build docker image

```
docker build --tag xss-detector:0.1 .
```

# Running xss-detector using docker

```
docker run -it xss-detector:0.1 --url https://www.victim.com
```
