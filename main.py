import os, sys, requests, json
from twarc import Twarc
from datetime import datetime as dt
from operator import itemgetter


VERBOSE = True

if not os.path.exists("output"):
    os.mkdir("output")

# Check environmental setup
consumer_key = os.getenv("RR_CONSUMER_KEY")
consumer_secret = os.getenv("RR_CONSUMER_SECRET")
access_token = os.getenv("RR_ACCESS_TOKEN")
access_token_secret = os.getenv("RR_ACCESS_SECRET")

errs = []
if consumer_key is None:
    errs.append("RR_CONSUMER_KEY")
if consumer_secret is None:
    errs.append("RR_CONSUMER_SECRET")
if access_token is None:
    errs.append("RR_ACCESS_TOKEN")
if access_token_secret is None:
    errs.append("RR_ACCESS_SECRET")

if errs:
    raise RuntimeError(
        f"Required environment variables are undefined: {errs}. See README for details."
    )

# Check that tweet_id was provided
if len(sys.argv) != 2:
    raise RuntimeError("Program should be called like: `python main.py <tweet_id>`")

tweet_id = sys.argv[1]

# Main
t = Twarc(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)

tweet = t.tweet(tweet_id)
if not tweet:
    raise RuntimeError(f"tweet with id {tweet_id} does not exist" % query)
# replies is a generator object
replies = t.replies(tweet, True)

# List to hold dict of relevant photo data from each of the replies
photo_data = []
for reply in replies:
    # Photos will be in a list stored at reply['extended_entities']['media']
    print("Processing next reply")

    ee = reply.get("extended_entities")
    if ee is None:
        continue

    m = ee.get("media")
    if m is None:
        continue

    for media in m:
        if media.get("type") == "photo":
            pd = {}
            pd["url"] = media["media_url_https"]

            pd["id_str"] = media["id_str"]  # unique ID per photo
            pd["YYYYMMDD"] = dt.strftime(
                dt.strptime(
                    " ".join(itemgetter(1, 2, 5)(reply["created_at"].split(" "))),
                    "%b %d %Y",
                ),
                "%Y%m%d",
            )
            pd["screen_name"] = reply["user"]["screen_name"]
            # Build a name for the photo from it's metadata
            # Format is YYYYMMDD_<screen_name>_<id_str>.<ext>
            # YYYYMMDD is the day the reply was sent
            # <screen_name> is the user's Twitter username i.e. "@jack" becomes "jack"
            # <id_str> is a unique ID assigned by Twitter to each photo. We leverage it's uniqueness
            # to prevent filename overlap
            # <ext> is just the extension of the photo i.e. jpg/png/etc
            pd[
                "saved_photo_name"
            ] = f"{pd['YYYYMMDD']}_{pd['screen_name']}_{pd['id_str']}.{pd['url'].split('.')[-1]}"
            if VERBOSE:
                print(f"Found a photo posted by: {pd['screen_name']}")
            photo_data.append(pd)

# Save photo data as json, useful in case photos need to be re-downloaded
with open("output/meta.json", "w") as meta:
    json.dump(photo_data, meta)


for pd in photo_data:
    if VERBOSE:
        print(f"Downloading photo posted by {pd['screen_name']} from {pd['url']}")
    filename = os.path.join("output", pd["saved_photo_name"])
    img = requests.get(pd["url"]).content
    with open(filename, "wb") as f:
        f.write(img)