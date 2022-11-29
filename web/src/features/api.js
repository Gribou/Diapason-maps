import axios from "axios";
import { useEffect, useReducer } from "react";
import { createApi } from "@reduxjs/toolkit/query/react";
import { API_URI, DEBUG, BACKEND_HOST } from "constants";
import airfieldsEndpoints from "features/airfields/api";
import mapsEndpoints from "features/maps/api";
import civEndpoints from "features/civ/api";
import infoEndpoints from "features/info/api";
import accEndpoints from "features/acc/api";
import phonesEndpoints from "features/phones/api";
import filesEndpoints from "features/files/api";
import navEndpoints from "features/nav/api";
import tilesEndpoints from "features/layers/api";
import radionavEndpoints from "features/radionav/api";

axios.defaults.baseURL = `${API_URI}/`;
axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers.common["Accept"] = `application/json`;

const axiosBaseQuery = () => async (call) => {
  try {
    const result = await axios(call);
    return { data: result.data };
  } catch (error) {
    const { response } = error;
    if (DEBUG) {
      console.error(error, response);
    }
    if (response && response.status === 503) {
      //503 Service Unavailable
      window.location.reload();
      return;
    }
    return { error: generateErrorMessage(error) };
  }
};

function generateErrorMessage(error) {
  const { response, message } = error;
  if (response) {
    if (response.data) {
      if (
        typeof response.data === "string" ||
        response.data instanceof String
      ) {
        return {
          non_field_errors: `${response.status} - ${response.statusText}`,
        };
      } else {
        return response.data;
      }
    } else if (response.status >= 500) {
      return {
        non_field_errors: `Erreur serveur (${response.status} ${response.statusText}) : rafraîchissez la page ou réessayez plus tard.`,
      };
    } else {
      return {
        non_field_errors: `${response.status} - ${response.statusText}`,
      };
    }
  } else {
    return {
      non_field_errors: `Erreur serveur (${message}) : rafraîchissez la page ou réessayez plus tard.`,
    };
  }
}

const api = createApi({
  reducerPath: "api",
  baseQuery: axiosBaseQuery(),
  endpoints: () => ({}),
});

export default api
  .injectEndpoints({
    endpoints: airfieldsEndpoints,
    overrideExisting: false,
  })
  .injectEndpoints({ endpoints: mapsEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: civEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: infoEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: accEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: phonesEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: filesEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: navEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: tilesEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: radionavEndpoints, overrideExisting: false });

//call url without using api slice
async function makeApiCall(url, dispatch) {
  try {
    dispatch({ type: "pending" });
    const response = await axios.request({
      url,
      withCredentials: false,
      baseURL: BACKEND_HOST,
    });
    dispatch({
      type: "success",
      data: response.data,
    });
  } catch (error) {
    const { response } = error;
    if (DEBUG) {
      console.error(error, response);
    }
    dispatch({ type: "failure", error: generateErrorMessage(error) });
  }
}

function api_result_reducer(state, action) {
  switch (action.type) {
    case "reset":
      return { ...action.data };
    case "pending":
      return { ...state, isLoading: true };
    case "success":
      return { ...state, isLoading: false, data: action.data, isSuccess: true };
    case "failure":
      return { ...state, isLoading: false, error: action.error, isError: true };
    default:
      throw new Error();
  }
}

export const useApiCall = (url, disabled) => {
  const [result, dispatch] = useReducer(api_result_reducer, {});

  useEffect(() => {
    if (url && !disabled) {
      makeApiCall(url, (action) => dispatch(action));
    }
  }, [url, disabled]);

  return result;
};
