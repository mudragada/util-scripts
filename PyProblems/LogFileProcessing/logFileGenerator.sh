#!/bin/bash

touch server.log
echo -n -e '[01/Aug/1995:00:54:59 -0400] "GET /images/opf-logo.gif HTTP/1.0" 200 32511\n[01/Aug/1995:00:55:04 -0400] "GET /images/ksclogosmall.gif HTTP/1.0" 200 3635\n[01/Aug/1995:00:55:06 -0400] "GET /images/ksclogosmall.gif HTTP/1.0" 403 298\n[01/Aug/1995:00:55:09 -0400] "GET /images/ksclogosmall.gif HTTP/1.0" 200 3635\n[01/Aug/1995:00:55:18 -0400] "GET /images/opf-logo.gif HTTP/1.0" 200 32511\n[01/Aug/1995:00:56:52 -0400] "GET /images/ksclogosmall.gif HTTP/1.0" 200 3635\n' >> server.log

touch input.log
echo -n -e '2015-10-02 17:16:15.572813+00:00 heroku router - - at=info method=GET path="/" host=testapp.herokuapp.com request_id=5a32a15f-fb80-4559-b52a-d3551408c088 fwd="11.22.33.44" dyno=web.1 connect=1ms service=5440ms status=200 bytes=8823 High Response Time\n2015-10-02 17:16:24.270610+00:00 heroku router - - at=info method=GET path="/main.js" host=testapp.herokuapp.com request_id=2743a6f1-778f-4452-9fd7-c2a4c2473258 fwd="11.22.33.44" dyno=web.1 connect=1ms service=15ms status=304 bytes=236\n2015-10-02 17:16:15.842297+00:00 heroku router - - at=info method=GET path="/styles.css" host=testapp.herokuapp.com request_id=85c5c3ed-c893-4e50-a99d-8e01bac0c52b fwd="12.34.56.78" dyno=web.1 connect=0ms service=17ms status=200 bytes=2993\n2015-10-02 17:16:24.271826+00:00 heroku router - - at=info method=GET path="/styles.css" host=testapp.herokuapp.com request_id=a409275e-3e27-4e14-b6fd-59edac5a7792 fwd="11.22.33.44" dyno=web.1 connect=0ms service=9ms status=304 bytes=235\n2015-10-02 17:16:16.486789+00:00 heroku router - - at=info method=GET path="/icons/android-touch-icon.png" host=testapp.herokuapp.com request_id=1c16c27b-751e-483e-a0e5-014e47c7fb0f fwd="12.34.56.78" dyno=web.1 connect=0ms service=29ms status=404 bytes=239\2015-10-02 17:16:24.047899+00:00 heroku router - - at=info method=GET path="/" host=testapp.herokuapp.com request_id=c72f2ff7-c7c8-43ac-9d79-5ab7c9aeaae6 fwd="12.34.56.78" dyno=web.1 connect=0ms service=12ms status=304 bytes=236\n2015-10-02 17:17:17.035437+00:00 heroku router - - at=error code=H13 desc="Connection closed without response" method=POST path="/api/1.0/player/weekly" host=testapp.herokuapp.com request_id=56ff999f-2e56-4bf7-8716-fb6765adc86e fwd="52.6.158.18" dyno=web.1 connect=1ms service=1325ms status=503 bytes=0 Critical' >> input.log