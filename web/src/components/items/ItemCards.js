import React from "react";
import {
  Card,
  CardHeader,
  Typography,
  IconButton,
  Link,
  useMediaQuery,
} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import {
  EarthBox,
  Helicopter,
  Airport,
  RadioTower,
  Phone,
  Radar,
  FileMultipleOutline,
} from "mdi-material-ui";
import { ROUTES } from "routes";

export default function ItemCard({
  title,
  subheader,
  href,
  to,
  Icon,
  sx = [],
  ...props
}) {
  const xsDown = useMediaQuery((theme) => theme.breakpoints.down("xs"));
  const linkProps = to
    ? { component: RouterLink, to }
    : {
        component: Link,
        href,
        rel: "noopener noreferrer",
        target: "_blank",
        underline: "none",
      };
  return (
    <Card
      sx={[
        { display: "flex", alignItems: "center" },
        ...(Array.isArray(sx) ? sx : [sx]),
      ]}
      {...props}
    >
      <CardHeader
        sx={{
          textDecoration: "none",
          color: "primary.main",
          "& .MuiCardHeader-content": { flex: "1 1 auto", width: "80%" },
        }}
        title={
          <Typography
            component="h4"
            sx={{ typography: { xs: "body1", sm: "h6" } }}
          >
            {title}
          </Typography>
        }
        subheader={subheader}
        avatar={
          <IconButton color="secondary">
            <Icon color="secondary" fontSize={xsDown ? undefined : "large"} />
          </IconButton>
        }
        {...linkProps}
      />
    </Card>
  );
}

export function MapCard({ item, ...props }) {
  const { airfield, name, pdf } = item;
  return (
    <ItemCard
      {...props}
      title={name.split("_").join(" ")}
      subheader={airfield}
      href={pdf}
      Icon={EarthBox}
      {...props}
    />
  );
}

export function AirfieldCard({ item, ...props }) {
  const { icao_code, name, category } = item;
  return (
    <ItemCard
      title={icao_code || category.toUpperCase()}
      subheader={name}
      Icon={category.includes("héli") ? Helicopter : Airport}
      to={ROUTES.airfield.path.replace(":code", icao_code || name)}
      {...props}
    />
  );
}

export function SectorCard({ item, ...props }) {
  const { name, frequencies } = item;
  const vhf_f = frequencies.find((freq) => freq.frequency_type === "VHF");
  const vhf = vhf_f ? `${vhf_f.frequency} MHz` : "";
  const uhf_f = frequencies.find((freq) => freq.frequency_type === "UHF");
  const uhf = uhf_f ? `UHF ${uhf_f.frequency} MHz` : "";
  return (
    <ItemCard
      title={`${name} ${vhf}`}
      subheader={uhf}
      Icon={Radar}
      to={ROUTES.sector.path.replace(":sector_name", name)}
      {...props}
    />
  );
}

export function AccCard({ item, ...props }) {
  const { pk, name, sectors } = item;
  return (
    <ItemCard
      title={name}
      subheader={`${sectors?.length || 0} secteur${sectors?.length ? "s" : ""}`}
      Icon={Radar}
      to={ROUTES.acc.path.replace(":pk", pk)}
      {...props}
    />
  );
}

export function PhoneCard({ item, ...props }) {
  const { name, telephone_number, isExterior } = item;
  return (
    <ItemCard
      title={name}
      subheader={`${isExterior ? "3" : ""} ${telephone_number} #`}
      Icon={Phone}
      {...props}
    />
  );
}

export function FrequencyCard({ item, ...props }) {
  const { value, frequency_type, comments } = item;
  return (
    <ItemCard
      subheader={
        <Typography variant="body2" color="textSecondary">
          {frequency_type}
          <br />
          {comments}
        </Typography>
      }
      title={`${value} MHz`}
      Icon={RadioTower}
      {...props}
    />
  );
}

export function RadionavCard({ item, ...props }) {
  const { short_name, long_name, types } = item;

  return (
    <ItemCard
      subheader={long_name}
      title={`${short_name} (${types?.join(" ") || "?"})`}
      Icon={RadioTower}
      to={ROUTES.station.path.replace(":name", short_name)}
      {...props}
    />
  );
}

export function FileCard({ item, ...props }) {
  const { label, pdf, categories } = item;
  return (
    <ItemCard
      subheader={categories?.join(", ")}
      title={label}
      Icon={FileMultipleOutline}
      href={pdf}
      {...props}
    />
  );
}
