We have an Apache-style access log at /app/access.log and I need a compact summary of it for a traffic review.

Write your summary to /app/report.json. It should be a single JSON object with exactly three keys:

- "total_requests" (integer) - how many requests the log contains
- "unique_ips" (integer) - how many distinct client IP addresses appear in it
- "top_path" (string) - the request path that was requested most often

On the log format: every non-blank line is one request (a line containing only whitespace is ignored), the client IP is the first whitespace-separated field on that line, and the request path is the second token inside the quoted request section - so a line whose quoted section reads "GET /example.html HTTP/1.1" has the path /example.html.

Consider the job done when all of the following hold:

1. /app/report.json exists and parses as a single JSON object.
2. That object has exactly the keys "total_requests", "unique_ips" and "top_path" - no extras and none missing.
3. "total_requests" is an integer equal to the number of non-blank lines in /app/access.log.
4. "unique_ips" is an integer equal to the number of distinct client IP addresses in /app/access.log.
5. "top_path" is a string equal to the request path that appears most often in /app/access.log. Exactly one path is the most frequent, so there is no tie to resolve.
