import React from "react";
import SvgIcon from "@mui/material/SvgIcon";
import { useTheme } from "@mui/material/styles";

export default function CoconutsIcon({ baseColor, accentColor, ...props }) {
  const theme = useTheme();
  const baseStyle = {
    fill: baseColor || theme.palette.secondary.main,
    strokeWidth: 6,
    display: "inline",
  };

  const accentStyle = {
    display: "inline",
    fill: accentColor || theme.palette.secondary.main,
    stroke: "none",
    strokeWidth: 0.32,
  };

  return (
    <SvgIcon viewBox="0 0 189.86496 185.74362" {...props}>
      <g
        id="layer3"
        style={{ display: "inline" }}
        transform="translate(-64.510947,-2.0844952)"
      >
        <path
          style={baseStyle}
          d="m 159.63999,79.021915 c 9.53738,45.647565 -11.99673,77.978745 -11.99673,77.978745 h 17.99508 c 11.27693,-34.79052 5.99836,-59.443797 2.99919,-71.980384 M 181.59399,67.98492 c 1.01972,1.259657 2.03943,2.579294 2.81922,3.958919 10.2572,16.255571 8.21777,36.769981 -3.77896,50.626201 5.03861,-12.29665 4.31882,-26.812694 -3.2991,-38.929389 -0.47986,-0.779786 -1.01973,-1.439604 -1.4996,-2.159411 -3.53903,-4.978641 -8.0378,-8.937561 -12.95647,-11.876758 -17.27526,5.518491 -29.75186,21.654093 -29.75186,40.728898 0,4.43879 0.65982,8.69762 1.85949,12.65654 -5.03862,-7.01808 -7.97783,-15.59574 -7.97783,-24.83323 0,-14.096157 6.83814,-26.572755 17.33528,-34.370625 -8.69763,-0.65982 -17.93511,1.259658 -25.97292,6.238299 -3.71899,2.459326 -6.9581,5.278566 -9.71735,8.457699 3.2991,-7.977828 8.99755,-15.11588 16.79542,-20.034543 8.99755,-5.638461 19.19476,-7.497954 29.03208,-6.058347 -2.45933,-3.359084 -5.4585,-6.538218 -9.05753,-9.35745 -3.47905,-2.519314 -7.25802,-4.558757 -11.21694,-5.998364 8.63765,0.239934 17.27529,2.999181 24.65328,8.577662 3.77897,2.819231 6.77814,6.2383 9.17749,9.837317 0.59984,0 1.13968,-0.05998 1.73952,-0.05998 19.19476,0 35.45034,12.65655 40.84887,30.111788 -6.71817,-9.477421 -17.09536,-15.895666 -29.03209,-17.515228 z"
          id="path106"
        />
        <path
          style={accentStyle}
          d="m 103.21563,15.622573 c -1.95095,1.805797 -4.432198,4.822244 -6.883014,5.855589 -1.142044,0.481616 -2.408341,-0.35563 -3.577012,-0.350278 -1.737949,0.008 -3.389048,1.643591 -4.120616,3.095543 5.328591,2.503135 6.460492,5.369736 9.192144,10.193604 l 3.251488,-3.504306 0.2,-3.817696 6.69157,-6.057104 c 1.15916,4.259589 3.37161,9.982279 5.82053,13.655289 1.22604,1.838353 3.70728,1.158567 4.22141,-0.914494 1.38484,-5.581157 -4.37863,-11.959009 -3.31646,-17.519047 0.73917,-3.868345 12.21794,-8.3748748 7.76672,-12.9878023 -4.71778,-4.8894549 -9.73353,6.8963583 -13.85826,6.9840233 -5.6126,0.119265 -11.13042,-6.919705 -16.799437,-6.3587223 -2.150328,0.2127785 -3.175093,2.6672681 -1.512583,4.1485262 3.333578,2.9697481 8.822873,5.8520541 12.92352,7.5768751 m 134.07852,21.342859 c -1.21907,0.390543 -4.25406,1.587973 -4.11428,3.199199 0.22854,2.63441 3.47178,6.196119 4.66961,8.587156 3.25022,6.486955 6.14891,13.069157 8.13632,20.068662 8.57278,30.190585 0.0824,62.188311 -20.79041,85.371431 -25.33862,28.14327 -69.94811,36.82057 -103.91244,20.30502 C 98.843022,163.58497 82.115857,143.66412 74.079387,120.10702 66.82742,98.849847 68.665531,75.459033 77.955936,55.12279 79.90372,50.858996 82.07053,46.629606 84.62341,42.699335 c 1.684381,-2.592998 4.033766,-5.154142 5.27946,-7.963754 -0.961371,-0.735532 -2.466347,-2.671297 -3.775118,-2.536614 -1.016208,0.10458 -1.789615,1.480493 -2.331318,2.218064 -1.808634,2.461756 -3.42233,5.023536 -4.98753,7.645203 -6.218961,10.416908 -10.453687,21.848398 -12.741263,33.766318 -6.055086,31.546968 5.987573,64.482508 28.589786,86.640858 30.966113,30.35814 81.444303,33.17413 117.279083,9.97794 15.37751,-9.95405 27.54664,-24.95745 34.73141,-41.82818 9.182,-21.56138 10.2074,-45.592802 2.82484,-67.851177 -3.06732,-9.247192 -8.14107,-17.079065 -12.19861,-25.802561"
          id="path309"
        />
      </g>
    </SvgIcon>
  );
}