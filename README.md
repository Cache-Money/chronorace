# ChronoRace

ChronoRace is a tool to accurately perform timed race conditions to circumvent application business logic. I've found in my research that well timed race conditions can allow for uncovering all kinds of interesting edge cases. An example use case is seen [here](https://hackerone.com/reports/300305), where I was able to get arbitrary email confirmation by hitting both the confirmation and email change endpoints a couple hundred milliseconds apart.

## Usage
ChronoRace takes in raw requests and repeats them with a specified time delay. Create files with the raw requests you want to run as done in the `http_requests/example/` folder. Then create a configuration which references the requests.

**Sample configuration**
```
{
  "proxy": "http://127.0.0.1:8080",
  "verify_ssl": false,
  "requests": [
    {
      "file": "http_requests/example/get.txt",
      "delay": 0,
      "replacements": []
    },
    {
      "file": "http_requests/example/post.txt",
      "delay": 500,
      "replacements": [
        ["[REPLACE]", "bar"]
      ]
    }
  ]
}
```

| Config Parameter | Type | Description | Required | Default |
| ---------------- | ---- | ----------- | -------- | ------- |
| requests | array | Array of requests to make. | Yes | |
| requests[x].file | string | Path to file containing the raw http request. | Yes | |
| requests[x].delay | integer | Delay in milliseconds since start. | No | `0` |
| requests[x].replacements | array | Replacements to perform in the request. `[["replace1", "with1"], ["replace2", "with2"]]`. | No | `[]` |
| requests[x].secure | boolean | Make request using the `https` protocol. | No | `true` |
| proxy | string | Proxy URL. It's recommended to send through Burp to track the requests. | No | `null` |
| verify_ssl | boolean | Skip certificate validation. | No | `true` |
| threads | integer | Maximum number of simultaneous requests. Less threads than requests will delay them. | No | `100` |
| print_response | boolean | Print the entire response in the console. | No | `false` |




**Running**
```
pip install -r requirements.txt
python chronorace.py race -c config.json
```
