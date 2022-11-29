import moment from "moment";
import { useSearchParams } from "features/router";
import { useInfo } from "features/info/hooks";
import { useEffect } from "react";

export const to_timestamp = (v, format) => v && moment.utc(v, format).unix();

export const from_timestamp = (v, format = "DD/MM HH:mm") =>
  v && moment.unix(v).utc().format(format);

export const now = () => moment.utc().minutes(0).unix();

const PARAM_DATETIME_FORMAT = "YYYYMMDDHHmm";

export const useReferenceDates = () => {
  const { azba_schedule } = useInfo();
  const [{ reference_date, ...params }, push] = useSearchParams();

  const min = to_timestamp(azba_schedule?.from);
  const max = to_timestamp(azba_schedule?.up_to);

  // get timestamp from params or use Now as default
  //
  const current = to_timestamp(reference_date, PARAM_DATETIME_FORMAT) || now();

  const set = (v) =>
    push({
      reference_date: from_timestamp(v, PARAM_DATETIME_FORMAT),
      ...params,
    });

  useEffect(() => {
    //ensure that param is in available range
    if (reference_date) {
      if (min && current < min) {
        set(min);
      }
      if (max && current > max) {
        set(max);
      }
    }
  }, [min, max, reference_date]);

  return {
    current,
    min,
    max,
    set,
  };
};
