import requests
from fastapi import HTTPException, status
from ...config import Config 
ADAFRUIT_IO_USERNAME = "Phat_Adafruit"
ADAFRUIT_IO_KEY = "aio_FpCw83QuD1wktNbwmwyGBBajuNEU" 

class DeviceService:

    def _fetch_feed_data(self, feed_key: str):
        """
        Returns the entire list of data records for a given Adafruit IO feed.
        Typically the newest record is index 0.
        """
        url = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/{feed_key}/data"
        headers = {
            "X-AIO-Key": ADAFRUIT_IO_KEY,
            "Content-Type": "application/json"
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Error fetching feed '{feed_key}': {resp.text}"
            )
        return resp.json()

    async def get_single_feed(self, feed_key: str, db):
        """
        Fetch data from one feed, record the newest data in 'record_device' collection, 
        and return the full feed data.
        """
        feed_data = self._fetch_feed_data(feed_key)
        if not feed_data:
            raise HTTPException(
                status_code=404,
                detail=f"No data returned for feed '{feed_key}'."
            )

        newest_entry = feed_data[0]
        await db["record_device"].insert_one({
            "feed_name": feed_key,
            "value": newest_entry.get("value"),
            "created_at": newest_entry.get("created_at")
        })

        return {f"{feed_key}_data": feed_data}

    async def get_all_feeds(self, db):
        """
        Fetch info on ALL Adafruit IO feeds, store the 'last_value' for each feed in 'record_device', 
        and return the feed list.
        """
        url = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds"
        headers = {
            "X-AIO-Key": ADAFRUIT_IO_KEY,
            "Content-Type": "application/json"
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Error fetching all feeds: {resp.text}"
            )
        feeds_list = resp.json()

        for feed in feeds_list:
            await db["record_device"].insert_one({
                "feed_name": feed.get("key"),
                "value": feed.get("last_value"),
                "created_at": feed.get("last_value_at")
            })

        return {"all_feeds": feeds_list}
