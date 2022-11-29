import scrapy
from datetime import datetime, timezone, timedelta

from ..items import AzbaKnownScheduleItem, AzbaScheduleItem

# scrapy crawl azba_schedule
SIA_URL = "sia.aviation-civile.gouv.fr"
SCHEDULE_PAGE = "https://www.sia.aviation-civile.gouv.fr/schedules"

AZBA_CONTAINER_SELECTOR = ".zones-activees"
AZBA_DATERANGE_SELECTOR = "#dates"
AZBA_AREA_SELECTOR = ".lignes-zones"
DATE_REGEX = r"[0-9]{2}/[0-9]{2}/20[0-9]{2}"
TIME_REGEX = r"[0-9]{2}:[0-9]{2}"
TIMERANGE_REGEX = r"[0-9]{2}[0-9]{2}-[0-9]{2}[0-9]{2}"
AREA_NAME_REGEX = r"R[a-zA-Z0-9\.]+"


class AzbaScheduleSpider(scrapy.Spider):
    name = "azba_schedule"
    allowed_domains = [SIA_URL]

    def start_requests(self):
        yield scrapy.Request(url=SCHEDULE_PAGE, callback=self.parse)

    def parse(self, response):
        schedule = response.css(AZBA_CONTAINER_SELECTOR)
        start, end = self.parse_fromto(schedule.css(AZBA_DATERANGE_SELECTOR))
        yield AzbaKnownScheduleItem(up_to=end, from_d=start)
        for line in schedule.css(AZBA_AREA_SELECTOR):
            for s in self.parse_schedule(line):
                yield AzbaScheduleItem(**s)

    def parse_fromto(self, fromto):
        dates = fromto.re(DATE_REGEX)
        times = fromto.re(TIME_REGEX)
        return [self.parse_datetime(d, times[i]) for i, d in enumerate(dates)]

    def parse_datetime(self, date_string, time_string, next_day=False):
        result = datetime.strptime(
            "{} {}".format(date_string, time_string.replace(":", "")), "%d/%m/%Y %H%M").replace(tzinfo=timezone.utc)
        if next_day:
            return result + timedelta(days=1)
        return result

    def parse_schedule(self, schedule):
        date = schedule.re(DATE_REGEX)[0]
        timerange = schedule.re(TIMERANGE_REGEX)
        area = schedule.re(AREA_NAME_REGEX)[0]
        # FIXME can end time be 00h00 ? what if multiple dates in one schedule ?
        # what if multiple schedules ?
        results = []
        for t in timerange:
            start, end = t.split("-")
            next_day = False
            if end == "0000":
                next_day = True
            results.append({
                'azba': area,
                'activation_time': self.parse_datetime(date, start),
                'deactivation_time': self.parse_datetime(date, end, next_day=next_day)})
        return results
