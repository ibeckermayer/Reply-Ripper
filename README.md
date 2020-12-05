# Reply Ripper

Reply Ripper is a script for downloading all photo media posted in a reply to a tweet.

The project forks [twarc](https://github.com/DocNow/twarc) and is released under the MIT license.

## Setup

#### Twitter Developer Setup

In order to run Reply Ripper you must set up a [Twitter Developer](https://developer.twitter.com/) account. Once your account is set up, navigate to the [developer portal](https://developer.twitter.com/en/portal/projects-and-apps) to create a new app and get your API keys.

From "Projects & Apps > Overview", scroll down to "Standalone Apps" and click the "Create App". Name your app (probably some derivative of "Reply Ripper") and then navigate back to "Projects & Apps > Overview".

Find the app you just made under "Standalone Apps" and click it's corresponding key icon which will take you to your app's Keys and Tokens page. You'll need these keys and tokens for the "Environment Setup" step below, so you can either look ahead and set your environment up, or just save them in a text file or document. Under "Consumer Keys > API key & secret", click regenerate and save the string of letters and numbers for both "API key" and "API key secret". These correspond to the `RR_CONSUMER_KEY` and `RR_CONSUMER_SECRET` environment variables below, respectively. Exit that popup and then click "Generate" under "Authentication Tokens > Access token & secret". Again, save these in your text file which correspond to `RR_ACCESS_TOKEN` and `RR_ACCESS_SECRET` below.

#### Python Setup

This README assumes you have python >=3.7 installed on your system. If you don't, there are many easily google-able tutorials for setting that up. Instructions below are for UNIX-like systems (MacOS/Linux). Windows users may have to do some Google-ing and modify the commands.

Create a new virtual environment for this python project by opening your terminal and navigating to this project's directory, and then executing

```
python3 -m venv venv
```

You should now have a folder named `venv/` in the top level directory. Activate the virtual environment by executing

```
source venv/bin/activate
```

Now that your terminal is using the python virtual environment, you can download this project's required dependencies into the environment by running

```
pip install -r requirements.txt
```

#### Environment Setup

Finally, before running the script you need to set the proceeding environment variables to their respective keys saved during the "Twitter Developer Setup" above.

The mapping of the keys is:

- `RR_CONSUMER_KEY` --> "Consumer Keys > API key & secret > API key"
- `RR_CONSUMER_SECRET` --> "Consumer Keys > API key & secret > API key secret"
- `RR_ACCESS_TOKEN` --> "Authentication Tokens > Access token & secret > Access token"
- `RR_ACCESS_SECRET` --> "Authentication Tokens > Access token & secret > Access token secret"

To set these as environment variables, from your shell run (substituting your key strings)

```
export RR_CONSUMER_KEY='zOSMosQ3zZ07aujnV0gEQwjtZ'
export RR_CONSUMER_SECRET='WUxZsze0P8S7Pz5voLCrfLJJ587h7Pc0axcbkjaaxyhbTiCYpx'
export RR_ACCESS_TOKEN='1385251826-YOEkPVQVKC7TxSfP7yxknKAGAZyd0eOlz2NukhV'
export RR_ACCESS_SECRET='5uSknbFvkb93mlQHcrTBqOxa37107a926mplKsRFuDfFk'
```

## Rip Replies

#### Find Tweet ID

Find the Tweet whose replies you wish to rip and copy it's tweet id. The tweet id is the string of numbers at the end of the status' url. So for example the tweet id for `https://twitter.com/dril/status/1334872015954563074` is `1334872015954563074`.

#### Run Script

From your python virtual environment, call the script by running (in your terminal)

```bash
# e.g. to rip the @dril tweet from above,
# you'd run:
# python main.py 1334872015954563074
python main.py <tweet_id>
```

Depending on how many replies your original tweet had, the script may take some significant time to run. Due to Twitter's rate limiting restrictions, the script must frequently pause to avoid being temporarily banned from asking for more replies.

#### Output

The results of the Reply Ripper script will appear in a directory named `output/`. The current format of the outputs is
`YYYYMMDD_<screen_name>_<id_str>.<ext>`

- `YYYYMMDD` is the day the reply was sent
- `<screen_name>` is the user's Twitter username i.e. "@jack" becomes "jack"
- `<id_str> `is a unique ID assigned by Twitter to each photo. We leverage it's uniqueness to prevent filename overlap
- `<ext>` is just the extension of the photo i.e. jpg/png/etc

The script will also output the list of metadata used to name and download each photo under `output/meta.json`
